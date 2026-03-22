from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / 'dist'
BUNDLE_ROOT = DIST_DIR / 'smart-tourist-safety-web-mvp'
ZIP_PATH = DIST_DIR / 'smart-tourist-safety-web-mvp.zip'

INCLUDE = [
    ROOT / 'README.md',
    ROOT / 'PROJECT-TYPE.md',
    ROOT / 'backend',
    ROOT / 'docs',
    ROOT / 'NEEDTOCHANGE.md',
]

EXCLUDE_NAMES = {
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    '.DS_Store',
}
EXCLUDE_SUFFIXES = {'.pyc', '.pyo'}


def ignore_filter(_dir: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in EXCLUDE_NAMES:
            ignored.add(name)
        elif any(name.endswith(suffix) for suffix in EXCLUDE_SUFFIXES):
            ignored.add(name)
    return ignored


def copy_item(source: Path, target_root: Path) -> None:
    destination = target_root / source.name
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore_filter)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_bundle() -> Path:
    if BUNDLE_ROOT.exists():
        shutil.rmtree(BUNDLE_ROOT)
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)

    for item in INCLUDE:
        copy_item(item, BUNDLE_ROOT)

    with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(BUNDLE_ROOT.rglob('*')):
            if path.is_dir():
                continue
            archive.write(path, path.relative_to(DIST_DIR))

    return ZIP_PATH


if __name__ == '__main__':
    zip_path = build_bundle()
    print(zip_path)
