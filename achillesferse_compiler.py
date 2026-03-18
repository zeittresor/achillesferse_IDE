from __future__ import annotations

import argparse
import ast
import json
import shlex
from pathlib import Path
from typing import Any


class ParseError(Exception):
    pass


def parse_value(text: str) -> Any:
    lower = text.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        return ast.literal_eval(text)
    except Exception:
        return text


def strip_comments(line: str) -> str:
    if "#" not in line:
        return line.rstrip()
    parts = line.split("#", 1)
    if parts[0].count('"') % 2 == 0 and parts[0].count("'") % 2 == 0:
        return parts[0].rstrip()
    return line.rstrip()


def parse_header_args(text: str) -> dict[str, Any]:
    tokens = shlex.split(text, posix=True)
    return parse_kv_tokens(tokens)


def parse_kv_tokens(tokens: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for token in tokens:
        if "=" not in token:
            raise ParseError(f"Expected key=value token, got: {token}")
        key, value = token.split("=", 1)
        out[key] = parse_value(value)
    return out


def parse_program(source: str) -> dict[str, Any]:
    raw_lines = [strip_comments(line) for line in source.splitlines()]
    lines = [line for line in raw_lines]
    index = 0

    program = {
        "app": {},
        "vars": {},
        "widgets": [],
        "bindings": [],
        "functions": {},
        "on_start": [],
        "on_tick": None,
    }

    def skip_blanks(idx):
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        return idx

    def parse_block(idx: int, end_tokens: set[str] | None = None):
        if end_tokens is None:
            end_tokens = {"END"}
        statements = []
        idx = skip_blanks(idx)
        while idx < len(lines):
            line = lines[idx].strip()
            if not line:
                idx += 1
                continue
            upper = line.upper()
            if any(upper == tok or upper.startswith(tok + " ") for tok in end_tokens):
                break

            if upper.startswith("SET "):
                rest = line[4:]
                if "=" not in rest:
                    raise ParseError(f"SET requires '=': {line}")
                name, expr = rest.split("=", 1)
                statements.append({"type": "set", "name": name.strip(), "expr": expr.strip()})
                idx += 1
            elif upper.startswith("UISET "):
                rest = line[6:]
                widget, expr = rest.split(",", 1)
                statements.append({"type": "uiset", "widget": widget.strip(), "expr": expr.strip()})
                idx += 1
            elif upper.startswith("APPEND "):
                rest = line[7:]
                widget, expr = rest.split(",", 1)
                statements.append({"type": "append", "widget": widget.strip(), "expr": expr.strip()})
                idx += 1
            elif upper.startswith("CLEAR "):
                statements.append({"type": "clear", "widget": line[6:].strip()})
                idx += 1
            elif upper.startswith("FOCUS "):
                statements.append({"type": "focus", "widget": line[6:].strip()})
                idx += 1
            elif upper.startswith("CANVAS_CLEAR "):
                statements.append({"type": "canvas_clear", "widget": line[13:].strip()})
                idx += 1
            elif upper.startswith("DRAW_STARFIELD "):
                rest = line[15:]
                widget, expr = rest.split(",", 1)
                statements.append({"type": "draw_starfield", "widget": widget.strip(), "expr": expr.strip()})
                idx += 1
            elif upper.startswith("CALL "):
                statements.append({"type": "expr", "expr": line[5:].strip()})
                idx += 1
            elif upper.startswith("EXPR "):
                statements.append({"type": "expr", "expr": line[5:].strip()})
                idx += 1
            elif upper == "RETURN":
                statements.append({"type": "return"})
                idx += 1
            elif upper.startswith("RETURN "):
                statements.append({"type": "return", "expr": line[7:].strip()})
                idx += 1
            elif upper.startswith("IF "):
                cond = line[3:].strip()
                idx += 1
                then_body, idx = parse_block(idx, {"ELIF", "ELSE", "END"})
                elifs = []
                else_body = []
                while idx < len(lines):
                    token = lines[idx].strip()
                    token_upper = token.upper()
                    if token_upper.startswith("ELIF "):
                        econd = token[5:].strip()
                        idx += 1
                        body, idx = parse_block(idx, {"ELIF", "ELSE", "END"})
                        elifs.append({"cond": econd, "body": body})
                    elif token_upper == "ELSE":
                        idx += 1
                        else_body, idx = parse_block(idx, {"END"})
                        break
                    else:
                        break
                if idx >= len(lines) or lines[idx].strip().upper() != "END":
                    raise ParseError("IF block missing END")
                idx += 1
                statements.append({"type": "if", "cond": cond, "then": then_body, "elifs": elifs, "else": else_body})
            elif upper.startswith("FOR "):
                if " IN " not in upper:
                    raise ParseError(f"FOR syntax is 'FOR name IN expr': {line}")
                rest = line[4:]
                split_pos = upper.index(" IN ")
                name = rest[:split_pos]
                expr = rest[split_pos + 4 :]
                idx += 1
                body, idx = parse_block(idx, {"END"})
                if idx >= len(lines) or lines[idx].strip().upper() != "END":
                    raise ParseError("FOR block missing END")
                idx += 1
                statements.append({"type": "for", "name": name.strip(), "iterable": expr.strip(), "body": body})
            elif upper.startswith("WHILE "):
                cond = line[6:].strip()
                idx += 1
                body, idx = parse_block(idx, {"END"})
                if idx >= len(lines) or lines[idx].strip().upper() != "END":
                    raise ParseError("WHILE block missing END")
                idx += 1
                statements.append({"type": "while", "cond": cond, "body": body})
            else:
                raise ParseError(f"Unknown statement: {line}")
            idx = skip_blanks(idx)
        return statements, idx

    while index < len(lines):
        index = skip_blanks(index)
        if index >= len(lines):
            break
        line = lines[index].strip()
        upper = line.upper()
        if upper.startswith("APP "):
            program["app"] = parse_header_args(line[4:])
            index += 1
        elif upper.startswith("VAR "):
            rest = line[4:]
            if "=" not in rest:
                raise ParseError(f"VAR requires '=': {line}")
            name, expr = rest.split("=", 1)
            program["vars"][name.strip()] = expr.strip()
            index += 1
        elif upper.startswith("WIDGET "):
            parts = shlex.split(line[7:], posix=True)
            if len(parts) < 2:
                raise ParseError(f"WIDGET requires name and type: {line}")
            name = parts[0]
            wtype = parts[1]
            options = parse_kv_tokens(parts[2:]) if len(parts) > 2 else {}
            program["widgets"].append({"name": name, "type": wtype, "options": options})
            index += 1
        elif upper.startswith("BIND "):
            parts = shlex.split(line[5:], posix=True)
            if len(parts) != 3:
                raise ParseError("BIND syntax: BIND widget event action")
            program["bindings"].append({"widget": parts[0], "event": parts[1], "action": parts[2]})
            index += 1
        elif upper.startswith("FUNC "):
            header = line[5:].strip()
            if "(" in header and header.endswith(")"):
                name = header[: header.index("(")].strip()
                params = [p.strip() for p in header[header.index("(") + 1 : -1].split(",") if p.strip()]
            else:
                name = header
                params = []
            index += 1
            body, index = parse_block(index, {"END"})
            if index >= len(lines) or lines[index].strip().upper() != "END":
                raise ParseError(f"Function {name} missing END")
            index += 1
            program["functions"][name] = {"params": params, "body": body}
        elif upper == "ON_START":
            index += 1
            body, index = parse_block(index, {"END"})
            if index >= len(lines) or lines[index].strip().upper() != "END":
                raise ParseError("ON_START missing END")
            index += 1
            program["on_start"] = body
        elif upper.startswith("ON_TICK "):
            ms = int(line[8:].strip())
            index += 1
            body, index = parse_block(index, {"END"})
            if index >= len(lines) or lines[index].strip().upper() != "END":
                raise ParseError("ON_TICK missing END")
            index += 1
            program["on_tick"] = {"ms": ms, "body": body}
        else:
            raise ParseError(f"Unknown top-level construct: {line}")
    return program


def compile_source_to_python(source: str) -> str:
    program = parse_program(source)
    json_blob = json.dumps(program, indent=2, ensure_ascii=False)
    return f'''from __future__ import annotations

import json
import sys
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()
_SEARCH_DIRS = [
    _THIS_FILE.parent,
    _THIS_FILE.parent.parent,
    _THIS_FILE.parent.parent / "src",
]
for _candidate in _SEARCH_DIRS:
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

from achillesferse_runtime import AchillesferseApp

PROGRAM = json.loads(r"""{json_blob}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
'''


def compile_file(source_path: str | Path, output_path: str | Path):
    source_text = Path(source_path).read_text(encoding="utf-8")
    py_code = compile_source_to_python(source_text)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(py_code, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Achillesferse compiler")
    parser.add_argument("source", help="Path to the .af file")
    parser.add_argument("output", nargs="?", help="Path to the generated .py file")
    parser.add_argument("--dump-json", action="store_true", help="Print parsed JSON instead of generating Python")
    args = parser.parse_args()

    source_text = Path(args.source).read_text(encoding="utf-8")
    program = parse_program(source_text)
    if args.dump_json:
        print(json.dumps(program, indent=2, ensure_ascii=False))
        return

    output = Path(args.output) if args.output else Path(args.source).with_suffix(".py")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(compile_source_to_python(source_text), encoding="utf-8")
    print(f"Compiled {args.source} -> {output}")


if __name__ == "__main__":
    main()
