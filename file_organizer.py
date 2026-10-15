"""Project 2: File organizer.

Sorts the files in a folder into subfolders (Images, Documents, ...) by extension.
Runs as a dry run by default, so nothing moves until you pass --apply.

Usage:
    python file_organizer.py ~/Downloads            # preview
    python file_organizer.py ~/Downloads --apply    # actually move files
"""

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".key"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".ipynb", ".c", ".cpp"},
}


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Other"


def unique_destination(dest: Path) -> Path:
    """Avoid overwriting: report.pdf -> report (1).pdf -> report (2).pdf"""
    if not dest.exists():
        return dest
    n = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({n}){dest.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def organize(folder: Path, apply: bool) -> None:
    if not folder.is_dir():
        raise SystemExit(f"Not a folder: {folder}")

    moved = 0
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        target_dir = folder / category_for(item)
        dest = unique_destination(target_dir / item.name)
        print(f"{item.name}  ->  {dest.relative_to(folder)}")
        if apply:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
        moved += 1

    verb = "Moved" if apply else "Would move"
    print(f"\n{verb} {moved} file(s)." + ("" if apply else " Re-run with --apply to do it."))


def main():
    parser = argparse.ArgumentParser(description="Sort files into folders by type")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--apply", action="store_true", help="actually move files")
    args = parser.parse_args()
    organize(args.folder.expanduser(), args.apply)


if __name__ == "__main__":
    main()
