# radiant-rho.py

# This is code for generating an image file

# The image illustrates the proportionality built into the plastic ratio.

import bpy
RHO = 1.32471795724474602596090885447809734073

# Several lists are required:
#     The edge length of the squares, 
#     the center positions of each square
#     the color of each square,
#     the cyclic series of directions between squares,
    
edge_lengths = [1, 2, 2, 3, 4, 5, 7, 9, 12, 16, 21, 28, 37, 49]

labels_100 = ['.03', '.03', '.05', '.06', '.08', '.11', '.14', '.18', '.25', '.32', '.43', '.57', '.75', '1.00']


int_200 = [5, 7, 9, 12, 16, 21, 28, 37, 49, 65, 86, 114, 151, 200]

BLACK = (0.0, 0.0, 0.0, 1.0)
RED = (1.0, 0.0, 0.0, 1.0)
GREEN = (0.0, 1.0, 0.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)
WHITE = (1.0, 1.0, 1.0, 1.0)

colors = [BLACK, RED, GREEN, BLUE, WHITE]
color_names = ["black", "red", "green", "blue", "white"]
# create colored materials
for i in range(0, len(colors)):
    mat = bpy.data.materials.new(f"{color_names[i]}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"]    \
        .default_value = colors[i]     

# these directions correspond to up and right down and right 
# down and left and left and up
clockwise_from_left = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
clockwise_from_top = [(1, -1), (-1, -1), (-1, 1),(1, 1)]
clockwise_from_right = [(-1, -1), (-1, 1),(1, 1), (1, -1)]
counter_clockwise_from_left = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
counter_clockwise_from_top = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
directions = clockwise_from_left
# these positions start in the center and 
# spiral outwardly in a clockwise direction
origin = (0.0, 0, 0.0)
#origin = (0.1254, -0.1853, 0.0)

factor = .02
border_size = .01

def calculate_positions(start_position=origin, 
                        sizes=edge_lengths, 
                        directions=counter_clockwise_from_left):
    positions = [start_position]
    # The next position is obtained by summing the current and next edge lengths, 
    # dividing by two, multiplying  length times the x and y of the next direction;
    # and adding that shift to the previous position

    for i in range(1, 14):
        previous_position = positions[i-1]
        shift_length = factor * (sizes[i-1]+sizes[i]) / 2
        shift_x = shift_length * (directions[(i+2) % 4][0])
        shift_y = shift_length * (directions[(i+2) % 4][1])
        position = (previous_position[0] + shift_x, 
                    previous_position[1] + shift_y,
                    0.0)
        positions.append(position)        
    return (positions)


# get the value the highest x in the lowest x also the y values
# get the index number for that value to then obtain size in edge_lengths
positions = calculate_positions()
xs, ys, zs = zip(*positions)
max_x = max(xs) + factor * (edge_lengths[xs.index(max(xs))]) / 2
min_x = min(xs) - factor * (edge_lengths[xs.index(min(xs))]) / 2
max_y = max(ys) + factor * (edge_lengths[ys.index(max(ys))]) / 2
min_y = min(ys) - factor * (edge_lengths[ys.index(min(ys))]) / 2
origin = ((max_x + min_x) / 2, (max_y + min_y) / 2, 0)


spiral_width = max_x - min_x
spiral_height = max_y - min_y

header_position_x =  -.303 #spiral_width / 2
header_position_y =  max_y * 1.35


def create_header():
    add_text(location=(header_position_x, header_position_y, 0.001),
            content="We're number .011 !",
            # content="\"Rho\", the radiant number.",
            scale=0.35)
    add_text(location=(header_position_x, header_position_y * .82, 0.001),
            # content="Use base-rho binary, and you can " +
            #         "be number .00111, too!",
            content="Get radiant with base - 1.324717....",
            scale=0.18)
    add_heading_background()
    
    
def add_rho(location=(header_position_x, header_position_y * .79, 0), 
            scale=0.18):
    font_curve = bpy.data.curves.new(type="FONT", name="rho")
    font_curve.body = "r=1.324717..." # 𝞺 ⍴ 𝛒 "
    obj = bpy.data.objects.new(name="Greek Symbol", object_data=font_curve)
    fnt = bpy.data.fonts.load('/usr/share/fonts/ATHENS1X.TTF')
    obj.data.font = fnt
    obj.scale.x = scale
    obj.scale.y = scale
    obj.location.x = location[0]
    obj.location.y = location[1]

    obj.location.z = 0.06 
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'CENTER'
    obj.active_material = bpy.data.materials["black"]    
    bpy.context.scene.collection.objects.link(obj)



def create_spiral_squares(sizes=edge_lengths):
    positions = calculate_positions()
    for i in range(0, 14):
        # add a square plane, scaled to size
        # the default size of a plane is one meter 
        # largest square to be 28 centimeters
        border_size = i * 0.001 + 0.002
        bpy.ops.mesh.primitive_plane_add(
            size=sizes[i] * factor, 
            location=(positions[i][0], positions[i][1], 0.0001))
        bpy.context.active_object.name = "square-" + str(i)
        bpy.context.active_object.active_material = bpy.data.materials["black"]    
        bpy.ops.mesh.primitive_plane_add(
            size=factor * sizes[i] - border_size,
            location=(positions[i][0], positions[i][1], 0.0002))
        bpy.context.active_object.name = "square-" + str(i) + "-mask"
        bpy.context.active_object.active_material = bpy.data.materials["white"]    
    
        add_text(
            location=(positions[i][0], positions[i][1], 0.001),
            content= labels_100[i],
            # content= str(edge_lengths[i]),
            scale=sizes[i] * factor * .75
            )
        

def add_background():
    obj = bpy.ops.mesh.primitive_plane_add(
            size = 1, #edge_lengths[-1] * factor,
            location = origin)

    bpy.context.active_object.scale[0] = spiral_width
    bpy.context.active_object.scale[1] = spiral_height
    
    bpy.context.active_object.name = "background"
    bpy.context.active_object.active_material = bpy.data.materials["green"]    
    
def add_heading_background():
    obj = bpy.ops.mesh.primitive_plane_add(
            size = 1, 
            location = origin)

    bpy.context.active_object.location.y = max_y + (spiral_width - spiral_height) / 2
    bpy.context.active_object.scale[0] = spiral_width
    bpy.context.active_object.scale[1] = spiral_width - spiral_height

    
    bpy.context.active_object.name = "heading_background"
    bpy.context.active_object.active_material = bpy.data.materials["white"]
    
# add labels to the squares indicating size
def add_text(location, content, scale):
    font_curve = bpy.data.curves.new(type="FONT", name="objectSize")
    font_curve.body = content
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    obj.scale.x = scale * 0.6
    obj.scale.y = scale * 0.8
    obj.location = location
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'CENTER'
    obj.location.y = location[1] - .05 * scale
    # obj.location.y = location[1] - scale / 2.3
    # obj.location.z = location[2]
    obj.active_material = bpy.data.materials["black"]    
    bpy.context.scene.collection.objects.link(obj)


def add_camera():
    bpy.ops.object.camera_add(
        # location=(min_x / 2, min_y / 2, 4.4), 
        location=(origin[0], origin[1] + .5, 4.4), 
        rotation=(0, 0, 0),
        scale=(1, 1, 1))
    
'''
better_living_through_better_language_
better_language_through_better_numbers_
better_numbers_through_better_bases

I'm all about the base
the mighty morphic number base
we're number 0.011
a number for better living
a number for Ignatius
there are 1.011 types of people in the world
'''

def add_light():
    bpy.ops.object.light_add(
        type='AREA', 
        location=(3, 0, 4))
    bpy.context.object.data.energy = 300
    bpy.ops.object.light_add(
        type='AREA', 
        location=(-3, 0, 4))
    bpy.context.object.data.energy = 300

def set_resolution():
    bpy.context.scene.render.resolution_x = 4500
    bpy.context.scene.render.resolution_y = 4500 #6000

def create_text_object(text):
    bpy.ops.object.text_add()

    text_obj = bpy.context.active_object
    text_obj.scale *= 0.49
    text_obj.data.body = text

    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", 
                              center="MEDIAN")
    text_obj.location = 0, 0, 0
    text_obj.data.extrude = 0.01
    text_obj.data.fill_mode = "BOTH"
    # text_obj.data.bevel_depth = 0.002
    text_obj.data.materials.append(bpy.data.materials["black"])
    
    return text_obj

def main():
    create_header()
    set_resolution()
    add_camera()
    add_light()
    add_background()
    create_spiral_squares()
    #add_rho()
    # print(calculate_positions())

if __name__ == "__main__":
    main()
