#!/usr/bin/env python3
"""Deterministic checks for the knowledge/ tree. Exit non-zero on any finding.

Checks: orphan pages, index gaps, stale derived pages, broken links, log size.
Frontmatter here is always flat `key: value` YAML (no lists/nesting), so it's
parsed with a simple line scan rather than a YAML dependency.
"""
import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = REPO_ROOT / "knowledge"
LOG_ROTATE_THRESHOLD = 500

findings = []


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text, body = parts[1], parts[2]
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, body


def domain_dirs():
    if not KNOWLEDGE.is_dir():
        return []
    return [
        d
        for d in KNOWLEDGE.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    ]


def check_orphans_and_index_gaps():
    main_md = KNOWLEDGE / "main.md"
    main_text = main_md.read_text() if main_md.exists() else ""

    for domain in domain_dirs():
        if domain.name not in main_text:
            findings.append(f"index gap: domain '{domain.name}' not listed in main.md")

        index_md = domain / "index.md"
        index_text = index_md.read_text() if index_md.exists() else ""

        for sub in ("self", "derived"):
            subdir = domain / sub
            if not subdir.is_dir():
                continue
            for page in subdir.glob("*.md"):
                rel = f"{sub}/{page.name}"
                if rel not in index_text and page.stem not in index_text:
                    findings.append(
                        f"orphan page: {domain.name}/{rel} not referenced in {domain.name}/index.md"
                    )


def check_stale_derived():
    for domain in domain_dirs():
        derived_dir = domain / "derived"
        if not derived_dir.is_dir():
            continue
        for page in derived_dir.glob("*.md"):
            fm, _ = parse_frontmatter(page)
            content_hash = fm.get("content_hash")
            source_ref = fm.get("source_ref")
            if not content_hash or not source_ref:
                continue
            source_path = REPO_ROOT / source_ref
            if not source_path.exists():
                findings.append(
                    f"broken link: {domain.name}/derived/{page.name} source_ref '{source_ref}' does not exist"
                )
                continue
            actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
            if actual_hash != content_hash:
                findings.append(
                    f"stale derived: {domain.name}/derived/{page.name} content_hash does not match {source_ref}"
                )


WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def check_broken_links():
    for domain in domain_dirs():
        for sub in ("self", "derived"):
            subdir = domain / sub
            if not subdir.is_dir():
                continue
            for page in subdir.glob("*.md"):
                fm, body = parse_frontmatter(page)
                for ref_key in ("source_ref", "source_refs"):
                    if ref_key in fm:
                        for ref in fm[ref_key].split(","):
                            ref = ref.strip()
                            if ref and not (REPO_ROOT / ref).exists():
                                findings.append(
                                    f"broken link: {domain.name}/{sub}/{page.name} {ref_key} '{ref}' does not exist"
                                )
                for target in WIKILINK_RE.findall(body):
                    target = target.strip()
                    found = any(
                        (domain / other / f"{target}.md").exists()
                        for other in ("self", "derived")
                    )
                    if not found:
                        findings.append(
                            f"broken link: {domain.name}/{sub}/{page.name} wikilink '[[{target}]]' does not resolve"
                        )


def check_log_size():
    for log_file in [KNOWLEDGE / "log.md"] + list(KNOWLEDGE.glob("log-*.md")):
        if not log_file.exists():
            continue
        entry_count = len(re.findall(r"^## \[", log_file.read_text(), re.MULTILINE))
        if entry_count > LOG_ROTATE_THRESHOLD:
            findings.append(
                f"log size: {log_file.relative_to(REPO_ROOT)} has {entry_count} entries "
                f"(> {LOG_ROTATE_THRESHOLD}) — rotate to log-YYYY.md"
            )


def main():
    check_orphans_and_index_gaps()
    check_stale_derived()
    check_broken_links()
    check_log_size()

    if findings:
        for f in findings:
            print(f)
        print(f"\n{len(findings)} finding(s).")
        return 1

    print("lint: clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
