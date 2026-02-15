import random
from enum import Enum

class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [1 for i in range(n)]

    def find(self, child):
        if self.parent[child] != child:
            self.parent[child] = self.find(self.parent[child])
        return self.parent[child]

    def union(self, i, j):
        root_1 = self.find(i)
        root_2 = self.find(j)
        if root_1 != root_2 :
            if self.rank[root_1] > self.rank[root_2]:
                self.parent[root_2] = root_1
            elif self.rank[root_1] < self.rank[root_2]:
                self.parent[root_1] = root_2
            else :
                self.parent[root_1] = root_2
                self.rank[root_2] += 1
            return True
        return False

class Kruskal_Maze:
    def __init__(self, height, width, entry = (0, 0), exit = (0, 0), seed = 42, output_filename = "maze.txt", cell_size = 42):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.output_filename = output_filename
        self.cell_size = cell_size
        self._rng = random.Random(seed)
        self.matrix_cells = None
        self.walls = []
        self.maze_walls = []
        self.pattern_walls = []
        self.pattern_cells = set()
        self.set_four_cells()
        self.set_two_cells()
        self.fill_walls()
    
    def set_four_cells(self):
        w = self.width
        h = self.height
        left_cells = (w - 7) // 2
        top_cells = (h - 5) // 2
        pattern_cells = self.pattern_cells
        for i in range(5):
            if i == 2:
                pattern_cells.add((top_cells + i) * w + left_cells)
                pattern_cells.add((top_cells + i) * w + left_cells + 1)
                pattern_cells.add((top_cells + i) * w + left_cells + 2)
            elif i > 2:
                pattern_cells.add((top_cells + i) * w + left_cells + 2)
            else:
                pattern_cells.add((top_cells + i) * w + left_cells)

    def set_two_cells(self):
        w = self.width
        h = self.height
        left_cells = (w - 7) // 2 + 4
        top_cells = (h - 5) // 2
        pattern_cells = self.pattern_cells
        for i in range(5):
            if i == 1:
                pattern_cells.add((top_cells + i) * w +  left_cells + 2)
            elif i == 3:
                pattern_cells.add((top_cells + i) * w + left_cells)
            else :
                pattern_cells.add((top_cells + i) * w + left_cells)
                pattern_cells.add((top_cells + i) * w + left_cells + 1)
                pattern_cells.add((top_cells + i) * w + left_cells + 2)


    def fill_walls(self):
        w = self.width
        h = self.height
        walls = self.walls
        pattern_cells = self.pattern_cells
        pattern_walls = self.pattern_walls
        for y in range(h):
            for x in range(w):
                index = y * w + x
                if x < w - 1:
                    if index in pattern_cells or index + 1 in pattern_cells:
                        pattern_walls.append((index, index + 1))
                    else:
                        walls.append((index, index + 1))
                if y < h - 1:
                    if index in pattern_cells or index + w in pattern_cells:
                        pattern_walls.append((index, index + w))
                    else:
                        walls.append((index, index + w))   

    def generate_perfect(self):
        self._rng.shuffle(self.walls)
        dsu = DSU(self.height * self.width)
        maze_walls = self.maze_walls
        maze_walls.clear()
        for wall in self.walls:
            cell1, cell2 = wall
            if dsu.find(cell1) != dsu.find(cell2):
                dsu.union(cell1, cell2)
            else:
                maze_walls.append(wall)
        self.fill_matrix_cells()

    def generate_regular(self):
        self._rng.shuffle(self.walls)
        dsu = DSU(self.height * self.width)
        maze_walls = self.maze_walls
        maze_walls.clear()
        for wall in self.walls:
            cell1, cell2 = wall
            if dsu.find(cell1) != dsu.find(cell2):
                dsu.union(cell1, cell2)
            else :
                if self._rng.random() < 0.05:
                    pass
                else :
                    maze_walls.append(wall)
        self.fill_matrix_cells()

    def fill_matrix_cells(self):
        h = self.height
        w = self.width
        self.matrix_cells = [[[0, 0, 0, 0] for _ in range(w)] for _ in range(h)]
        mat = self.matrix_cells
        walls = self.maze_walls + self.pattern_walls
        for l1, l2 in zip(mat[0], mat[h - 1]):
            l1[0] = 1
            l2[2] = 1
        for row in mat:
            row[0][3] = 1
            row[w - 1][1] = 1
        for wall in walls :
            x1 = wall[0] % w
            y1 = wall[0] // w
            x2 = wall[1] % w
            y2 = wall[1] // w
            if wall[1] - wall[0] == 1:
                mat[y1][x1][1] = 1
                mat[y2][x2][3] = 1
            elif wall[1] - wall[0] == w:
                mat[y1][x1][2] = 1
                mat[y2][x2][0] = 1

    def output_file(self):
        if self.matrix_cells is None:
            return
        mat = self.matrix_cells
        try:
            with open(self.output_filename, "w") as file:
                for y in range(self.height):
                    hex_seq = ""
                    for x in range(self.width) :
                        val = mat[y][x][0] * 8 + mat[y][x][1] * 4 + mat[y][x][2] * 2 + mat[y][x][3]
                        hex_seq += f"{val:X}"
                    hex_seq+="\n"
                    file.write(hex_seq)
        except Exception as e:
            print("Something went wrong: ", e)

Dir = Enum('Direction', [('UP', 1), ('DOWN', 2), ('RIGHT', 3), ('LEFT', 4)])
class Bracktrack_Maze:
    def __init__(self, height, width, entry=(0, 0), exit=(0, 0), output_filename="maze.txt", seed = 42, cell_size = 42):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.output_filename = output_filename
        self.cell_size = cell_size
        self.walls = []
        self.matrix_cells = None
        self.pattern_walls = []
        self.pattern_cells = set()
        self.walls_to_remove = set()
        self.set_four_cells()
        self.set_two_cells()
        self.fill_walls()
        self._rng = random.Random(seed)

    def set_four_cells(self):
        w = self.width
        h = self.height
        left_cells = (w - 7) // 2
        top_cells = (h - 5) // 2
        pattern_cells = self.pattern_cells
        for i in range(5):
            if i == 2:
                pattern_cells.add((top_cells + i) * w + left_cells)
                pattern_cells.add((top_cells + i) * w + left_cells + 1)
                pattern_cells.add((top_cells + i) * w + left_cells + 2)
            elif i > 2:
                pattern_cells.add((top_cells + i) * w + left_cells + 2)
            else:
                pattern_cells.add((top_cells + i) * w + left_cells)

    def set_two_cells(self):
        w = self.width
        h = self.height
        left_cells = (w - 7) // 2 + 4
        top_cells = (h - 5) // 2
        pattern_cells = self.pattern_cells
        for i in range(5):
            if i == 1:
                pattern_cells.add((top_cells + i) * w +  left_cells + 2)
            elif i == 3 :
                pattern_cells.add((top_cells + i) * w + left_cells)
            else:
                pattern_cells.add((top_cells + i) * w + left_cells)
                pattern_cells.add((top_cells + i) * w + left_cells + 1)
                pattern_cells.add((top_cells + i) * w + left_cells + 2)

    def fill_walls(self):
        w = self.width
        h = self.height
        walls = self.walls
        pattern_cells = self.pattern_cells
        pattern_walls = self.pattern_walls
        for y in range(h):
            for x in range(w):
                index = y * w + x
                if x < w - 1:
                    walls.append((index, index + 1))
                if y < h - 1:
                    walls.append((index, index + w))

    def get_unvisited_neighbors(self, cur: int, visited: set):
        h = self.height
        w = self.width
        i = cur // w
        j = cur % w
        to_visit = []
        if i > 0:
            up = w * (i - 1) + j
            to_visit.append((up, Dir.UP))
        if i < h - 1:
            bottom = w * (i + 1) + j
            to_visit.append((bottom, Dir.DOWN))
        if j > 0:
            left = w * i + j - 1
            to_visit.append((left, Dir.LEFT))
        if j < w - 1:
            right = w * i + j + 1
            to_visit.append((right, Dir.RIGHT))
        return to_visit

    def add_to_walls_to_remove(self, cur, cell, direction):
        if direction == Dir.UP:
            self.walls_to_remove.add((cell, cur))
        if direction == Dir.DOWN:
            self.walls_to_remove.add((cur, cell))
        if direction == Dir.LEFT:
            self.walls_to_remove.add((cell, cur))
        if direction == Dir.RIGHT:
            self.walls_to_remove.add((cur, cell))

    def generate_perfect(self):
        def helper(cur: int, visited: set):
            neighbors = self.get_unvisited_neighbors(cur, visited)
            self._rng.shuffle(neighbors)
            for cell, direction in neighbors:
                if cell not in visited:
                    self.add_to_walls_to_remove(cur, cell, direction)
                    visited.add(cell)
                    helper(cell, visited)
        visited = {0}
        for cell in self.pattern_cells:
            visited.add(cell)
        helper(0, visited)
        self.fill_matrix_cells()

    def generate_regular(self):
        def helper(cur: int, visited: set):
            neighbors = self.get_unvisited_neighbors(cur, visited)
            self._rng.shuffle(neighbors)
            for cell, direction in neighbors:
                if cell not in visited:
                    self.add_to_walls_to_remove(cur, cell, direction)
                    visited.add(cell)
                    helper(cell, visited)
        visited = {0}
        for cell in self.pattern_cells:
            visited.add(cell)
        helper(0, visited)
        for wall in self.walls:
            if wall not in self.walls_to_remove and self._rng.random() < 0.05:
                self.walls_to_remove.add(wall)
        self.fill_matrix_cells()

    def fill_matrix_cells(self):
        h = self.height
        w = self.width
        self.matrix_cells = [[[0, 0, 0, 0] for _ in range(w)] for _ in range(h)]
        mat = self.matrix_cells
        for l1, l2 in zip(mat[0], mat[h - 1]):
            l1[0] = 1
            l2[2] = 1
        for row in mat:
            row[0][3] = 1
            row[w - 1][1] = 1
        walls = self.walls
        for wall in walls:
            if wall not in self.walls_to_remove:
                x1 = wall[0] % w
                y1 = wall[0] // w
                x2 = wall[1] % w
                y2 = wall[1] // w
                if wall[1] - wall[0] == 1:
                    mat[y1][x1][1] = 1
                    mat[y2][x2][3] = 1
                elif wall[1] - wall[0] == w:
                    mat[y1][x1][2] = 1
                    mat[y2][x2][0] = 1
    
    def output_file(self):
        if self.matrix_cells is None:
            return
        mat = self.matrix_cells
        try:
            with open(self.output_filename, "w") as file:
                for y in range(self.height):
                    hex_seq = ""
                    for x in range(self.width) :
                        val = mat[y][x][0] * 8 + mat[y][x][1] * 4 + mat[y][x][2] * 2 + mat[y][x][3]
                        hex_seq += f"{val:X}"
                    hex_seq += "\n"
                    file.write(hex_seq)
        except Exception as e:
            print("Error while openning the file: ", e)

if __name__ == "__main__":
    Maze = Bracktrack_Maze(50, 50, output_filename = "maze.txt")
    Maze.generate_regular()
    Maze.output_file()
    # Maze.generate_regular()
    # Maze.out_put_file()
