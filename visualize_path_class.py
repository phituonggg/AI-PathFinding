from settings import *

class VisualizePath():
    def __init__(self, surface, start_node_x, start_node_y, path, path_coords):
        self.surface = surface
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.path = path
        self.path_coords = path_coords

    # For BFS and DFS mainly
    def get_path_coords(self):
        i = self.start_node_x
        j = self.start_node_y
        for move in self.path:
            if move == 'L':
                i -= 1
            elif move == 'R':
                i += 1
            elif move == 'U':
                j -= 1
            elif move == 'D':
                j += 1
            self.path_coords.append((i,j))

    def draw_path(self,COLOUR):
        
        for (x_pos, y_pos) in self.path_coords:
            pygame.draw.rect(self.surface, COLOUR, (x_pos*24 + 240, y_pos*24, 24, 24), 0)
    
    def get_list(self):
        return self.path_coords
    def list_len(self):
        return len(self.path_coords)