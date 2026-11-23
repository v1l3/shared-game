"""Check asset file names against the conventions in CLAUDE.md.

Usage:
  python3 Tools/blender/check_names.py Art/Export [more paths...]
Exits 1 if any name is wrong. Runs without Blender.
"""
import re
import sys
from pathlib import Path

PREFIXES = ("SM_", "SK_", "M_", "MI_", "T_", "A_", "BP_", "S_", "SC_")
TEXTURE_SUFFIXES = ("_D", "_N", "_ORM", "_E")
TEXTURE_EXT = {".png", ".tga", ".exr", ".tif", ".tiff", ".jpg", ".jpeg"}
CHECK_EXT = TEXTURE_EXT | {".fbx", ".obj", ".glb", ".gltf", ".wav"}
NAME_RE = re.compile(r"^[A-Z]{1,3}_[A-Z][A-Za-z0-9]*(_[A-Za-z0-9]+)*$")


def problems(path):
    stem, ext = path.stem, path.suffix.lower()
    out = []
    if not stem.startswith(PREFIXES):
        out.append(f"missing prefix ({', '.join(PREFIXES)})")
    if not NAME_RE.match(stem):
        out.append("use Prefix_PascalCase_Variant, no spaces or dashes")
    if ext in TEXTURE_EXT:
        if not stem.startswith("T_"):
            out.append("textures must start with T_")
        if not stem.endswith(TEXTURE_SUFFIXES):
            out.append(f"texture needs a suffix ({', '.join(TEXTURE_SUFFIXES)})")
    return out


def main(paths):
    bad = 0
    for root in paths or ["Art/Export"]:
        root = Path(root)
        files = [root] if root.is_file() else root.rglob("*")
        for f in files:
            if f.is_file() and f.suffix.lower() in CHECK_EXT:
                for p in problems(f):
                    print(f"{f}: {p}")
                    bad += 1
    print("OK" if not bad else f"{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
