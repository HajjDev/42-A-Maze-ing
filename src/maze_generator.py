"""
TODO
"""
import random
import heapq
from typing import Any, Dict, List, Tuple, Union, Set
from enum import Enum


class MazeGenerator:
    """
    TODO
    """
    Direction = Enum(
        'Direction',
        [('UP', 1), ('DOWN', 2), ('RIGHT', 3), ('LEFT', 4)]
    )

    class DSU:
        """
        TODO
        """
        def __init__(self, n: int) -> None:
            """
            TODO
            """
            self.parent = [i for i in range(n)]
            self.rank = [1 for i in range(n)]

        def find(self, child: int) -> int:
            """
            TODO
            """
            if self.parent[child] != child:
                self.parent[child] = self.find(self.parent[child])
            return self.parent[child]

        def union(self, i: int, j: int) -> bool:
            """
            TODO
            """
            root_1 = self.find(i)
            root_2 = self.find(j)
            if root_1 != root_2:
                if self.rank[root_1] > self.rank[root_2]:
                    self.parent[root_2] = root_1
                elif self.rank[root_1] < self.rank[root_2]:
                    self.parent[root_1] = root_2
                else:
                    self.parent[root_1] = root_2
                    self.rank[root_2] += 1
                return True
            return False

    def __init__(self, width: int, height: int, seed: int, cell_size: int,
                 entry_point: Tuple[int, int], exit_point: Tuple[int, int],
                 algorithm: str, maze_type: str, output_filename: str) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.algorithm = algorithm
        self.maze_type = maze_type
        self.output_filename = output_filename
        self._rng = random.Random(seed)
        self.walls: List[Tuple[int, int]] = []
        self.maze_walls: List[Tuple[int, int]] = []
        self.pattern_walls: List[Tuple[int, int]] = []
        self.pattern_cells: Set[int] = set()
        self.walls_to_remove: Set[Tuple[int, int]] = set()
        self.matrix_cells: Union[List[List[List[int]]], None] = None
        self.shortest_path: Union[List[int], None] = None
        self.set_four_cells()
        self.set_two_cells()
        self.fill_walls()

    def set_four_cells(self) -> None:
        """
        TODO
        """
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

    def set_two_cells(self) -> None:
        """
        TODO
        """
        w = self.width
        h = self.height
        left_cells = (w - 7) // 2 + 4
        top_cells = (h - 5) // 2
        pattern_cells = self.pattern_cells
        for i in range(5):
            if i == 1:
                pattern_cells.add((top_cells + i) * w + left_cells + 2)
            elif i == 3:
                pattern_cells.add((top_cells + i) * w + left_cells)
            else:
                pattern_cells.add((top_cells + i) * w + left_cells)
                pattern_cells.add((top_cells + i) * w + left_cells + 1)
                pattern_cells.add((top_cells + i) * w + left_cells + 2)

    def fill_walls(self) -> None:
        """
        TODO
        """
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

    def kruskal_fill_matrix_cells(self) -> None:
        """
        TODO
        """
        h = self.height
        w = self.width
        self.matrix_cells = [[[0, 0, 0, 0] for _ in range(w)]
                             for _ in range(h)]
        mat = self.matrix_cells
        walls = self.maze_walls + self.pattern_walls
        for l1, l2 in zip(mat[0], mat[h - 1]):
            l1[0] = 1
            l2[2] = 1
        for row in mat:
            row[0][3] = 1
            row[w - 1][1] = 1
        for wall in walls:
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

    def dfs_fill_matrix_cells(self) -> None:
        """
        TODO
        """
        h = self.height
        w = self.width
        self.matrix_cells = [[[0, 0, 0, 0] for _ in range(w)]
                             for _ in range(h)]
        mat = self.matrix_cells
        for l1, l2 in zip(mat[0], mat[h - 1]):
            l1[0] = 1
            l2[2] = 1
        for row in mat:
            row[0][3] = 1
            row[w - 1][1] = 1
        walls = self.walls + self.pattern_walls
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

    def get_unvisited_neighbors(self, cur: int) -> List[Tuple[int, Any]]:
        """
        TODO
        """
        h = self.height
        w = self.width
        i = cur // w
        j = cur % w
        to_visit: List[Tuple[int, Any]] = []
        if i > 0:
            up = w * (i - 1) + j
            to_visit.append((up, self.Direction.UP))
        if i < h - 1:
            bottom = w * (i + 1) + j
            to_visit.append((bottom, self.Direction.DOWN))
        if j > 0:
            left = w * i + j - 1
            to_visit.append((left, self.Direction.LEFT))
        if j < w - 1:
            right = w * i + j + 1
            to_visit.append((right, self.Direction.RIGHT))
        return to_visit

    def add_to_walls_to_remove(self, cur: int, cell: int,
                               direction: Direction) -> None:
        """
        TODO
        """
        match direction:
            case self.Direction.UP:
                self.walls_to_remove.add((cell, cur))
            case self.Direction.DOWN:
                self.walls_to_remove.add((cur, cell))
            case self.Direction.LEFT:
                self.walls_to_remove.add((cell, cur))
            case self.Direction.RIGHT:
                self.walls_to_remove.add((cur, cell))

    def kruskal_generate_perfect(self) -> None:
        """
        TODO
        """
        self._rng.shuffle(self.walls)
        dsu = self.DSU(self.height * self.width)
        maze_walls = self.maze_walls
        maze_walls.clear()
        for wall in self.walls:
            cell1, cell2 = wall
            if dsu.find(cell1) != dsu.find(cell2):
                dsu.union(cell1, cell2)
            else:
                maze_walls.append(wall)

    def kruskal_generate_regular(self) -> None:
        """
        TODO
        """
        self._rng.shuffle(self.walls)
        dsu = self.DSU(self.height * self.width)
        maze_walls = self.maze_walls
        maze_walls.clear()
        for wall in self.walls:
            cell1, cell2 = wall
            if dsu.find(cell1) != dsu.find(cell2):
                dsu.union(cell1, cell2)
            else:
                if self._rng.random() < 0.05:
                    pass
                else:
                    maze_walls.append(wall)

    def dfs_generate_perfect(self) -> None:
        """
        TODO
        """
        def helper(cur: int, visited: Set[int]) -> None:
            """
            TODO
            """
            neighbors = self.get_unvisited_neighbors(cur)
            self._rng.shuffle(neighbors)
            for cell, direction in neighbors:
                if cell not in visited:
                    self.add_to_walls_to_remove(cur, cell, direction)
                    visited.add(cell)
                    helper(cell, visited)
        start = self.entry_point[1] * self.width + self.entry_point[0]
        visited = set()
        for cell in self.pattern_cells:
            visited.add(cell)
        helper(start, visited)

    def dfs_generate_regular(self) -> None:
        """
        TODO
        """
        def helper(cur: int, visited: set):
            neighbors = self.get_unvisited_neighbors(cur)
            self._rng.shuffle(neighbors)
            for cell, direction in neighbors:
                if cell not in visited:
                    self.add_to_walls_to_remove(cur, cell, direction)
                    visited.add(cell)
                    helper(cell, visited)
        start = self.entry_point[1] * self.width + self.entry_point[0]
        visited = set()
        for cell in self.pattern_cells:
            visited.add(cell)
        helper(start, visited)
        for wall in self.walls:
            if wall not in self.walls_to_remove and self._rng.random() < 0.05:
                self.walls_to_remove.add(wall)

    def solve_maze(self) -> None:
        """
        TODO
        """
        if self.matrix_cells is None:
            return
        matrix_cells = self.matrix_cells
        width = self.width
        height = self.height
        start = self.entry_point[1] * width + self.entry_point[0]
        end = self.exit_point[1] * width + self.exit_point[0]

        def get_available_neighbor(node: int) -> List[int]:
            """
            TODO
            """
            j = node // width
            i = node % width
            neighbor = []
            if matrix_cells[j][i][0] == 0:
                neighbor.append(width * (j - 1) + i)
            if matrix_cells[j][i][1] == 0:
                neighbor.append(width * j + i + 1)
            if matrix_cells[j][i][2] == 0:
                neighbor.append(width * (j + 1) + i)
            if matrix_cells[j][i][3] == 0:
                neighbor.append(width * j + i - 1)
            return neighbor

        def dijkstra() -> Union[List[int], None]:
            """
            TODO
            """
            distance = [float('inf')] * (width * height)
            distance[start] = 0
            parent: Dict[Any, Any] = {start: None}
            pq = [(0, start)]
            while pq:
                cur_dist, cur_ver = heapq.heappop(pq)
                if cur_ver == end:
                    path: List[Any] = []
                    while cur_ver is not None:
                        path.append(cur_ver)
                        cur_ver = parent[cur_ver]
                    return path[::-1]
                if cur_dist != distance[cur_ver]:
                    continue
                neighbor_list = get_available_neighbor(cur_ver)
                for neighbor in neighbor_list:
                    dist = cur_dist + 1
                    if dist < distance[neighbor]:
                        parent[neighbor] = cur_ver
                        distance[neighbor] = dist
                        heapq.heappush(pq, (dist, neighbor))
            return None
        self.shortest_path = dijkstra()

    def generate_output_file(self) -> None:
        """
        TODO
        """
        if self.matrix_cells is None or self.shortest_path is None:
            return
        mat = self.matrix_cells
        shortest_path = self.shortest_path
        try:
            with open(self.output_filename, "w", encoding="utf-8") as file:
                for y in range(self.height):
                    hex_seq = ""
                    for x in range(self.width):
                        val = (mat[y][x][0] + mat[y][x][1] * 2 +
                               mat[y][x][2] * 4 + mat[y][x][3] * 8)
                        hex_seq += f"{val:X}"
                    hex_seq += "\n"
                    file.write(hex_seq)
                file.write("\n")
                file.write(f"{self.entry_point[0]},{self.entry_point[1]}\n")
                file.write(f"{self.exit_point[0]},{self.exit_point[1]}\n")
                direction = ""
                for i in range(len(shortest_path) - 1):
                    if shortest_path[i + 1] - shortest_path[i] == self.width:
                        direction += "S"
                    if shortest_path[i + 1] - shortest_path[i] == -self.width:
                        direction += "N"
                    if shortest_path[i + 1] - shortest_path[i] == 1:
                        direction += "E"
                    if shortest_path[i + 1] - shortest_path[i] == -1:
                        direction += "W"
                direction += "\n"
                file.write(direction)
        except (FileNotFoundError, PermissionError, FileExistsError) as e:
            print("Something went wrong: ", e)

    def generate(self) -> None:
        """
        TODO
        """
        if self.algorithm == 'dfs':
            if self.maze_type == 'perfect':
                self.dfs_generate_perfect()
            else:
                self.dfs_generate_regular()
            self.dfs_fill_matrix_cells()
        else:
            if self.maze_type == 'prefect':
                self.kruskal_generate_perfect()
            else:
                self.kruskal_generate_regular()
            self.kruskal_fill_matrix_cells()
        self.solve_maze()
        self.generate_output_file()

        self.maze_walls.clear()
        self.walls_to_remove.clear()
