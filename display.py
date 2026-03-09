import sys
from mlx import Mlx

class MazeDisplay:
    def __init__(self, maze_instance):
        self.maze = maze_instance
        self.width = self.maze.width
        self.height = self.maze.height

        self.win_w = 1024
        self.win_h = 768
        
        self.ui_height = 60
        self.margin = 40

        usable_w = self.win_w - (2 * self.margin)
        usable_h = self.win_h - self.ui_height - (2 * self.margin)

        self.cell_size = min(usable_w // self.width, usable_h // self.height)
        self.cell_size = min(self.cell_size, 60)

        self.offset_x = self.margin + (usable_w - (self.width * self.cell_size)) // 2
        self.offset_y = self.ui_height + self.margin + (usable_h - (self.height * self.cell_size)) // 2

        self.mlx_wrap = Mlx()
        self.mlx_ptr = self.mlx_wrap.mlx_init()
        self.win_ptr = self.mlx_wrap.mlx_new_window(self.mlx_ptr, self.win_w, self.win_h, "A-Maze-ing - Clean PRO")
        
        self.img_ptr = self.mlx_wrap.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        self.img_data, self.bpp, self.size_line, self.endian = self.mlx_wrap.mlx_get_data_addr(self.img_ptr)
        self.bytes_per_pixel = self.bpp // 8

        self.show_path = False
        self.theme_idx = 0
        
        self.themes = [
            (0x3C3C3C, 0x1E1E1E, 0x007ACC), 
            (0x75715E, 0x272822, 0xA6E22E), 
            (0x504945, 0x282828, 0xFB4934)  
        ]

        self.c_entry = 0x10B981   
        self.c_exit = 0xEF4444    
        self.c_42 = 0x8B5CF6      
        self.c_ui_bg = 0x0F0F0F   
        
        self.is_drawn = False

    def fast_put_pixel(self, x, y, color):
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            index = (y * self.size_line) + (x * self.bytes_per_pixel)
            self.img_data[index] = color & 0xFF             
            self.img_data[index + 1] = (color >> 8) & 0xFF  
            self.img_data[index + 2] = (color >> 16) & 0xFF 
            if self.bytes_per_pixel == 4:
                self.img_data[index + 3] = 255 

    def draw_rect(self, start_x, start_y, w, h, color):
        for y in range(start_y, start_y + h):
            for x in range(start_x, start_x + w):
                self.fast_put_pixel(x, y, color)
    
    def setup_hooks(self):
        self.mlx_wrap.mlx_hook(self.win_ptr, 17, 0, self.close_window, self)
        self.mlx_wrap.mlx_hook(self.win_ptr, 2, 1, self.key_press, self)
        self.mlx_wrap.mlx_hook(self.win_ptr, 12, 0, self.expose_event, self)

    def expose_event(self, *args):
        if not self.is_drawn:
            self.render_maze()
            self.is_drawn = True

    def close_window(self, *args):
        self.mlx_wrap.mlx_loop_exit(self.mlx_ptr)
        self.mlx_wrap.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.mlx_wrap.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        print("\n[+] Exited successfully.")
        sys.exit(0)

    def draw_ui_text(self):
        y_text = 35 
        c_text = 0xCCCCCC 
        
        theme_names = ["VS Code", "Monokai", "Gruvbox"]
        
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 30, y_text, c_text, "[R] Regenerate")
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 200, y_text, c_text, "[C] Theme")
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 350, y_text, c_text, "[P] Toggle Path")
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 550, y_text, c_text, "[ESC] Quit")
        
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, self.win_w - 120, y_text, 0x007ACC, theme_names[self.theme_idx])

    def render_maze(self):
        c_wall, c_bg, c_path = self.themes[self.theme_idx]

        self.draw_rect(0, 0, self.win_w, self.win_h, c_bg)
        
        self.draw_rect(0, 0, self.win_w, self.ui_height, self.c_ui_bg)
        self.draw_rect(0, self.ui_height - 1, self.win_w, 1, 0x333333)

        wall_thick = max(1, self.cell_size // 10)

        for y in range(self.height):
            for x in range(self.width):
                px = self.offset_x + (x * self.cell_size)
                py = self.offset_y + (y * self.cell_size)
                index_1d = y * self.width + x

                if (x, y) == self.maze.entry_point:
                    self.draw_rect(px, py, self.cell_size, self.cell_size, self.c_entry)
                elif (x,y) == self.maze.exit_point:
                    self.draw_rect(px, py, self.cell_size, self.cell_size, self.c_exit)
                elif index_1d in self.maze.pattern_cells:
                    self.draw_rect(px, py, self.cell_size, self.cell_size, self.c_42)
                
                cell = self.maze.matrix_cells[y][x]
                if cell[0] == 1:
                    self.draw_rect(px, py, self.cell_size, wall_thick, c_wall)
                if cell[1] == 1:
                    self.draw_rect(px + self.cell_size - wall_thick, py, wall_thick, self.cell_size, c_wall)
                if cell[2] == 1:
                    self.draw_rect(px, py + self.cell_size - wall_thick, self.cell_size, wall_thick, c_wall)
                if cell[3] == 1:
                    self.draw_rect(px, py, wall_thick, self.cell_size, c_wall)
                
        if self.show_path and self.maze.shortest_path:
            path_size = max(2, self.cell_size // 3)
            path_offset = (self.cell_size - path_size) // 2

            for node_1d in self.maze.shortest_path:
                px = self.offset_x + ((node_1d % self.width) * self.cell_size) + path_offset
                py = self.offset_y + ((node_1d // self.width) * self.cell_size) + path_offset
                self.draw_rect(px, py, path_size, path_size, c_path)
                
        self.mlx_wrap.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        self.draw_ui_text()

    def key_press(self, keycode, *args):
        if keycode in [53, 65307]:
            self.close_window()
        elif keycode in [15, 114]:
            self.maze.generate_perfect()
            self.maze.solve_maze()
            self.render_maze()
        elif keycode in [8, 99]:
            self.theme_idx = (self.theme_idx + 1) % len(self.themes)
            self.render_maze()
        elif keycode in [35, 112]:
            self.show_path = not self.show_path
            self.render_maze()
    
    def run(self):
        self.setup_hooks()
        print("[+] MLX Engine started. Window running.")
        self.mlx_wrap.mlx_loop(self.mlx_ptr)

if __name__ == "__main__":
    from maze_gen import Kruskal_Maze
    sys.setrecursionlimit(30000)
    
    maze_size = 100
    maze = Kruskal_Maze(maze_size, maze_size, entry_point=(0, 1), exit_point=(maze_size-1, maze_size-1))
    
    maze.generate_regular()
    maze.solve_maze()

    ui = MazeDisplay(maze)
    ui.run()