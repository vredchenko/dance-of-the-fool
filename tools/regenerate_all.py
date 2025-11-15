#!/usr/bin/env python3
"""
Regenerate all translation output formats.

This script runs all generation scripts to rebuild:
- Webui data (translation-data.json)
- PDF without uncertainties
- PDF with uncertainties
- EPUB without uncertainties
- EPUB with uncertainties
"""

import subprocess
import sys
from pathlib import Path


def run_script(script_name: str, args: list[str] = None) -> bool:
    """Run a Python script and return success status."""
    tools_dir = Path(__file__).parent
    script_path = tools_dir / script_name

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd[1:])}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, cwd=tools_dir.parent)

    if result.returncode != 0:
        print(f"\n❌ Failed: {script_name}", file=sys.stderr)
        return False

    print(f"\n✓ Completed: {script_name}")
    return True


def main():
    """Regenerate all translation outputs."""
    print("\n" + "="*60)
    print("REGENERATING ALL TRANSLATION FORMATS")
    print("="*60)

    tasks = [
        ("build-webui-data.py", [], "Webui data"),
        ("generate-pdf.py", ["--output", "dist/translation.pdf"], "PDF (no uncertainties)"),
        ("generate-pdf.py", ["--output", "dist/translation-with-notes.pdf", "--include-uncertainties"], "PDF (with uncertainties)"),
        ("generate-epub.py", ["--output", "dist/translation.epub"], "EPUB (no uncertainties)"),
        ("generate-epub.py", ["--output", "dist/translation-with-notes.epub", "--include-uncertainties"], "EPUB (with uncertainties)"),
    ]

    results = []

    for script, args, description in tasks:
        success = run_script(script, args)
        results.append((description, success))

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    all_success = True
    for description, success in results:
        status = "✓" if success else "❌"
        print(f"{status} {description}")
        if not success:
            all_success = False

    print("="*60)

    if all_success:
        print("\n✓ All formats regenerated successfully!\n")
        return 0
    else:
        print("\n❌ Some tasks failed. See output above for details.\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
