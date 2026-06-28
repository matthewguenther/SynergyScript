"""The Middle Manager — recursive-descent parser producing the AST.

Grammar: README.md §5. The parser consumes the token stream from the lexer
and validates block structure: every ``if`` / ``let's drill down while`` closes
with ``circle back``; every ``schedule a meeting`` closes with ``end meeting``.
"""

from __future__ import annotations

from synergyscript import ast_nodes as ast
from synergyscript.errors import ParseError
from synergyscript.tokens import Token, TokenType as T

# Tokens that can begin an expression (used to detect "no arguments").
_EXPR_STARTERS = frozenset(
    {
        T.NUMBER,
        T.STRING,
        T.TRUE,
        T.FALSE,
        T.NULL,
        T.LAST_EMAIL,
        T.IDENT,
        T.PING,
        T.LEVERAGE,
        T.TAKE,
        T.SCALE,
        T.STREAMLINE,
    }
)

_COMPARISONS = frozenset({T.EQ, T.NEQ, T.GT, T.LT, T.GTE, T.LTE})
_COMPARISON_OPS = {
    T.EQ: "==",
    T.NEQ: "!=",
    T.GT: ">",
    T.LT: "<",
    T.GTE: ">=",
    T.LTE: "<=",
}

# Block terminators — tokens that close a block rather than start a statement.
_TERMINATORS = frozenset({T.END_BLOCK, T.END_FUNC, T.ELIF, T.ELSE})


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = list(tokens)
        self.pos = 0
        # The lexer leaves the EOF sentinel to us; ensure exactly one trailing EOF.
        if not self.tokens or self.tokens[-1].type is not T.EOF:
            line = self.tokens[-1].line if self.tokens else 1
            self.tokens.append(Token(T.EOF, "", line))

    # --- entry point --------------------------------------------------------

    def parse(self) -> ast.Program:
        """program = { statement } ; consume until EOF."""
        body = self._block(())
        self._expect(T.EOF, "end of program")
        return ast.Program(body)

    # --- token cursor helpers ----------------------------------------------

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _check(self, type_: T) -> bool:
        return self._peek().type is type_

    def _match(self, *types: T) -> Token | None:
        """Advance and return the token if it matches any ``types``, else None."""
        if self._peek().type in types:
            return self._advance()
        return None

    def _expect(self, type_: T, what: str) -> Token:
        tok = self._peek()
        if tok.type is not type_:
            raise ParseError(f"Expected {what}", tok.line)
        return self._advance()

    def _skip_newlines(self) -> None:
        while self._check(T.NEWLINE):
            self._advance()

    def _block(self, stop: tuple[T, ...]) -> list[ast.Node]:
        """Parse statements until a token in ``stop`` (or EOF) is the next token."""
        stmts: list[ast.Node] = []
        self._skip_newlines()
        while not self._check(T.EOF) and self._peek().type not in stop:
            stmts.append(self.statement())
            self._skip_newlines()
        return stmts

    # --- statements ---------------------------------------------------------

    def statement(self) -> ast.Node:
        """Dispatch on the leading token to the matching statement rule."""
        tok = self._peek()
        kind = tok.type
        if kind is T.TOUCH_BASE:
            self._advance()
            return ast.TouchBase(tok.line)
        if kind is T.ONBOARD:
            return self.onboard()
        if kind is T.TRANSITION:
            return self.transition()
        if kind is T.PRINT:
            return self.output()
        if kind is T.INPUT:
            return self.input_stmt()
        if kind is T.IF:
            return self.if_block()
        if kind is T.WHILE:
            return self.while_block()
        if kind is T.FUNC_DEF:
            return self.func_def()
        if kind is T.DELIVER:
            return self.return_stmt()
        if kind is T.HARD_STOP:
            self._advance()
            return ast.Break(tok.line)
        if kind is T.CONTINUE:
            self._advance()
            return ast.Continue(tok.line)
        if kind is T.PING:
            return self.call()
        if kind in _TERMINATORS:
            raise ParseError(
                f"'{tok.lexeme}' has nothing to close — check your block structure",
                tok.line,
            )
        raise ParseError(f"Unexpected '{tok.lexeme}'", tok.line)

    def onboard(self) -> ast.Onboard:
        """onboard IDENT as expression"""
        line = self._expect(T.ONBOARD, "onboard").line
        name = self._expect(T.IDENT, "a variable name").lexeme
        self._expect(T.AS, "'as'")
        return ast.Onboard(name, self.expression(), line)

    def transition(self) -> ast.Transition:
        """transition IDENT to expression"""
        line = self._expect(T.TRANSITION, "transition").line
        name = self._expect(T.IDENT, "a variable name").lexeme
        self._expect(T.TO, "'to'")
        return ast.Transition(name, self.expression(), line)

    def output(self) -> ast.Print:
        """run it up the flagpole expression"""
        line = self._expect(T.PRINT, "run it up the flagpole").line
        return ast.Print(self.expression(), line)

    def input_stmt(self) -> ast.Input:
        """poll the stakeholders into IDENT"""
        line = self._expect(T.INPUT, "poll the stakeholders into").line
        name = self._expect(T.IDENT, "a variable name").lexeme
        return ast.Input(name, line)

    def return_stmt(self) -> ast.Return:
        """deliver expression"""
        line = self._expect(T.DELIVER, "deliver").line
        return ast.Return(self.expression(), line)

    def if_block(self) -> ast.If:
        """if ... { pivot to ... } [ pivot ... ] circle back"""
        line = self._expect(T.IF, "if we have bandwidth for").line
        branches: list[tuple[ast.Node | None, list[ast.Node]]] = []
        cond = self.expression()
        branches.append((cond, self._block((T.ELIF, T.ELSE, T.END_BLOCK))))
        while self._match(T.ELIF):
            elif_cond = self.expression()
            branches.append((elif_cond, self._block((T.ELIF, T.ELSE, T.END_BLOCK))))
        if self._match(T.ELSE):
            branches.append((None, self._block((T.END_BLOCK,))))
        self._expect(T.END_BLOCK, "'circle back' to close the if")
        return ast.If(branches, line)

    def while_block(self) -> ast.While:
        """let's drill down while COND ... circle back"""
        line = self._expect(T.WHILE, "let's drill down while").line
        cond = self.expression()
        body = self._block((T.END_BLOCK,))
        self._expect(T.END_BLOCK, "'circle back' to close the loop")
        return ast.While(cond, body, line)

    def func_def(self) -> ast.FuncDef:
        """schedule a meeting IDENT taking [params] ... end meeting"""
        line = self._expect(T.FUNC_DEF, "schedule a meeting").line
        name = self._expect(T.IDENT, "a function name").lexeme
        self._expect(T.TAKING, "'taking'")
        params: list[str] = []
        if self._check(T.IDENT):
            params.append(self._advance().lexeme)
            while self._match(T.COMMA):
                params.append(self._expect(T.IDENT, "a parameter name").lexeme)
        body = self._block((T.END_FUNC,))
        self._expect(T.END_FUNC, "'end meeting' to close the function")
        return ast.FuncDef(name, params, body, line)

    def call(self) -> ast.Call:
        """ping IDENT with [args]"""
        line = self._expect(T.PING, "ping").line
        name = self._expect(T.IDENT, "a function name").lexeme
        self._expect(T.WITH, "'with'")
        args: list[ast.Node] = []
        if self._peek().type in _EXPR_STARTERS:
            args.append(self.expression())
            while self._match(T.COMMA):
                args.append(self.expression())
        return ast.Call(name, args, line)

    # --- expressions (precedence climbing per §5) ---------------------------

    def expression(self) -> ast.Node:
        return self.logic_or()

    def logic_or(self) -> ast.Node:
        """logic_and { 'or' logic_and }"""
        node = self.logic_and()
        while (tok := self._match(T.OR)) is not None:
            node = ast.BinaryOp("or", node, self.logic_and(), tok.line)
        return node

    def logic_and(self) -> ast.Node:
        """comparison { 'and' comparison }"""
        node = self.comparison()
        while (tok := self._match(T.AND)) is not None:
            node = ast.BinaryOp("and", node, self.comparison(), tok.line)
        return node

    def comparison(self) -> ast.Node:
        """arithmetic { (== | != | > | < | >= | <=) arithmetic }"""
        node = self.arithmetic()
        while self._peek().type in _COMPARISONS:
            tok = self._advance()
            op = _COMPARISON_OPS[tok.type]
            node = ast.BinaryOp(op, node, self.arithmetic(), tok.line)
        return node

    def arithmetic(self) -> ast.Node:
        """keyword-led leverage/take/scale/streamline, else primary"""
        tok = self._peek()
        if tok.type is T.LEVERAGE:
            self._advance()
            left = self.arithmetic()
            self._expect(T.WITH, "'with'")
            return ast.BinaryOp("+", left, self.arithmetic(), tok.line)
        if tok.type is T.TAKE:
            self._advance()
            left = self.arithmetic()
            self._expect(T.OFFLINE_BY, "'offline by'")
            return ast.BinaryOp("-", left, self.arithmetic(), tok.line)
        if tok.type is T.SCALE:
            self._advance()
            left = self.arithmetic()
            self._expect(T.BY, "'by'")
            return ast.BinaryOp("*", left, self.arithmetic(), tok.line)
        if tok.type is T.STREAMLINE:
            self._advance()
            left = self.arithmetic()
            self._expect(T.BY, "'by'")
            return ast.BinaryOp("/", left, self.arithmetic(), tok.line)
        return self.primary()

    def primary(self) -> ast.Node:
        """NUMBER | STRING | aligned | blocked | tbd | per my last email | call | IDENT"""
        tok = self._peek()
        kind = tok.type
        if kind is T.NUMBER:
            self._advance()
            return ast.Literal(tok.value, tok.line)
        if kind is T.STRING:
            self._advance()
            return ast.Literal(tok.value, tok.line)
        if kind is T.TRUE:
            self._advance()
            return ast.Literal(True, tok.line)
        if kind is T.FALSE:
            self._advance()
            return ast.Literal(False, tok.line)
        if kind is T.NULL:
            self._advance()
            return ast.Literal(None, tok.line)
        if kind is T.LAST_EMAIL:
            self._advance()
            return ast.LastEmail(tok.line)
        if kind is T.PING:
            return self.call()
        if kind is T.IDENT:
            self._advance()
            return ast.Var(tok.lexeme, tok.line)
        raise ParseError(f"Expected an expression, found '{tok.lexeme}'", tok.line)


def parse(tokens: list[Token]) -> ast.Program:
    """Convenience wrapper used by the CLI and tests."""
    return Parser(tokens).parse()
