#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml"]
# ///
"""Validate an Agent Skill directory against the agentskills.io specification.

Checks hard spec rules (errors) and best-practice guidance (warnings), then
prints a JSON report to stdout. Exits non-zero if any hard rule is violated.

Spec: https://agentskills.io/specification
Progressive disclosure: https://agentskills.io/specification#progressive-disclosure

Usage:
  python3 scripts/validate_skill.py <path-to-skill-directory>
  python3 scripts/validate_skill.py --help

Exit codes:
  0  no errors (warnings may still be present)
  1  one or more spec violations (errors) found
  2  usage error / skill directory or SKILL.md not found
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_BODY_LINES = 500
SPEC = "https://agentskills.io/specification"

KNOWN_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


def split_frontmatter(text):
    """Return (frontmatter_str, body_str). Frontmatter is None if absent."""
    if not text.startswith("---"):
        return None, text
    # Frontmatter is delimited by a leading '---' and a following '---' line.
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            fm = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1 :])
            return fm, body
    return None, text


def parse_frontmatter(fm):
    """Parse frontmatter. Prefer PyYAML; fall back to a minimal parser.

    The fallback handles the fields this validator inspects: top-level scalars,
    block scalars (>, |, >-, |-), quoted strings, and one level of mapping
    (for `metadata`). It is intentionally conservative.
    """
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(fm)
        return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return _minimal_parse(fm)


def _minimal_parse(fm):
    data = {}
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        # Only handle top-level (non-indented) keys.
        if raw[:1].isspace():
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest in (">", "|", ">-", "|-", ">+", "|+"):
            block, i = _collect_block(lines, i + 1)
            joiner = " " if rest.startswith(">") else "\n"
            data[key] = joiner.join(line.strip() for line in block).strip()
            continue
        if rest == "" and _next_is_indented(lines, i + 1):
            # Nested mapping (e.g. metadata). Collect indented key: value pairs.
            nested, i = _collect_mapping(lines, i + 1)
            data[key] = nested
            continue
        data[key] = _strip_quotes(rest)
        i += 1
    return data


def _next_is_indented(lines, idx):
    return idx < len(lines) and lines[idx][:1].isspace() and lines[idx].strip()


def _collect_block(lines, idx):
    block = []
    while idx < len(lines):
        line = lines[idx]
        if line.strip() and not line[:1].isspace():
            break
        block.append(line)
        idx += 1
    return block, idx


def _collect_mapping(lines, idx):
    nested = {}
    while idx < len(lines):
        line = lines[idx]
        if line.strip() and not line[:1].isspace():
            break
        if line.strip():
            m = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
            if m:
                nested[m.group(1)] = _strip_quotes(m.group(2).strip())
        idx += 1
    return nested, idx


def _strip_quotes(s):
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


def find_referenced_files(body):
    """Return relative paths referenced in markdown links or code fences."""
    refs = set()
    for m in re.finditer(r"\]\(([^)]+)\)", body):
        refs.add(m.group(1))
    for m in re.finditer(r"(?:references|assets|scripts)/[\w./-]+", body):
        refs.add(m.group(0))
    cleaned = set()
    for r in refs:
        r = r.split("#")[0].strip()
        if not r or "://" in r or r.startswith("mailto:"):
            continue
        if not r.startswith(("references/", "assets/", "scripts/")):
            continue
        cleaned.add(r)
    return sorted(cleaned)


def validate(skill_dir):
    errors = []
    warnings = []
    info = {}

    skill_dir = os.path.abspath(skill_dir)
    if not os.path.isdir(skill_dir):
        return {
            "errors": [f"Not a directory: {skill_dir}"],
            "warnings": [],
            "info": {},
            "usage_error": True,
        }

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        errors.append(f"Missing SKILL.md at skill root ({SPEC})")
        return {"errors": errors, "warnings": warnings, "info": info, "usage_error": True}

    with open(skill_md, "r", encoding="utf-8") as fh:
        text = fh.read()

    fm, body = split_frontmatter(text)
    if fm is None:
        errors.append(f"SKILL.md has no YAML frontmatter delimited by '---' lines ({SPEC})")
        return {"errors": errors, "warnings": warnings, "info": info}

    data = parse_frontmatter(fm)

    # name
    name = data.get("name")
    dir_name = os.path.basename(skill_dir)
    if not name:
        errors.append("Frontmatter is missing required field: name")
    else:
        info["name"] = name
        if len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} chars; max is {MAX_NAME}")
        if not NAME_RE.match(name):
            errors.append(
                "name must be lowercase a-z/0-9/hyphens, not start/end with a hyphen, "
                "and contain no consecutive hyphens"
            )
        if name != dir_name:
            errors.append(f"name '{name}' must match parent directory name '{dir_name}'")

    # description
    desc = data.get("description")
    if not desc or not str(desc).strip():
        errors.append("Frontmatter is missing required non-empty field: description")
    else:
        dlen = len(str(desc))
        info["description_length"] = dlen
        if dlen > MAX_DESCRIPTION:
            errors.append(f"description is {dlen} chars; max is {MAX_DESCRIPTION}")

    # compatibility
    compat = data.get("compatibility")
    if compat is not None:
        clen = len(str(compat))
        if clen == 0 or clen > MAX_COMPATIBILITY:
            errors.append(f"compatibility must be 1-{MAX_COMPATIBILITY} chars; got {clen}")

    # metadata
    meta = data.get("metadata")
    if meta is not None and not isinstance(meta, dict):
        warnings.append("metadata should be a key-value mapping")

    # unknown keys
    for key in data:
        if key not in KNOWN_KEYS:
            warnings.append(
                f"Unknown frontmatter key '{key}' (not in the spec; clients may ignore it)"
            )

    # body length (progressive disclosure)
    body_lines = len(body.splitlines())
    info["body_lines"] = body_lines
    if body_lines > MAX_BODY_LINES:
        warnings.append(
            f"SKILL.md body is {body_lines} lines; keep under {MAX_BODY_LINES} and move "
            "detail to references/ (progressive disclosure)"
        )

    # referenced files exist
    missing = []
    for ref in find_referenced_files(body):
        if not os.path.exists(os.path.join(skill_dir, ref)):
            missing.append(ref)
    if missing:
        warnings.append("Referenced files not found: " + ", ".join(missing))

    # undocumented scripts
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        for entry in sorted(os.listdir(scripts_dir)):
            full = os.path.join(scripts_dir, entry)
            if os.path.isfile(full) and f"scripts/{entry}" not in body:
                warnings.append(
                    f"Script 'scripts/{entry}' is not mentioned in SKILL.md; "
                    "list bundled scripts so the agent knows they exist"
                )

    return {"errors": errors, "warnings": warnings, "info": info}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate an Agent Skill directory against the agentskills.io spec.",
        epilog="Spec: https://agentskills.io/specification",
    )
    parser.add_argument("skill_dir", help="Path to the skill directory containing SKILL.md")
    args = parser.parse_args(argv)

    if not os.path.exists(args.skill_dir):
        # Diagnostics go to stderr; stdout is reserved for the validation report.
        print(
            json.dumps({"errors": [f"Path not found: {args.skill_dir}"]}, indent=2),
            file=sys.stderr,
        )
        return 2

    result = validate(args.skill_dir)
    usage_error = result.pop("usage_error", False)
    result["passed"] = len(result["errors"]) == 0
    # A usage error (bad path / missing SKILL.md) is a diagnostic, not a report.
    print(json.dumps(result, indent=2), file=sys.stderr if usage_error else sys.stdout)
    return 2 if usage_error else (0 if result["passed"] else 1)


if __name__ == "__main__":
    sys.exit(main())
