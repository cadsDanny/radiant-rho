# radiant_spirals.py
import bpy
RHO = 1.32471795724474602596090885447809734073
    
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

origin = (0.0, 0, 0.0)    


def create_spiral_data(rounds=2, magnitude=1.324717, direction=(1, 1),
                  start_angle=0, radius=1, steps=60, center=(0,0,0)):
    step_magnitude = (magnitude - 1) / steps
    spiral_data = [radius + center[0], center[1]]
    for step in range(steps * rounds):
        current_radius = step_magnitude * radius
        
    


def main():
    print(color_names)


if __name__ == "__main__":
    main()
