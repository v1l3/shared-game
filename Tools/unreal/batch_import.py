"""Batch-import FBX files and textures from Art/Export into the Unreal project.

Run in the Unreal editor (Python Editor Script Plugin enabled):
  Tools -> Execute Python Script -> Tools/unreal/batch_import.py
Art/Export/<Folder>/SM_Thing.fbx  ->  /Game/Art/<Folder>/SM_Thing
Edit SOURCE / DEST below if your layout differs.
"""
import os

import unreal

REPO = os.path.abspath(os.path.join(unreal.Paths.project_dir(), ".."))
SOURCE = os.path.join(REPO, "Art", "Export")
DEST = "/Game/Art"
TEXTURE_EXT = (".png", ".tga", ".exr", ".tif", ".tiff", ".jpg", ".jpeg")


def fbx_options():
    opts = unreal.FbxImportUI()
    opts.import_mesh = True
    opts.import_textures = False
    opts.import_materials = False
    opts.import_as_skeletal = False
    opts.static_mesh_import_data.import_uniform_scale = 1.0
    opts.static_mesh_import_data.combine_meshes = True
    opts.static_mesh_import_data.auto_generate_collision = False  # use UCX_ meshes
    opts.static_mesh_import_data.generate_lightmap_u_vs = True
    return opts


def make_task(path, dest):
    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = dest
    task.automated = True
    task.replace_existing = True
    task.save = True
    if path.lower().endswith(".fbx"):
        task.options = fbx_options()
    return task


def main():
    tasks = []
    for root, _, files in os.walk(SOURCE):
        rel = os.path.relpath(root, SOURCE).replace("\\", "/")
        dest = DEST if rel == "." else f"{DEST}/{rel}"
        for f in files:
            if f.lower().endswith((".fbx",) + TEXTURE_EXT):
                tasks.append(make_task(os.path.join(root, f), dest))
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    unreal.log(f"Imported {len(tasks)} file(s) from {SOURCE}")


main()
