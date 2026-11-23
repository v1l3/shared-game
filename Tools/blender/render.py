"""Headless render of the current scene (still or animation).

Usage:
  blender -b scene.blend --python Tools/blender/render.py -- --out /path/to/renders/ [--anim] [--samples 128] [--engine CYCLES|BLENDER_EEVEE_NEXT]
On JanPC (via `ssh janpc`), point --out at a local folder, then scp results back.
Renders do not go in git: put them in the shared cloud folder.
"""
import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--anim", action="store_true")
    p.add_argument("--samples", type=int, default=None)
    p.add_argument("--engine", default=None)
    p.add_argument("--res", type=int, default=100, help="resolution percentage")
    return p.parse_args(argv)


def main():
    args = parse_args()
    scene = bpy.context.scene
    if args.engine:
        scene.render.engine = args.engine
    if args.samples and scene.render.engine == "CYCLES":
        scene.cycles.samples = args.samples
    scene.render.resolution_percentage = args.res
    os.makedirs(args.out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(bpy.data.filepath))[0] or "render"
    scene.render.filepath = os.path.join(args.out, stem + ("_####" if args.anim else ""))
    bpy.ops.render.render(animation=args.anim, write_still=not args.anim)
    print(f"rendered to {args.out}")


main()
