# radiant-rho.py

# This is code for generating an image file

# The image illustrates the proportionality built into the plastic ratio.

import bpy
RHO = 1.3246324717957244746

# Several lists are required:
#     The edge length of the squares, 
#     the center positions of each square
#     the color of each square,
#     the cyclic series of directions between squares,
    
edge_lengths = [1, 2, 2, 3, 4, 5, 7, 9, 12, 16, 21, 28, 37, 49]
                                                                                                                                                            
four_hundreds = [100, 75, 57, 43, 32, 25, 18, 14, 11, 7, 7, 4, 3, 4]

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
#origin = (0.0, 0, 0.0)
origin = (0.1254, -0.1853, 0.0)

factor = .012
border_size = .01
spiral_height = factor * sum(edge_lengths[-3:])
spiral_width = factor * sum(edge_lengths[-2:])
def calculate_positions(start_position=origin, 
                        sizes=edge_lengths, 
                        directions=clockwise_from_top):
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
# print(calculate_positions())

def create_spiral_squares(sizes=edge_lengths):
    positions = calculate_positions()
    for i in range(0, 14):
        # add a square plane, scaled to size
        # the default size of a plane is one meter 
        # largest square to be 28 centimeters
        bpy.ops.mesh.primitive_plane_add(
            size=sizes[i] * factor, 
            location=(positions[i][0], positions[i][1], 0.0001))
        bpy.context.active_object.name = "square-" + str(i)
        bpy.context.active_object.active_material = bpy.data.materials["black"]    
        #bpy.context.scene.collection.objects.link(obj)
        bpy.ops.mesh.primitive_plane_add(
            size=factor * sizes[i] - border_size,
            # size=sizes[i] * factor * 0.9, 
            location=(positions[i][0], positions[i][1], 0.0002))
        bpy.context.active_object.name = "square-" + str(i) + "-mask"
        bpy.context.active_object.active_material = bpy.data.materials["white"]    
        #bpy.context.scene.collection.objects.link(obj)
    
        #create_text_object('100')
        
        create_label(
            location=(positions[i][0], positions[i][1], 0.001),
            content= str(edge_lengths[i]),
            # content= str(four_hundreds[-i]),
            scale=sizes[i] * factor
            )
        

def add_background():
    location = origin
    obj = bpy.ops.mesh.primitive_plane_add(
            size = 1, #edge_lengths[-1] * factor,
            location = (0, 0, -0.001))

    bpy.context.active_object.scale[0] = spiral_width
    bpy.context.active_object.scale[1] = spiral_height
    bpy.context.active_object.name = "background"
    bpy.context.active_object.active_material = bpy.data.materials["green"]    
    #
    # bpy.context.scene.collection.objects.link(obj)
    
# create a sequence of squares along a diagonal
# add labels to the squares indicating size
def create_label(location, content, scale):
    font_curve = bpy.data.curves.new(type="FONT", name="objectSize")
    font_curve.body = content
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    obj.scale.x = scale * 0.8
    obj.scale.y = scale * 0.8
    obj.location = location
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'CENTER'
    obj.location.y = location[1] - .05 * scale
    # obj.location.y = location[1] - scale / 2.3
    # obj.location.z = location[2]
    obj.active_material = bpy.data.materials["black"]    
    bpy.context.scene.collection.objects.link(obj)


def add_rho_camera():
    bpy.ops.object.camera_add(
        location=(0, 0, 2.2), 
        rotation=(0, 0, 0),
        scale=(1, 1, 1))

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
    bpy.context.scene.render.resolution_y = 6000

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


def create_color_plane():
    bpy.ops.mesh.primitive_plane_add()
    plane = active_object()
    plane.scale.y *= 0.2
    plane.data.materials.append(black)
    return plane

def main():
    set_resolution()
    add_rho_camera()
    add_light()
    add_background()
    create_spiral_squares()
    # print(calculate_positions())

if __name__ == "__main__":
    main()
