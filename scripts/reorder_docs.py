#!/usr/bin/env python3
"""
reorder_docs.py — Resolve doc file conflicts after git merge.

File naming convention uses HHMM timestamp so files created at different
times are naturally unique. This script handles the rare edge case where
two developers create a file at the exact same minute, producing a collision.

For sprint plan files (sprint-{N}-{slug}.md), also resolves duplicate sprint
numbers that can occur when two developers work on the same project
simultaneously.

Uses git first-commit time as tiebreaker for same-timestamp files.

Usage:
    python scripts/reorder_docs.py              # scan from cwd
    python scripts/reorder_docs.py [target-dir]
    python scripts/reorder_docs.py --dry-run    # preview, no rename
    python scripts/reorder_docs.py --scope be   # limit to one subdir

File patterns handled:
    docs/changelog/{YYYYMMDD}-{HHMM}-changelog-{slug}.md
    docs/test/{YYYYMMDD}-{HHMM}-test-{slug}.md
    docs/test/{YYYYMMDD}-{HHMM}-testlog-{slug}.md
    docs/plan/sprint-{N}-{slug}.md
"""

import argparse
import os
import re
import subprocess
import sys
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DATED_RE  = re.compile(r'^(\d{8})-(\d{4})-(changelog|test|testlog)-(.+)\.md$')
SPRINT_RE = re.compile(r'^sprint-(\d+)-(.+)\.md$')


# ── Git time ──────────────────────────────────────────────────────────────────

def _git_first_commit_time(path: Path) -> Optional[float]:
    try:
        r = subprocess.run(
            ['git', 'log', '--follow', '--format=%at', '--', str(path)],
            capture_output=True, text=True, timeout=10,
        )
        times = [int(t) for t in r.stdout.strip().splitlines() if t.strip()]
        return float(min(times)) if times else None
    except Exception:
        return None


def _sort_key(path: Path) -> float:
    """Sort key: (date, time) from filename, then git time as tiebreaker."""
    m = DATED_RE.match(path.name)
    if m:
        date, time = m.group(1), m.group(2)
        base = float(f"{date}{time}")
        git_t = _git_first_commit_time(path) or path.stat().st_mtime
        return base + git_t * 1e-16  # tiny offset keeps timestamp order primary
    return _git_first_commit_time(path) or path.stat().st_mtime


# ── Discovery ─────────────────────────────────────────────────────────────────

def _find_doc_dirs(root: Path, scope: Optional[str]) -> List[Path]:
    search = (root / scope) if scope else root
    found: List[Path] = []
    for sub in ('changelog', 'test', 'plan'):
        found.extend(d for d in search.rglob(f'docs/{sub}') if d.is_dir())
    return found


# ── Conflict detection & rename computation ───────────────────────────────────

def _compute_dated_renames(doc_dir: Path) -> List[Tuple[Path, Path]]:
    """
    Find files with identical YYYYMMDD-HHMM-type. For each collision group,
    keep the earliest git-commit file at the original timestamp and bump
    later files by +1 minute until no collision remains.
    """
    # Group by (date, time, type)
    groups: Dict[Tuple[str, str, str], List[Path]] = defaultdict(list)
    for f in doc_dir.iterdir():
        if not f.is_file() or f.suffix != '.md':
            continue
        m = DATED_RE.match(f.name)
        if m:
            groups[(m.group(1), m.group(2), m.group(3))].append(f)

    renames: List[Tuple[Path, Path]] = []
    # Collect all new names to detect cross-group collisions after bump
    taken = {f.name for f in doc_dir.iterdir() if f.is_file()}

    for (date, time, type_), files in groups.items():
        if len(files) == 1:
            continue  # no conflict
        sorted_files = sorted(files, key=_sort_key)
        # First file keeps its name; subsequent files get time+1, +2, ...
        for i, path in enumerate(sorted_files[1:], start=1):
            m = DATED_RE.match(path.name)
            assert m
            slug = m.group(4)
            h, mn = int(time[:2]), int(time[2:])
            for delta in range(1, 60):
                total = h * 60 + mn + i + delta - 1
                new_h, new_mn = divmod(total % (24 * 60), 60)
                new_time = f"{new_h:02d}{new_mn:02d}"
                new_name = f"{date}-{new_time}-{type_}-{slug}.md"
                if new_name not in taken:
                    taken.add(new_name)
                    taken.discard(path.name)
                    renames.append((path, path.parent / new_name))
                    break
    return renames


def _compute_sprint_renames(doc_dir: Path) -> List[Tuple[Path, Path]]:
    """Only renumber when duplicate sprint Ns exist after a merge."""
    files: List[Path] = []
    for f in doc_dir.iterdir():
        if f.is_file() and f.suffix == '.md' and SPRINT_RE.match(f.name):
            files.append(f)

    if not files:
        return []

    ns = [int(SPRINT_RE.match(f.name).group(1)) for f in files]  # type: ignore[union-attr]
    if len(ns) == len(set(ns)):
        return []  # no duplicates

    start_n = min(ns)
    sorted_files = sorted(files, key=_sort_key)
    renames: List[Tuple[Path, Path]] = []
    for new_n, path in enumerate(sorted_files, start=start_n):
        m = SPRINT_RE.match(path.name)
        assert m
        old_n, slug = int(m.group(1)), m.group(2)
        if old_n != new_n:
            renames.append((path, path.parent / f'sprint-{new_n}-{slug}.md'))
    return renames


# ── Apply ─────────────────────────────────────────────────────────────────────

def _apply(renames: List[Tuple[Path, Path]], dry_run: bool) -> None:
    if dry_run:
        for old, new in renames:
            print(f'  [dry]  {old.name}  →  {new.name}')
        return
    staged: List[Tuple[Path, Path]] = []
    for old, new in renames:
        tmp = old.parent / f'_reorder_{uuid.uuid4().hex[:8]}_{old.name}'
        old.rename(tmp)
        staged.append((tmp, new))
        print(f'  {old.name}  →  {new.name}')
    for tmp, new in staged:
        tmp.rename(new)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument('target', nargs='?', default=None)
    ap.add_argument('--dry-run', '-n', action='store_true', help='Preview without renaming')
    ap.add_argument('--scope', default=None, metavar='SUBDIR')
    args = ap.parse_args()

    root = Path(args.target).resolve() if args.target else Path(os.getcwd()).resolve()
    if not root.exists():
        print(f'Error: {root} not found')
        sys.exit(1)

    doc_dirs = _find_doc_dirs(root, args.scope)
    if not doc_dirs:
        print('No docs/changelog|test|plan directories found.')
        return

    total = 0
    for doc_dir in sorted(doc_dirs):
        renames = (
            _compute_sprint_renames(doc_dir)
            if doc_dir.name == 'plan'
            else _compute_dated_renames(doc_dir)
        )
        if not renames:
            continue
        print(f'\n[{doc_dir.relative_to(root)}]')
        _apply(renames, args.dry_run)
        total += len(renames)

    if total == 0:
        print('No conflicts found — all files are uniquely named.')
    elif args.dry_run:
        print(f'\n{total} file(s) would be renamed. Remove --dry-run to apply.')
    else:
        print(f'\n{total} file(s) renamed.')


if __name__ == '__main__':
    main()
