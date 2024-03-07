import bpy
RHO = 1.32471795724474602596090885447809734073
edge_lengths = [1, 2, 2, 3, 4, 5, 7, 9, 12, 16, 21, 28, 37, 49]
roundeds = [0,0,0,0,0,0,0,0, 1, 2, 2, 3, 4, 5]
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

def add_text(location, content, scale, color="black"):
    font_curve = bpy.data.curves.new(type="FONT", name="objectSize")
    font_curve.body = content
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    obj.scale.x = scale * 0.6
    obj.scale.y = scale * 0.8
    obj.location = location
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'CENTER'
    obj.location.y = location[1] - .05 * scale
    obj.active_material = bpy.data.materials[color]    
    bpy.context.scene.collection.objects.link(obj)

# these directions correspond to up and right, down and right, 
# down and left, and left and up
clockwise_from_left = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
clockwise_from_top = [(1, -1), (-1, -1), (-1, 1),(1, 1)]
clockwise_from_right = [(-1, -1), (-1, 1),(1, 1), (1, -1)]
counter_clockwise_from_left = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
counter_clockwise_from_top = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
directions = clockwise_from_left
# these positions start in the center and 
# spiral outwardly in a clockwise direction
origin = (0.0, 0, 0.0)
factor = .02
border_size = .01

def calculate_positions(start_position=origin, 
                        sizes=edge_lengths, 
                        directions=counter_clockwise_from_top):
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

center = ((max_x + min_x) / 2, (max_y + min_y) / 2, 0)

spiral_width = max_x - min_x
spiral_height = max_y - min_y

def create_spiral_squares(sizes=edge_lengths):
    positions = calculate_positions()
    for i in range(8, 14):
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
            scale=sizes[i] * factor * .75
            )
        base_rho = '1.0'
        if i < 13:
            base_rho = "0." + (12-i)*"0" + "1"
        add_text(
            location=(positions[i][0], 
                      positions[i][1] - sizes[i] * factor * .35, 
                      0.001),
            content=base_rho,
            scale=sizes[i] * factor * .2
            )


def rounded_integers():
    positions = calculate_positions()
    print(len(positions))
    print(positions)
    for i in range(8,14):
        if (i == 0):
            location=(positions[i][0] + roundeds[i] * factor,
                      positions[i][1], 0.001)
        else:
            if i % 2 == 0:
                location=(positions[4+i -1][0], positions[4+i][1], 0.001)
            else:
                location=(positions[4 + i][0], positions[4+i-1][1], 0.001)
        add_text(location=location,
            content= str(roundeds[i]),
            scale=edge_lengths[i] * factor * .60,
            color="white")
        location = (location[0],
                    location[1] - (roundeds[i] * factor * 1.4),
                    location[2])
        add_text(location=location,
            content= "1" + (i-5)*"0",
            scale=edge_lengths[i] * factor * .15,
            color="white")
    
def add_background():
    obj = bpy.ops.mesh.primitive_plane_add(
            size = 1, #edge_lengths[-1] * factor,
            location = center)

    bpy.context.active_object.scale[0] = spiral_width
    bpy.context.active_object.scale[1] = spiral_height
    
    bpy.context.active_object.name = "background"
    bpy.context.active_object.active_material = bpy.data.materials["green"]    
    
def add_camera():
    bpy.ops.object.camera_add(
        location=(center[0], center[1] + .35, 3.5), 
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
    bpy.context.scene.render.resolution_y = 4500 #6000


def main():
    set_resolution()
    add_camera()
    add_light()
    add_background()
    create_spiral_squares()
    rounded_integers()
    # print(calculate_positions())

if __name__ == "__main__":
    main()
