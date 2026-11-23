# shared-game

Shared Unreal + Blender game. See [CLAUDE.md](CLAUDE.md) for conventions and rules.

## Setup (once per machine)

### macOS (Mac Studio, MacBook Pro)
```sh
brew install git git-lfs
git lfs install
git clone https://github.com/v1l3/shared-game.git
cd shared-game
git lfs pull
```

### Windows (JanPC)
Install [Git for Windows](https://git-scm.com/download/win) (includes Git LFS), then in PowerShell:
```powershell
git lfs install
git clone https://github.com/v1l3/shared-game.git
cd shared-game
git lfs pull
```

Install the same Unreal Engine and Blender versions listed in `CLAUDE.md` on every machine.

## Day-to-day
```sh
git pull
git lfs locks                     # who is editing what
git lfs lock Art/Source/Crate/SM_Crate_A.blend
# ...edit, save...
git add -A && git commit -m "Crate: new bevels" && git push
git lfs unlock Art/Source/Crate/SM_Crate_A.blend
```
Binary files (`.uasset`, `.umap`, `.blend`, `.fbx`, textures, audio) are LFS-tracked and
**lockable**: they check out read-only until you lock them.

## Storage
GitHub's free plan includes about **1 GB of LFS storage and bandwidth**. Unreal projects grow
fast, so expect to buy a data pack, and keep renders and caches out of the repo
(`Saved/`, `Intermediate/`, `DerivedDataCache/` are already ignored).

## Tools
- `blender -b file.blend --python Tools/blender/export_fbx.py -- --out Art/Export/Crate`
- `blender -b file.blend --python Tools/blender/render.py -- --out /path/to/renders/`
- `python3 Tools/blender/check_names.py Art/Export` (no Blender needed)
- In Unreal: *Tools → Execute Python Script* → `Tools/unreal/batch_import.py`
