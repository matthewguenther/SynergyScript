# SynergyScript

> The Enterprise-Grade Corporate Esoteric Language — the first programming language designed from the ground up to sound exactly like a Q3 deliverables read-out.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-pre--alpha-orange)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

SynergyScript is an interpreted, imperative, dynamically typed esoteric language whose
keywords are corporate jargon. You `onboard` a variable, `let's drill down while` you loop,
and `circle back` to close your blocks. Source files use the **`.corp`** extension.

<details>
<summary>🎨 Banner concept (AI image generation prompt)</summary>

> *A hyper-realistic, overly retouched stock photo of three impeccably dressed business professionals (one pointing a pen, one holding a glowing tablet, one nodding enthusiastically) standing around a transparent glass whiteboard. The whiteboard features a completely meaningless upward-trending line graph and the word "SYNERGY" written in bold blue marker. The lighting is sterile and aggressively optimistic. Lens flare in the top right corner. Corporate blue and gray color palette.*

</details>

---

## 🏢 Executive Summary: Our Mission Statement

In today's fast-paced, paradigm-shifting B2B ecosystem, there is an unacceptable silo between the C-suite's vision and the dev-ops execution pipeline. For too long, developers have relied on non-synergistic, highly technical keywords like "while loops" and "booleans" that fail to move the needle on key performance indicators (KPIs).

**SynergyScript** changes the paradigm.

By leveraging a robust, scalable, and fully integrated corporate-jargon-based instruction set, SynergyScript ensures 100% cross-functional alignment across all verticals. Whether you're onboarding new variables, drilling down into iterative strategies, or taking bugs offline, SynergyScript empowers your enterprise to achieve true operational excellence. We aren't just writing code; we are strategically aligning our digital assets to maximize stakeholder value.

---

## 🚀 Quickstart

Requires **Python 3.10+** (the reference interpreter uses only the standard library).

```bash
git clone https://github.com/yourusername/synergyscript.git
cd synergyscript
pip install -e .          # installs the `synergy` command
```

```bash
synergy execute scripts/q3_earnings.corp    # run a program
synergy HR scripts/fibonacci.corp           # lint with the HR linter
python -m synergyscript execute file.corp   # equivalent, without the entry point
```

### Hello, Stakeholders

```text
touch base
run it up the flagpole "Hello World"
hard stop
```

---

## 📑 Language Reference

> This section is **normative**. Where it uses "MUST" / "is" it defines required behavior for the reference implementation. The corporate flavor is preserved, but every construct below is specified precisely enough to build.

### 1. Architecture Overview

SynergyScript's reference implementation is written in **Python 3.10+** and uses a three-stage tree-walking pipeline:

| Stage | Module | Role |
| :--- | :--- | :--- |
| Lexer — "The Recruiter" | [src/synergyscript/lexer.py](src/synergyscript/lexer.py) | Tokenizes `.corp` files, recognizing **multi-word corporate phrases as single tokens** (see §3) |
| Parser — "The Middle Manager" | [src/synergyscript/parser.py](src/synergyscript/parser.py) | Recursive-descent build of the AST, validating that every opened block is correctly closed |
| Interpreter — "The Intern" | [src/synergyscript/interpreter.py](src/synergyscript/interpreter.py) | Walks the AST and executes it directly against nested runtime scopes |

There is no separate compile step and no bytecode in v1; the interpreter evaluates the AST in place. ("Transpile to Python bytecode" is a possible future optimization, explicitly out of scope for v1.)

### 2. Source Files

- Extension: **`.corp`**. Encoding: **UTF-8**.
- A program is a sequence of **statements separated by newlines**. One statement per line.
- **Indentation is cosmetic** and ignored by the lexer. Blocks are delimited by explicit terminator phrases (`circle back`, `end meeting`) — never by whitespace.
- Blank lines and comment-only lines are ignored.

### 3. Lexical Structure

The lexer scans left to right and, at each position, applies **longest-phrase-first matching**: it attempts to match the longest known keyword phrase before falling back to shorter ones or to a literal/identifier. Phrase matching is **word-boundary aware** (`as` never matches inside `assets`).

This is the single most important implementation detail: `pivot to` MUST be tried before `pivot`, and `run it up the flagpole` is one token, not five.

**Token categories**

- **Keyword phrases** — the corporate vocabulary in §4 (each maps to exactly one token type).
- **Identifiers** — `[A-Za-z_][A-Za-z0-9_]*` that are not reserved phrases.
- **Number literals** — integers, e.g. `42` (`headcount`).
- **String literals** — double-quoted, e.g. `"Hello World"` (`messaging`).
- **Symbols** — comparison operators `== != > < >= <=` and the argument separator `,`.
- **Comments** — `//` to end of line. The idiomatic prefixes `// cc'ing:` and `// per my last email:` are conventional, not special; everything after `//` is discarded.
- **Newline** — emitted as a statement separator token; runs of blank lines collapse to one.

### 4. Vocabulary → Token Mapping

This table is the contract shared by the lexer ([keywords.py](src/synergyscript/keywords.py)) and the parser. The reference implementation keeps it in one place; do not duplicate it.

#### Data Types & Literal Values
| SynergyScript | Standard | Literals |
| :--- | :--- | :--- |
| `headcount` | Integer | `0`, `42` |
| `messaging` | String | `"Hello World"` |
| `buy-in` | Boolean | `aligned` (true), `blocked` (false) |
| `tbd` | Null / undefined | `tbd` |

#### Statements
| Phrase | Token | Meaning |
| :--- | :--- | :--- |
| `touch base` | `TOUCH_BASE` | Kickoff no-op (optional; conventionally the first line) |
| `onboard NAME as EXPR` | `ONBOARD` / `AS` | Declare a variable in the current scope |
| `transition NAME to EXPR` | `TRANSITION` / `TO` | Reassign an existing variable |
| `run it up the flagpole EXPR` | `PRINT` | Write a value to stdout |
| `poll the stakeholders into NAME` | `INPUT` | Read one line of stdin into a variable (as `messaging`) |
| `// ...` | (discarded) | Comment |

#### Operators (expressions)
| Phrase | Token | Operation |
| :--- | :--- | :--- |
| `leverage X with Y` | `LEVERAGE` / `WITH` | `X + Y` |
| `take X offline by Y` | `TAKE` / `OFFLINE_BY` | `X - Y` |
| `scale X by Y` | `SCALE` / `BY` | `X * Y` |
| `streamline X by Y` | `STREAMLINE` / `BY` | `X / Y` (integer division; `streamline` by `0` is a runtime error) |
| `==` `!=` `>` `<` `>=` `<=` | comparison | yields `buy-in` |
| `and` `or` | `AND` / `OR` | logical combinators (short-circuit), yield `buy-in` |

> **Note:** `take ... offline by ...` is a *circumfix* operator. The lexer emits two tokens (`TAKE`, then `OFFLINE_BY`); the parser pairs them around the operands.

#### Control Flow
| Phrase | Token | Meaning |
| :--- | :--- | :--- |
| `if we have bandwidth for COND` | `IF` | If |
| `pivot to COND` | `ELIF` | Else-if (zero or more) |
| `pivot` | `ELSE` | Else (optional) |
| `let's drill down while COND` | `WHILE` | While loop |
| `hard stop` | `HARD_STOP` | Break innermost loop; **at top level / outside any loop, halt the program** |
| `push to next quarter` | `CONTINUE` | Continue loop |
| `circle back` | `END_BLOCK` | Close an `if` or `while` block |

#### Functions
| Phrase | Token | Meaning |
| :--- | :--- | :--- |
| `schedule a meeting NAME taking P1, P2` | `FUNC_DEF` / `TAKING` | Define a function |
| `deliver EXPR` | `DELIVER` | Return a value from a function |
| `end meeting` | `END_FUNC` | Close a function definition |
| `ping NAME with A1, A2` | `PING` / `WITH` | Call a function (usable as a statement or an expression) |

### 5. Grammar (EBNF)

Recursive descent over the phrase tokens above. `NEWLINE` separates statements; it is omitted from expression rules for clarity.

```ebnf
program     = { statement } ;

statement   = "touch base"
            | onboard | transition | output | input
            | if_block | while_block | func_def
            | return_stmt | "hard stop" | "push to next quarter"
            | call ;                      (* call as an expression-statement *)

onboard     = "onboard" IDENT "as" expression ;
transition  = "transition" IDENT "to" expression ;
output      = "run it up the flagpole" expression ;
input       = "poll the stakeholders into" IDENT ;
return_stmt = "deliver" expression ;

if_block    = "if we have bandwidth for" expression NEWLINE { statement }
              { "pivot to" expression NEWLINE { statement } }
              [ "pivot" NEWLINE { statement } ]
              "circle back" ;

while_block = "let's drill down while" expression NEWLINE { statement }
              "circle back" ;

func_def    = "schedule a meeting" IDENT "taking" [ params ] NEWLINE
              { statement } "end meeting" ;
params      = IDENT { "," IDENT } ;

call        = "ping" IDENT "with" [ args ] ;
args        = expression { "," expression } ;

(* Expression precedence, lowest to highest *)
expression  = logic_or ;
logic_or    = logic_and { "or" logic_and } ;
logic_and   = comparison { "and" comparison } ;
comparison  = arithmetic { ( "==" | "!=" | ">" | "<" | ">=" | "<=" ) arithmetic } ;
arithmetic  = "leverage"   arithmetic "with"       arithmetic
            | "take"       arithmetic "offline by" arithmetic
            | "scale"      arithmetic "by"          arithmetic
            | "streamline" arithmetic "by"          arithmetic
            | primary ;
primary     = NUMBER | STRING | "aligned" | "blocked" | "tbd"
            | call | IDENT ;
```

Because every arithmetic operator is **keyword-led** with a fixed connector word, operands parse greedily without ambiguity (e.g. `leverage a with scale b by c` is `a + (b * c)`). Use explicit nested phrases for grouping; v1 has no parentheses.

### 6. Semantics

**Arithmetic phrases are pure expressions.** They evaluate to a value and have **no side effects** — they never mutate their operands. To change a variable you MUST use `transition`. (This is why `count += 1` is written `transition count to leverage count with 1`.)

**Truthiness** (for `if` / `while` / `and` / `or` conditions). Conditions should evaluate to `buy-in`; other types are coerced: `headcount` `0` → `blocked`, nonzero → `aligned`; empty `messaging` → `blocked`, non-empty → `aligned`; `tbd` → `blocked`.

**Scope.** The top level is the global scope. Each function call creates a fresh local scope whose parent is the **global** scope (functions are not closures over their definition site in v1). `onboard` binds in the current scope; `transition` updates the nearest existing binding (local, then global) and errors if the name was never onboarded. Reads search local then global.

**Functions & return.** `deliver` returns a value and unwinds to the caller. A function that finishes without `deliver` returns `tbd`. A `call` used as a statement discards the result.

**`hard stop` / `touch base` resolution.** `hard stop` breaks the innermost enclosing loop; with no enclosing loop it halts the whole program with success. `touch base` is a no-op kickoff statement (so example programs that begin with it and those that don't are both valid).

### 7. Errors & the `HR` Linter

The interpreter raises typed errors with a line number:
- **Lex errors** — unrecognized token.
- **Parse errors** — unclosed block (missing `circle back` / `end meeting`), stray terminator, malformed statement.
- **Runtime errors** — undefined variable, type mismatch, division (`streamline`) by `0`, calling an undefined function or with the wrong arity.

`HR` is a **static** linter (no execution) that emits passive-aggressive warnings. v1 checks:
- Blocks opened but never closed (`circle back` / `end meeting`).
- A terminator with no matching opener.
- Variables `onboard`ed but never used.
- `transition` to a name that was never `onboard`ed.

```bash
synergy HR scripts/q3_earnings.corp
# [HR Warning] Line 12: Let's touch base about your lack of 'circle back' for the loop you
#               opened. We need to align on closing our brackets.
```

---

## 📂 Examples

### The Corporate Countdown

```text
// per my last email: This script tracks remaining quarters

touch base

onboard quarters_left as 4
onboard status as "pending"

let's drill down while quarters_left > 0
    run it up the flagpole quarters_left
    transition quarters_left to take quarters_left offline by 1
circle back

if we have bandwidth for quarters_left == 0
    transition status to "KPIs Met"
    run it up the flagpole status
pivot
    run it up the flagpole "We need to optimize our workflows."
circle back

hard stop
```

### Fibonacci Sequence (Action Items)

```text
// cc'ing: Generating fibonacci sequence up to N

schedule a meeting fibonacci taking n
    onboard a as 0
    onboard b as 1
    onboard temp as 0
    onboard count as 0

    let's drill down while count < n
        run it up the flagpole a
        transition temp to a
        transition a to b
        transition b to leverage temp with b
        transition count to leverage count with 1
    circle back
end meeting

ping fibonacci with 10
hard stop
```

> Note: arithmetic phrases are expressions, so increments are written with `transition`
> (`transition count to leverage count with 1`) — there is no bare `leverage` statement.

---

## 🛠️ Project Layout & Development

```
src/synergyscript/
├── lexer.py         # The Recruiter — tokenizer
├── parser.py        # The Middle Manager — AST builder
├── interpreter.py   # The Intern — tree-walking evaluator
├── keywords.py      # canonical phrase → token table (§4)
├── tokens.py        # TokenType / Token
├── ast_nodes.py     # AST dataclasses
├── environment.py   # variable scopes
├── builtins.py      # I/O + value rendering
├── linter.py        # the HR static linter
├── errors.py        # errors + control-flow signals
└── cli.py           # the `synergy` command
scripts/             # example .corp programs
tests/               # pytest suite
```

```bash
pip install -e ".[dev]"     # editable install + pytest
pytest                      # run the full suite
pytest tests/test_lexer.py::test_phrase_longest_match   # run a single test
```

---

## 🤝 Contributing

Please ensure all pull requests are approved by at least three managers and align with our core values. Do not push directly to main; that is a career-limiting move.

## 📄 License

MIT.
