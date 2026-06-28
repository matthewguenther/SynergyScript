# SynergyScript

> The Enterprise-Grade Corporate Esoteric Language - the first programming language designed from the ground up to sound exactly like a Q3 deliverables read-out.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-pre--alpha-orange)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

SynergyScript is an interpreted, imperative, dynamically typed esoteric language whose
keywords are corporate jargon. You `onboard` a variable, `let's drill down while` you loop,
and `circle back` to close your blocks. Source files use the **`.corp`** extension.

<p align="center">
  <img src="SynergyScript_Logo.png" alt="SynergyScript logo" width="640">
</p>

---

## 🏢 Executive Summary: Our Mission Statement

In today's fast-paced, paradigm-shifting B2B ecosystem, there is an unacceptable silo between the C-suite's vision and the dev-ops execution pipeline. For too long, developers have relied on non-synergistic, highly technical keywords like "while loops" and "booleans" that fail to move the needle on key performance indicators (KPIs).

**SynergyScript** changes the paradigm.

By leveraging a robust, scalable, and fully integrated corporate-jargon-based instruction set, SynergyScript ensures 100% cross-functional alignment across all verticals. Whether you're onboarding new variables, drilling down into iterative strategies, or taking bugs offline, SynergyScript empowers your enterprise to achieve true operational excellence. We aren't just writing code; we are strategically aligning our digital assets to maximize stakeholder value.

---

## 🚀 Quickstart

Requires **Python 3.10+** (the reference interpreter uses only the standard library).

```bash
git clone https://github.com/matthewguenther/SynergyScript/synergyscript.git
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

> This is the official rulebook for how SynergyScript works. It's still written with a wink, but everything here is real and precise enough to actually build the language from. If you just want to *write* `.corp` programs, skim the cheat sheet in §4 and the examples below - that's honestly all you need.

### 1. How a Program Runs (The Org Chart)

When you run a `.corp` file, it gets passed down the chain to three "employees," each with one job:

| Employee | What they do |
| :--- | :--- |
| **The Recruiter** ([lexer.py](src/synergyscript/lexer.py)) | Reads your file and chops it into the "words" the language knows. The tricky part: a phrase like `run it up the flagpole` counts as **one** word, not five. |
| **The Middle Manager** ([parser.py](src/synergyscript/parser.py)) | Takes those words and works out the structure - which lines are loops, which are `if`s - and double-checks that every block you open also gets closed. |
| **The Intern** ([interpreter.py](src/synergyscript/interpreter.py)) | Actually runs your program, line by line, and keeps track of your variables. |

There's no separate "compile" or "build" step. The Intern just reads your code and does it.

### 2. Writing a `.corp` File

- Files end in **`.corp`** and are plain text (UTF-8).
- **One instruction per line.** A new line means a new statement.
- **Spaces and indentation are just for looks** and are ignored. Blocks begin and end with real words (`circle back`, `end meeting`), not by indenting.
- Blank lines and comment-only lines are skipped.

### 3. The One Weird Trick (Multi-Word Keywords)

Most languages split your code wherever there's a space. SynergyScript can't, because its keywords are made of *several* words. `run it up the flagpole` is a single command, not a sentence.

So the Recruiter always grabs the **longest** matching phrase it can. It tries `pivot to` before it tries plain `pivot`. It also respects word boundaries, so the keyword `as` won't accidentally fire inside the word `assets`.

Here's everything the Recruiter recognizes:

- **Keyword phrases** - the corporate vocabulary listed in §4.
- **Names** (your variables and functions) - things like `quarters_left`. Letters, numbers, and underscores; can't start with a number.
- **Numbers** - whole numbers like `42`.
- **Text** - anything inside double quotes, like `"Hello World"`.
- **Comparisons and commas** - `== != > < >= <=`, plus `,` for separating items in a list.
- **Comments** - anything after `//` on a line is ignored. (Fun convention: starting a comment with `// cc'ing:` or `// per my last email:` reads great, but it's not special - it's just a normal comment.)

### 4. The Vocabulary (Cheat Sheet)

This is the dictionary: the corporate phrase on the left, what it actually means on the right.

#### Kinds of Values
| SynergyScript | What it really is | Examples |
| :--- | :--- | :--- |
| `headcount` | A whole number | `0`, `42` |
| `messaging` | Text | `"Hello World"` |
| `buy-in` | True or false | `aligned` (true), `blocked` (false) |
| `tbd` | "Nothing yet" / empty | `tbd` |

#### Doing Things
| Phrase | What it does |
| :--- | :--- |
| `touch base` | Does nothing - a polite way to kick off a program. |
| `onboard NAME as VALUE` | Creates a new variable. |
| `transition NAME to VALUE` | Changes a variable that already exists. |
| `run it up the flagpole VALUE` | Prints something to the screen. |
| `poll the stakeholders into NAME` | Asks the user to type a line, saves it as text. |
| `// ...` | A comment (ignored). |

#### Math and Logic
| Phrase | What it does |
| :--- | :--- |
| `leverage X with Y` | Add (`X + Y`) |
| `take X offline by Y` | Subtract (`X - Y`) |
| `scale X by Y` | Multiply (`X * Y`) |
| `streamline X by Y` | Divide, whole numbers only (`X / Y`). Dividing by `0` is an error. |
| `== != > < >= <=` | Compare two things; gives you back true or false |
| `and` / `or` | Combine true/false conditions |

> Heads up: `take ... offline by ...` wraps around its two numbers like a sandwich - the first number goes after `take`, the second after `offline by`.

#### Loops, Ifs, and Branching
| Phrase | What it does |
| :--- | :--- |
| `if we have bandwidth for CONDITION` | If |
| `pivot to CONDITION` | Else-if (you can stack as many as you like) |
| `pivot` | Else (optional) |
| `let's drill down while CONDITION` | While loop |
| `hard stop` | Break out of a loop. (Outside any loop, it ends the whole program.) |
| `push to next quarter` | Skip to the next loop iteration (a.k.a. "continue") |
| `circle back` | Closes an `if` or a `while` block |

#### Functions
| Phrase | What it does |
| :--- | :--- |
| `schedule a meeting NAME taking P1, P2` | Define a function (with inputs) |
| `deliver VALUE` | Hand a value back from a function |
| `end meeting` | Closes a function |
| `ping NAME with A1, A2` | Call a function |

### 5. The Grammar (For the Nerds, Optional)

You do **not** need this to write programs - the cheat sheet and examples cover everything. This is the exact, formal structure, here for anyone building or extending the language.

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

The short version: every math phrase starts with a keyword (`leverage`, `scale`, and friends) and uses a fixed connecting word, so there's never any confusion about which number pairs with which. For example, `leverage a with scale b by c` always means `a + (b * c)`. There are no parentheses in v1 - if you need grouping, just nest the phrases.

### 6. The Rules That Trip People Up

**Math never changes your variables.** Writing `leverage count with 1` just *calculates* `count + 1` and hands you the answer - it leaves `count` itself untouched. To actually update a variable, you have to `transition` it. That's why "add 1 to count" is written:

> `transition count to leverage count with 1`

**What counts as "true."** Conditions (in `if`, `while`, `and`, `or`) work best with true/false values. If you hand them something else, here's how it's judged:

- A `headcount` of `0` is false; any other number is true.
- Empty text `""` is false; any other text is true.
- `tbd` (nothing) is false.

**Where variables live.** The main body of your program is the shared "global" space. Every time you call a function, it gets its own private workspace. Variables you `onboard` inside a function stay inside that function, and a function can only see its own variables plus the global ones (not the variables of whoever called it). `transition` updates the closest matching variable, and complains if that variable was never created in the first place.

**Functions and handing values back.** `deliver` sends a value back and immediately exits the function. If a function finishes without a `deliver`, you get `tbd` back. If you call a function but don't use its result, the result is simply thrown away.

**`hard stop` and `touch base`, one more time.** `hard stop` breaks out of the innermost loop you're in - but if you're not in a loop at all, it just ends the program successfully. `touch base` does nothing whatsoever; it's purely a nice way to start things off. (So programs that begin with it and programs that don't are equally valid.)

### 7. Errors and the `HR` Linter

When something's wrong, SynergyScript tells you the line number and what kind of problem it hit:

- **Word errors** - it ran into something it doesn't recognize.
- **Structure errors** - a block you opened was never closed (missing `circle back` or `end meeting`), a closer with nothing to close, or a line that doesn't make sense.
- **Runtime errors** - using a variable that doesn't exist, mixing incompatible types, dividing by `0`, or calling a function that doesn't exist (or with the wrong number of inputs).

`HR` is a separate tool that reviews your code **without running it** and leaves passive-aggressive sticky notes. Right now it flags:

- Blocks you opened but never closed.
- A closer (`circle back` / `end meeting`) that has nothing to close.
- Variables you created but never used.
- `transition`-ing a variable you never created.

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
> (`transition count to leverage count with 1`) - there is no bare `leverage` statement.

---

## 🛠️ Project Layout & Development

```
src/synergyscript/
├── lexer.py         # The Recruiter - tokenizer
├── parser.py        # The Middle Manager - AST builder
├── interpreter.py   # The Intern - tree-walking evaluator
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

## 🔎 A Note on How This Was Built

This project was built with significant help from AI (Claude). I worked as a web developer early in my career, but that was a long time ago, and I'll happily admit those skills have gotten rusty in the years since. SynergyScript is a for-fun project — an excuse to build a small interpreted language around a running joke about corporate jargon — not a polished, production-grade tool, and definitely not one you should run anything important on.

Being straight about where it stands: the part I've put the most care into is the **spec** - the language reference above is meant to be precise enough to actually build from. The implementation behind it is still a work in progress; several stages are scaffolded with the heavy lifting yet to be filled in, so today it's more "designed" than "finished."

What I've leaned on so far has mostly been hands-on:

- Writing the example `.corp` programs in `scripts/` and reasoning through, by hand, how they *should* behave under the spec
- A pytest suite that encodes the intended behavior (stages not yet built are marked `xfail`, so the suite stays honest as the language fills in)

That leaves plenty I'd genuinely welcome a second set of eyes on:

- Correctness of the lexer / parser / interpreter against the grammar in §5 - especially the fiddly bits like longest-match tokenization and the `take … offline by …` circumfix
- Gaps or ambiguities in the spec itself - places where two readings are possible and I only picked one
- Edge cases I haven't thought to test (odd whitespace, deeply nested blocks, scoping corners)
- Code quality & idiomatic patterns - places where this isn't the modern, idiomatic way to do things in Python

Issues and PRs are genuinely welcome - including blunt "this is bad practice, here's why" feedback. I'm here to learn.

## 🤝 Contributing

Please ensure all pull requests are approved by at least three managers and align with our core values. Do not push directly to main; that is a career-limiting move.

## 📄 License

MIT.
