""" rho_objects.py 
    creates in Blender a series of objects increasingly smaller in proportion to rho.
"""
import bpy

RHO = 1.3246324717957244746
CENTER = (0, 0, 0)
location = (0, 0, 0)
scale = (1, 1, 1)
# print(scale)


object_count = 4
start_location = (0,0)
start_size = 1
magnitude = 1/RHO
#direction = clockwise


d45 = (1, 1)
d135 = (-1, 1)
d225 = (-1, -1)
d315 = (1, -1) 

directions = [d45, d135, d225, d315]


# create a list of new positions for objects
def create_positions(object_count=8,
                     start_location=(0, 0),
                     start_size=1, 
                     magnitude=1/RHO,
                     directions=[(1, 1), (-1, 1), (-1,-1), (1, -1)]):
    # create initial position
    positions = [start_location]
    size = start_size
    for object in range(0, object_count - 1):
        direction = directions[object % 4]
        distance = (size + (size * magnitude)) / 2
        offset = ((distance * direction[0], distance * direction[1]))
        positions.append((positions[object][0] + offset[0], positions[object][1] + offset[1]))
        size = size * magnitude
    return positions
    
def create_integer_positions(object_count=8,
                     start_location=(0, 0),
                     edge_length=16, 
                     step=-1, # 1 for increase
                     directions=[(1, 1), (-1, 1), (-1,-1), (1, -1)]):
    # create initial position
    positions = [start_location]
    # create list of sizes
    index = padovan_list.index(edge_length)
    # size_list = 
    for i in range(0, object_count - 1):
        direction = directions[object % 4]
        distance = (edge_length + ()) / 2
        offset = ((distance * direction[0], distance * direction[1]))
        positions.append((positions[i][0] + offset[0], positions[i][1] + offset[1]))
        size = size * magnitude
    return positions


print(create_positions() [:])

'''
print(create_positions(edge_length=pow(RHO, -7), 
                       start_location=(0, 1),
                       magnitude = RHO)[:])
'''

# Create a list of integers in the padovan sequence
def list_padovan(elements=12):
    padovan=[1, 1, 1]
    for i in range(3, elements):
        padovan.append(padovan[-3]+padovan[-2])

    return padovan

padovan_list = list_padovan(30)
print(padovan_list)

def main():
    bpy.ops.mesh.primitive_cube_add(size=4)
    obj = bpy.context.active_object
    obj.location.z = 3
    obj.location.y = 3  
    obj.location.x = 3


# create a list of positions
if __name__ == "__main__":
    main()