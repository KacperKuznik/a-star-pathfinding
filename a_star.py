class Node:
    def __init__(self, board: list, start_pos: tuple, end_pos: tuple, parent=None):
        self.board = board
        self.pos = start_pos
        self.parent = parent
        self.g = 0
        if parent:
            self.g = parent.g + 1
        self.h = abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])
        self.f = self.g + self.h
        self.board[start_pos[0]][start_pos[1]] = self.f

    def __eq__(self, pos):
        return self.pos == pos

    def mark(self):
        self.board[self.pos[0]][self.pos[1]] = "W"


class A_Star:
    def __init__(self, board: list, start_pos: tuple, end_pos: tuple):
        self.board = board
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_node = Node(self.board, start_pos, end_pos)
        self.open_nodes = [self.current_node]
        self.closed_nodes = []

    def create_nodes(self, parent: Node):
        pos = parent.pos
        nodes = [Node(self.board, (row, col), self.end_pos, parent) for row in range(pos[0] - 1, pos[0] + 2) for col in range(pos[1] - 1, pos[1] + 2)
                 if 0 <= row < len(self.board)
                 and 0 <= col < len(self.board)
                 and (row, col) not in self.open_nodes + self.closed_nodes
                 and self.board[row][col] != "X"
                 ]
        return nodes

    def backtrace(self):
        path = []
        while self.current_node.parent != None:
            path.append(self.current_node.pos)
            self.current_node.mark()
            self.current_node = self.current_node.parent
        return path

    def run(self):
        while len(self.open_nodes) > 0:
            self.do_single_step()
        else:
            print("not found")
    
    def do_single_step(self):
        if len(self.open_nodes) > 0:
            self.current_node = min(self.open_nodes, key=lambda x: x.f)
            if self.current_node.pos == self.end_pos:
                return "Found", self.backtrace()
            self.closed_nodes.append(self.current_node)
            nodes = self.create_nodes(self.current_node)
            self.open_nodes += nodes
            self.open_nodes.remove(self.current_node)
            return "Searching", nodes
        else:
            return "Route not found", []

    def display_board(self):
        for row in self.board:
            print(*row)
