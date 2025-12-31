#!/usr/bin/env python3
import ast
import os
import sys
from pathlib import Path

# --------- helpers ---------
def safe(s: str) -> str:
    return (s or "").replace('"', "'")

def dotted_name(node):
    """Return dotted name for ast.Name / ast.Attribute chains."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return dotted_name(node.func)
    return ""

def const_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None

def first_str_arg(call: ast.Call):
    if call.args:
        s = const_str(call.args[0])
        if s is not None:
            return s
    return None

def get_keyword_str(call: ast.Call, key: str):
    for kw in call.keywords:
        if kw.arg == key:
            s = const_str(kw.value)
            if s is not None:
                return s
    return None

# --------- visitor ---------
class OrchestrationVisitor(ast.NodeVisitor):
    """
    Extract "external interactions" from Python scripts:
      - subprocess/os shell calls
      - requests HTTP calls
      - boto3 client calls (heuristic)
      - filesystem reads/writes
    """
    def __init__(self):
        self.events = []  # list of tuples (kind, label)
        self.boto_clients = set()  # variable names that look like boto3 clients

    def add(self, kind, label):
        self.events.append((kind, label))

    def visit_Assign(self, node: ast.Assign):
        # Detect boto3 clients: x = boto3.client("s3") or boto3.resource(...)
        try:
            if isinstance(node.value, ast.Call):
                fn = dotted_name(node.value.func)
                if fn in ("boto3.client", "boto3.resource"):
                    service = first_str_arg(node.value) or get_keyword_str(node.value, "service_name") or "aws"
                    # record target names
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            self.boto_clients.add(t.id)
                            self.add("aws", f"create {fn}({service}) as {t.id}")
        except Exception:
            pass
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        fn = dotted_name(node.func)

        # ---- shell / subprocess ----
        if fn in ("os.system",):
            cmd = first_str_arg(node) or "<command>"
            self.add("shell", f"os.system: {cmd}")
        elif fn in ("subprocess.run", "subprocess.call", "subprocess.check_call", "subprocess.check_output", "subprocess.Popen"):
            cmd = first_str_arg(node)
            if cmd is None and node.args:
                # could be list of args; just show placeholder
                cmd = "<subprocess args>"
            self.add("shell", f"{fn}: {cmd or '<command>'}")

        # ---- requests http ----
        elif fn.startswith("requests."):
            method = fn.split(".")[-1].upper()
            url = first_str_arg(node) or get_keyword_str(node, "url") or "<url>"
            self.add("http", f"{method} {url}")

        # ---- filesystem ----
        elif fn in ("open",):
            path = first_str_arg(node) or "<file>"
            mode = get_keyword_str(node, "mode") or (const_str(node.args[1]) if len(node.args) > 1 else None) or "r"
            self.add("fs", f"open({path}, mode={mode})")
        elif fn.endswith(".read_text") or fn.endswith(".read_bytes"):
            self.add("fs", f"{fn}()")
        elif fn.endswith(".write_text") or fn.endswith(".write_bytes"):
            self.add("fs", f"{fn}()")
        elif fn in ("pathlib.Path", "Path"):
            # not an interaction by itself
            pass

        # ---- boto3 client calls (heuristic): client.method(...) ----
        else:
            # if call is like <name>.<method>(...), and <name> is a boto client var
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                obj = node.func.value.id
                method = node.func.attr
                if obj in self.boto_clients:
                    self.add("aws", f"{obj}.{method}(...)")

        self.generic_visit(node)


def to_mermaid_sequence(title: str, events):
    lines = []
    lines.append("sequenceDiagram")
    lines.append("autonumber")
    lines.append("participant Script as " + safe(title))
    lines.append("participant FS as Filesystem")
    lines.append("participant Sh as Shell")
    lines.append("participant HTTP as HTTP")
    lines.append("participant AWS as AWS")
    lines.append("")

    if not events:
        lines.append("Note over Script: no external interactions detected")
        return "\n".join(lines)

    for kind, label in events:
        label = safe(label)
        if kind == "fs":
            lines.append(f"Script->>FS: {label}")
            lines.append("FS-->>Script: ok")
        elif kind == "shell":
            lines.append(f"Script->>Sh: {label}")
            lines.append("Sh-->>Script: exit status")
        elif kind == "http":
            lines.append(f"Script->>HTTP: {label}")
            lines.append("HTTP-->>Script: response")
        elif kind == "aws":
            lines.append(f"Script->>AWS: {label}")
            lines.append("AWS-->>Script: result")
        else:
            lines.append(f"Script->>Script: {label}")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print("usage: py_to_mermaid.py <input_dir_or_file> <out_dir>", file=sys.stderr)
        sys.exit(2)

    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    files = []
    if src.is_file():
        files = [src]
    else:
        files = sorted(src.rglob("*.py"))

    for p in files:
        try:
            code = p.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=str(p))
            v = OrchestrationVisitor()
            v.visit(tree)

            title = p.name
            mmd = to_mermaid_sequence(title, v.events)

            out = out_dir / (p.stem + ".mmd")
            out.write_text(mmd + "\n", encoding="utf-8")
            print(f"WROTE {out}")
        except Exception as e:
            print(f"SKIP {p}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()