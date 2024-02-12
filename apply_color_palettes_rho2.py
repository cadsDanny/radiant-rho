import json
import math
import pathlib
import random
import time

import bpy
def hex_color_str_to_rgba(hex_color: str):
    # remove the leading '#' symbol if present
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    assert len(hex_color) == 6, "RRGGBB is the supported hex color format"

    # extracting the Red color component - RRxxxx
    red = int(hex_color[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255
    linear_red = convert_srgb_to_linear_rgb(srgb_red)

    # extracting the Green color component - xxGGxx
    green = int(hex_color[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255
    linear_green = convert_srgb_to_linear_rgb(srgb_green)

    # extracting the Blue color component - xxxxBB
    blue = int(hex_color[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255
    linear_blue = convert_srgb_to_linear_rgb(srgb_blue)

    alpha = 1.0
    return tuple([linear_red, linear_green, linear_blue, alpha])


def convert_srgb_to_linear_rgb(srgb_color_component):
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)

    return linear_color_component


def setup_scene(palette_index):
    project_name = "rho_colors"

    render_dir_path = pathlib.Path.home() / "blender/rho" / project_name / f"rho_scene_{palette_index}.png"
    render_dir_path.parent.mkdir(parents=True, exist_ok=True)

    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = str(render_dir_path)


def prepare_and_render_scene(palette_index):
    setup_scene(palette_index)
    apply_colors()
    bpy.ops.render.render(write_still=True)


def render_all_palettes(palettes):
    bpy.context.scene.render.engine = "BLENDER_EEVEE"

    start_time = time.time()
    for palette_index, palette in enumerate(palettes):
        prepare_and_render_scene(palette_index)

        # remove the following line to render all the palettes
        break

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


def load_rho_palettes():    
    path = pathlib.Path.home() / "blender/rho/palettes/" / "100_five_color_palettes.json"
    with open(path, "r") as color_palette:
        color_palettes = json.loads(color_palette.read())
    return color_palettes
    
def apply_colors():

    colors = { 'white' : hex_color_str_to_rgba("ffffff"),
               'black' : hex_color_str_to_rgba("000000")
               }

    palettes = load_rho_palettes()

    for palette_index, palette in enumerate(palettes):
        palette = [hex_color_str_to_rgba(hex_color) for hex_color in palette]
        break

    shades=[0.666, 0.333]
    
    color_shades = []
    for color in palette:
        color_shades.append(color)
        for shading in shades:
            color_shades.append((
                        color[0] * shading, 
                        color[1] * shading, 
                        color[2] * shading, 
                        1.0))
    #print(f"length: {len(palette)}")
    #print(f"length: {len(color_shades)}")
        

    set_id = "100"
    palette_index = 0
    
    shades = ['original','shaded','darkened']
    
    # set as 
    rectangle_color_index = 0
    
    for color in color_shades:
        print(color)
    
    squares_colors = color_shades.copy()[3:]
    
    for color in squares_colors:
        print(color)
    
    for position in range(0,4):
        for shade in shades:
    
            #print(squares_colors[shades.index(shade)*4 + position])
            mat = bpy.data.materials.new(f"{set_id}_{palette_index}_{position}_{shade}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"]    \
                .default_value = squares_colors[position*3 + shades.index(shade)] 
                
            obj = bpy.data.objects[f"Square_irho{ shades.index(shade)*4 + position + 2 }"]
            obj.active_material = mat
            print(obj.name, mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"]    \
                .default_value[0:3])
     
                
    # rho ratio rectangle upon which successively smaller squares are inlaid
    
def main():
    """
    The main entry point of the script.
    """
    palettes = load_rho_palettes()
    
    palette_index = None
    if palette_index is not None:
        bpy.context.scene.render.engine = "CYCLES"
        selected_palette = palettes[palette_index]
        prepare_and_render_scene(selected_palette, palette_index)
        return

    render_all_palettes(palettes)


if __name__ == "__main__":
    main()

            #print(squares_colors[shades.index(shade)*4 + position])
mat = bpy.data.materials.new(f"{color_name}")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"]    \
    .default_value = color_value 
    
obj = bpy.data.objects[f"Square_irho{ shades.index(shade)*4 + position + 2 }"]
obj.active_material = mat
print(obj.name, mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"]    \
    .default_value[0:3])
\








