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
                                                                                                                                                            

BLACK = (1.0, 0.0, 0.0, 1.0)
RED = (1.0, 0.0, 0.0, 1.0)
GREEN = (0.0, 1.0, 0.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)
WHITE = (1.0, 1.0, 1.0, 1.0)

colors = []

# these directions correspond to up and right down and right 
# down and left and left and up
directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

# these positions start in the center and 
# spiral outwardly in a clockwise direction
origin = (0.0, 0.0, 0.0)

factor = .1        
def calculate_positions(start_position=origin, sizes=edge_lengths, course=directions):
    positions = [start_position]
    # The next position is obtained by summing the current and next edge lengths, 
    # dividing by two, multiplying  length times the x and y of the next direction;
    # and adding that shift to the previous position

    for i in range(1, 14):
        previous_position = positions[i-1]
        shift_length = factor * (sizes[i-1]+sizes[i]) / 2
        shift_x = shift_length * (directions[i % 4][0])
        shift_y = shift_length * (directions[i % 4][1])
        position = (previous_position[0] + shift_x, 
                    previous_position[1] + shift_y,
                    0.0)
        positions.append(position)        
    return (positions)
# print(calculate_positions())

def create_squares(sizes=edge_lengths):
    positions = calculate_positions()
    for i in range(0, 14):
        # add a square plane, scaled to size
        # the default size of a plane is one meter 
        # largest square to be 28 centimeters
        bpy.ops.mesh.primitive_plane_add(
            size=sizes[i] * factor, 
            location=(positions[i][0], positions[i][1], 0.0001))

def main():
    create_squares()
    # print(calculate_positions())

if __name__ == "__main__":
    main()
