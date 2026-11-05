"""Step 2: export a game-ready FBX from Blender.

Runs INSIDE Blender (Scripting tab, or through the Blender MCP server).
Name your parts <Asset>_<Part> (e.g. TreasureChest_Wood) and build the model
with its base center at the world origin, 1 Blender unit = 1 stud.
"""
from pathlib import Path

import bpy

ASSET_NAME = "TreasureChest"   # change to your asset's name
OUT_DIR = bpy.app.tempdir      # or a folder of your choice

MAX_TRIANGLES = 20_000  # Roblox rejects meshes above this


def export_asset(asset_name: str, out_dir: str) -> Path:
    """Apply transforms, check the triangle budget and export <asset_name>_* objects as FBX."""
    parts = [
        obj for obj in bpy.data.objects
        if obj.type == "MESH" and obj.name.startswith(f"{asset_name}_")
    ]
    if not parts:
        raise ValueError(f"No mesh objects named {asset_name}_*")

    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]

    # Bake location, rotation and scale into the mesh so nothing imports rotated or stretched.
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Count triangles after modifiers, the same way the game will see them.
    depsgraph = bpy.context.evaluated_depsgraph_get()
    triangles = 0
    for obj in parts:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        evaluated.to_mesh_clear()
    if triangles > MAX_TRIANGLES:
        raise ValueError(f"{triangles} triangles is over the {MAX_TRIANGLES} limit")

    out_path = Path(out_dir) / f"{asset_name}.fbx"
    bpy.ops.export_scene.fbx(
        filepath=str(out_path),
        use_selection=True,
        object_types={"MESH"},
        global_scale=0.01,  # Blender writes FBX in cm; this keeps 1 Blender unit = 1 stud
    )
    print(f"Exported {out_path} ({len(parts)} parts, {triangles} triangles)")
    return out_path


export_asset(ASSET_NAME, OUT_DIR)
