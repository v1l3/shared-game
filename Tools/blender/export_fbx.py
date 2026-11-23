"""Export each top-level mesh in a .blend to its own Unreal-ready FBX.

Usage:
  blender -b Art/Source/Crate/SM_Crate.blend --python Tools/blender/export_fbx.py -- --out Art/Export/Crate
Options:
  --out DIR        output folder (default: next to the .blend)
  --selected       export only selected objects
Collision (UCX_*) and LOD (*_LOD#) objects are exported together with their base mesh.
"""
import argparse
import os
import re
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=None)
    p.add_argument("--selected", action="store_true")
    return p.parse_args(argv)


def base_name(name):
    name = re.sub(r"^UCX_", "", name)
    name = re.sub(r"_\d{2}$", "", name)
    return re.sub(r"_LOD\d+$", "", name)


def main():
    args = parse_args()
    out = args.out or os.path.dirname(bpy.data.filepath)
    os.makedirs(out, exist_ok=True)

    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if args.selected:
        objs = [o for o in objs if o.select_get()]

    groups = {}
    for o in objs:
        groups.setdefault(base_name(o.name), []).append(o)

    for name, members in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in members:
            o.select_set(True)
        path = os.path.join(out, f"{name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=path,
            use_selection=True,
            object_types={"MESH"},
            apply_scale_options="FBX_SCALE_ALL",
            axis_forward="-Y",
            axis_up="Z",
            mesh_smooth_type="FACE",
            use_mesh_modifiers=True,
            add_leaf_bones=False,
            embed_textures=False,
        )
        print(f"exported {path} ({len(members)} objects)")


main()
