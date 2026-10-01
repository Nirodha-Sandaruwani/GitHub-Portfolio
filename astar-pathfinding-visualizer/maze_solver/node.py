import pygame
from constants import NODE_SIZE, PADDING
from node_type import NodeType

class Node:
    def __init__(self, row, col, node_type, offset_y=0):
        self.row = row
        self.col = col
        self.offset_y = offset_y
        self.node_type = node_type

    def is_wall(self):
        return self.node_type is NodeType.WALL

    def is_start(self):
        return self.node_type is NodeType.START

    def is_end(self):
        return self.node_type is NodeType.END

    def is_empty(self):
        return self.node_type is NodeType.EMPTY

    def is_visited(self):
        return self.node_type is NodeType.VISITED

    def is_path(self):
        return self.node_type is NodeType.PATH

    def visits(self):
        if not self.is_empty():
            return
        self.update_type(NodeType.VISITED)

    def update_type(self, new_type):
        self.node_type = new_type

    def draw(self, window):
        color = self.node_type.value
        x = self.col * NODE_SIZE + PADDING
        y = self.row * NODE_SIZE + PADDING + self.offset_y
        pygame.draw.rect(window, color, (x, y, NODE_SIZE, NODE_SIZE))

    def __lt__(self, other):
        return True
