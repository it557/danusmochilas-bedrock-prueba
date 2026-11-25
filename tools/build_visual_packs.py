"""Build the held models and inventory marker from the project's original art."""
from copy import deepcopy
from pathlib import Path
import json
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "packs"

def load_pack(name):
    with ZipFile(PACKS / name) as archive:
        return {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}

def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()

def write_pack(name, files):
    with ZipFile(PACKS / name, "w") as archive:
        for path, data in sorted(files.items()):
            archive.writestr(ZipInfo(path), data, compress_type=ZIP_DEFLATED)

def update_manifest(files, version, description):
    manifest = json.loads(files["manifest.json"])
    manifest["header"]["version"] = version
    manifest["header"]["description"] = description
    for module in manifest["modules"]:
        module["version"] = version
    files["manifest.json"] = encode(manifest)

def build_held():
    files = load_pack("DanusMochilas-iconos-EXPERIMENTAL.mcpack")
    back = load_pack("DanusMochilas-3D-EXPERIMENTAL.mcpack")
    update_manifest(files, [0, 3, 0], "Iconos y modelos de mano para DanusMochilas")
    mapping = json.loads((ROOT / "custom_mappings" / "danus-iconos.json").read_text(encoding="utf-8-sig"))
    for tier, entry in enumerate(mapping["items"]["minecraft:brown_dye"], 1):
        source = json.loads(back[f"models/entity/back_tier{tier}.geo.json"])
        geometry = source["minecraft:geometry"][0]
        geometry_id = f"geometry.danusmochilas.hand_tier{tier}"
        geometry["description"]["identifier"] = geometry_id
        cubes = deepcopy(next(bone["cubes"] for bone in geometry["bones"] if "cubes" in bone))
        minimum = [min(cube["origin"][axis] for cube in cubes) for axis in range(3)]
        maximum = [max(cube["origin"][axis] + cube["size"][axis] for cube in cubes) for axis in range(3)]
        center = [(lo + hi) / 2 for lo, hi in zip(minimum, maximum)]
        for cube in cubes:
            cube["origin"] = [round(value - center[axis], 4) for axis, value in enumerate(cube["origin"])]
        geometry["bones"] = [
            {"name": "grip", "pivot": [0, 0, 0], "binding": "query.item_slot_to_bone_name(context.item_slot)"},
            {"name": "bag", "parent": "grip", "pivot": [0, 0, 0], "cubes": cubes},
        ]
        files[f"models/entity/hand_tier{tier}.geo.json"] = encode(source)
        texture = f"textures/danusmochilas/hand_tier{tier}"
        files[texture + ".png"] = back[f"textures/models/armor/danus_tier{tier}.png"]
        identifier = entry["bedrock_identifier"]
        desc = {
            "identifier": identifier,
            "item": {identifier: "query.is_owner_identifier_any('minecraft:player')"},
            "materials": {"default": "entity_alphatest", "enchanted": "entity_alphatest_glint"},
            "textures": {"default": texture, "enchanted": "textures/misc/enchanted_item_glint"},
            "geometry": {"default": geometry_id},
            "animations": {"first_person": "animation.danusmochilas.hand.first_person", "third_person": "animation.danusmochilas.hand.third_person"},
            "scripts": {"animate": [{"first_person": "context.is_first_person == 1.0"}, {"third_person": "context.is_first_person == 0.0"}]},
            "render_controllers": ["controller.render.item_default"],
        }
        files[f"attachables/hand_tier{tier}.json"] = encode({"format_version": "1.20.30", "minecraft:attachable": {"description": desc}})
    animations = {
        "animation.danusmochilas.hand.first_person": {"loop": True, "bones": {"bag": {"rotation": [10, -25, -15], "position": [0, 0, -2], "scale": 0.76}}},
        "animation.danusmochilas.hand.third_person": {"loop": True, "bones": {"bag": {"rotation": [0, 0, 0], "scale": 0.65}}},
    }
    files["animations/danusmochilas.hand.animation.json"] = encode({"format_version": "1.8.0", "animations": animations})
    write_pack("DanusMochilas-Mano-3D-CANDIDATO.mcpack", files)

def build_marker():
    files = load_pack("DanusMochilas-Casilla-Bedrock-EXPERIMENTAL.mcpack")
    update_manifest(files, [0, 2, 2], "Marco amarillo de la mochila para inventarios clasico y tactil")
    legacy = json.loads(files.pop("ui/ui_common.json"))
    classic_marker = legacy["inventory_panel"]["modifications"][0]["value"][0]
    # The first cell is four 18px columns left of center and 57px above
    # the hotbar center. The hotbar center is 14px above the root bottom.
    classic_marker["danus_slot_marker"].update(layer=8, offset=[-72, -71])
    files["ui/inventory_screen.json"] = encode({
        "namespace": "crafting",
        "player_inventory@common.root_panel": {
            "modifications": [{"array_name": "controls", "operation": "insert_back", "value": [classic_marker]}],
        },
    })
    pocket_marker = deepcopy(classic_marker)
    pocket_marker["danus_slot_marker"].update(anchor_from="top_left", anchor_to="top_left", offset=[0, 0])
    files["ui/inventory_screen_pocket.json"] = encode({
        "namespace": "crafting_pocket",
        "survival_inventory_grid@crafting.scroll_grid_panel": {
            "modifications": [{"array_name": "controls", "operation": "insert_back", "value": [pocket_marker]}],
        },
    })
    write_pack("DanusMochilas-Casilla-CANDIDATO.mcpack", files)

def build_back():
    files = load_pack("DanusMochilas-3D-EXPERIMENTAL.mcpack")
    previous = json.loads(files["manifest.json"])["header"]["version"]
    update_manifest(files, [previous[0], previous[1], previous[2] + 1], "Mochila posterior alineada con el torso")
    for tier in range(1, 5):
        path = f"models/entity/back_tier{tier}.geo.json"
        model = json.loads(files[path])
        geometry = model["minecraft:geometry"][0]
        body, backpack = geometry["bones"]
        body["pivot"] = [0, 24, 0]
        backpack.pop("binding", None)
        backpack["pivot"] = [0, 24, 0]
        cubes = backpack["cubes"]
        bottom = min(c["origin"][1] for c in cubes)
        top = max(c["origin"][1] + c["size"][1] for c in cubes)
        front = max(c["origin"][2] + c["size"][2] for c in cubes)
        # Player torso spans y=12..24. Its back is positive Z. The Java
        # pocket faces negative Z, so turn both horizontal axes 180 degrees.
        scale = min(0.85, 10.5 / (top - bottom))
        for cube in cubes:
            x, y, z = cube["origin"]
            width, height, depth = cube["size"]
            cube["origin"] = [round((-x-width)*scale, 4),
                              round(12.5+(y-bottom)*scale, 4),
                              round(2.6+(front-z-depth)*scale, 4)]
            cube["size"] = [round(value*scale, 4) for value in (width, height, depth)]
            faces = cube["uv"]
            for a, b in (("north", "south"), ("west", "east")):
                if a in faces and b in faces:
                    faces[a], faces[b] = faces[b], faces[a]
            for direction in ("up", "down"):
                if direction in faces:
                    face = faces[direction]
                    face["uv"] = [a+b for a,b in zip(face["uv"], face["uv_size"])]
                    face["uv_size"] = [-value for value in face["uv_size"]]
        assert all(c["origin"][2] >= 2.6 and 12 <= c["origin"][1] <= 24
                   and c["origin"][1] + c["size"][1] <= 24 for c in cubes)
        files[path] = encode(model)
    write_pack("DanusMochilas-Espalda-CANDIDATO.mcpack", files)

if __name__ == "__main__":
    build_held()
    build_marker()
    build_back()
