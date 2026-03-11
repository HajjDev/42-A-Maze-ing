# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  display.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cel-hajj <cel-hajj@student.s19.be>        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/10 23:49:26 by cel-hajj        #+#    #+#               #
#  Updated: 2026/03/11 16:41:17 by cel-hajj        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
Handles the graphical display and user interaction for the Maze Generator.
"""
import os
import time
from typing import Any
from mlx import Mlx
from src.maze_generator import MazeGenerator


class MazeDisplay:
    """
    A graphical interface class for rendering a maze and handling user
    interactions.
    """
    def __init__(self, maze_instance: MazeGenerator) -> None:
        """
        Initializes the MLX display and sets up window dimensions, image
        buffer, and UI.

        Args:
            maze_instance (MazeGenerator): The generated maze object
            containing grid data.

        Returns:
            None: This constructor does not return a value.
        """
        self.maze = maze_instance
        self.width = self.maze.width
        self.height = self.maze.height

        self.mlx_wrap = Mlx()
        self.mlx_ptr = self.mlx_wrap.mlx_init()

        screen_width, screen_height = self.mlx_wrap.mlx_get_screen_size(
            self.mlx_ptr)[1:]

        max_win_w = int(screen_width * 0.95)
        max_win_h = int(screen_height * 0.95)

        tile_w = max_win_w // self.maze.width
        tile_h = max_win_h // self.maze.height

        self.tile_size = max(2, min(tile_w, tile_h, 32))

        self.win_w = max(800, self.maze.width * self.tile_size)
        self.win_h = self.maze.height * self.tile_size

        self.ui_height = 60
        self.margin = 40

        usable_w = self.win_w - (2 * self.margin)
        usable_h = self.win_h - self.ui_height - (2 * self.margin)

        self.cell_size = min(usable_w // self.width, usable_h // self.height)
        self.cell_size = min(self.cell_size, 60)

        self.offset_x = (self.margin +
                         (usable_w - (self.width * self.cell_size)) // 2)
        self.offset_y = (self.ui_height + self.margin +
                         (usable_h - (self.height * self.cell_size)) // 2)

        self.win_ptr = self.mlx_wrap.mlx_new_window(self.mlx_ptr,
                                                    self.win_w,
                                                    self.win_h,
                                                    "A-Maze-ing - Clean PRO")

        self.img_ptr = self.mlx_wrap.mlx_new_image(self.mlx_ptr,
                                                   self.win_w,
                                                   self.win_h)

        (self.img_data,
         self.bpp,
         self.size_line,
         self.endian) = self.mlx_wrap.mlx_get_data_addr(self.img_ptr)

        self.bytes_per_pixel = self.bpp // 8

        self.show_path = False
        self.theme_idx = 0

        self.themes = [
            (0x3C3C3C, 0x1E1E1E, 0x007ACC),
            (0x75715E, 0x272822, 0xA6E22E),
            (0x504945, 0x282828, 0xFB4934),
            (0x44475A, 0x282A36, 0xFF79C6),
            (0x3B4252, 0x2E3440, 0x88C0D0),
            (0x5C6370, 0x282C34, 0xE06C75),
            (0xA9B1D6, 0x1A1B26, 0x7AA2F7),
            (0x585858, 0x161616, 0x42BE65),
            (0xC0C0C0, 0x0D0D0D, 0xFF6600),
        ]

        self.c_entry = 0x10B981
        self.c_exit = 0xEF4444
        self.c_42 = 0x8B5CF6
        self.c_ui_bg = 0x0F0F0F

        self.last_key_time = 0.0
        self.key_cooldown = 0.3

        self.is_drawn = False

    def fast_put_pixel(self, x: int, y: int, color: int) -> None:
        """
        Modifies the raw image data buffer to color a specific pixel safely.

        Args:
            x (int): The x-coordinate of the pixel.
            y (int): The y-coordinate of the pixel.
            color (int): The hexadecimal color value.

        Returns:
            None: This method does not return a value.
        """
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            index = (y * self.size_line) + (x * self.bytes_per_pixel)
            self.img_data[index] = color & 0xFF
            self.img_data[index + 1] = (color >> 8) & 0xFF
            self.img_data[index + 2] = (color >> 16) & 0xFF
            if self.bytes_per_pixel == 4:
                self.img_data[index + 3] = 255

    def draw_rect(self, start_x: int, start_y: int, w: int,
                  h: int, color: int) -> None:
        """
        Draws a filled rectangle on the image buffer using byte-level
        manipulation.

        Args:
            start_x (int): The starting x-coordinate (top-left).
            start_y (int): The starting y-coordinate (top-left).
            w (int): The width of the rectangle in pixels.
            h (int): The height of the rectangle in pixels.
            color (int): The hexadecimal color value.

        Returns:
            None: This method does not return a value.
        """
        b = bytes([color & 0xFF,
                   (color >> 8) & 0xFF,
                   (color >> 16) & 0xFF,
                   0xFF])
        row = b * w
        for y in range(start_y, start_y + h):
            idx = y * self.size_line + start_x * self.bytes_per_pixel
            self.img_data[idx:idx + len(row)] = row

    def setup_hooks(self) -> None:
        """
        Registers the MLX event hooks for keyboard input and window
        interactions.

        Returns:
            None: This method does not return a value.
        """
        self.mlx_wrap.mlx_hook(self.win_ptr, 17, 0, self.close_window, self)
        self.mlx_wrap.mlx_hook(self.win_ptr, 2, 1, self.key_press, self)
        self.mlx_wrap.mlx_hook(self.win_ptr, 12, 0, self.expose_event, self)

    def expose_event(self, *_args: Any) -> None:
        """
        Handles the window expose event to ensure the maze renders correctly.

        Returns:
            None: This method does not return a value.
        """
        if not self.is_drawn:
            self.render_maze()
            self.is_drawn = True

    def close_window(self, *_args: Any) -> None:
        """
        Terminates the MLX loop, destroys memory pointers, and exits the
        program.

        Returns:
            None: This method does not return a value.
        """
        self.mlx_wrap.mlx_loop_exit(self.mlx_ptr)
        self.mlx_wrap.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.mlx_wrap.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        os._exit(0)

    def draw_ui_text(self) -> None:
        """
        Renders the user interface instructions and active theme name onto the
        header.

        Returns:
            None: This method does not return a value.
        """
        y_text = 35
        c_text = 0xCCCCCC

        theme_names = ["VS Code", "Monokai", "Gruvbox", "Dracula", "Nord",
                       "One Dark", "Tokyo Night", "Carbon", "Matrix"]

        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 30, y_text,
                                     c_text, "[R] Regenerate")
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 200, y_text,
                                     c_text, "[C] Theme")
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 350, y_text,
                                     c_text, "[P] Toggle Path")
        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr, 550, y_text,
                                     c_text, "[ESC] Quit")

        self.mlx_wrap.mlx_string_put(self.mlx_ptr, self.win_ptr,
                                     self.win_w - 120, y_text, 0x007ACC,
                                     theme_names[self.theme_idx])

    def render_maze(self) -> None:
        """
        Redraws the entire maze environment including background, walls, and
        path.

        Returns:
            None: This method does not return a value.
        """
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
                    self.draw_rect(px, py, self.cell_size, self.cell_size,
                                   self.c_entry)
                elif (x, y) == self.maze.exit_point:
                    self.draw_rect(px, py, self.cell_size, self.cell_size,
                                   self.c_exit)
                elif index_1d in self.maze.pattern_cells:
                    self.draw_rect(px, py, self.cell_size, self.cell_size,
                                   self.c_42)

                if self.maze.matrix_cells is not None:
                    cell = self.maze.matrix_cells[y][x]
                    if cell[0] == 1:
                        self.draw_rect(px, py, self.cell_size, wall_thick,
                                       c_wall)
                    if cell[1] == 1:
                        self.draw_rect(px + self.cell_size - wall_thick, py,
                                       wall_thick, self.cell_size, c_wall)
                    if cell[2] == 1:
                        self.draw_rect(px, py + self.cell_size - wall_thick,
                                       self.cell_size, wall_thick, c_wall)
                    if cell[3] == 1:
                        self.draw_rect(px, py, wall_thick, self.cell_size,
                                       c_wall)
        if self.show_path and self.maze.shortest_path:
            path_w = max(2, self.cell_size // 4)
            half = path_w // 2

            for i in range(len(self.maze.shortest_path) - 1):
                n1 = self.maze.shortest_path[i]
                n2 = self.maze.shortest_path[i + 1]

                # Centre des deux cellules consécutives
                cx1 = (
                    self.offset_x + (n1 % self.width) *
                    self.cell_size + self.cell_size // 2
                )
                cy1 = (
                    self.offset_y + (n1 // self.width) *
                    self.cell_size + self.cell_size // 2
                )
                cx2 = (
                    self.offset_x + (n2 % self.width) *
                    self.cell_size + self.cell_size // 2
                )
                cy2 = (
                    self.offset_y + (n2 // self.width) *
                    self.cell_size + self.cell_size // 2
                )

                # Segment horizontal ou vertical entre les deux centres
                x = min(cx1, cx2) - half
                y = min(cy1, cy2) - half
                w = abs(cx2 - cx1) + path_w
                h = abs(cy2 - cy1) + path_w
                self.draw_rect(x, y, w, h, c_path)

        self.mlx_wrap.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr,
                                              self.img_ptr, 0, 0)
        self.draw_ui_text()

    def key_press(self, keycode: int, *_args: Any) -> None:
        """
        Handles keyboard inputs to trigger interface actions with an anti-spam
        cooldown.

        Args:
            keycode (int): The integer code corresponding to the pressed key.

        Returns:
            None: This method does not return a value.
        """
        current_time = time.time()
        if current_time - self.last_key_time < self.key_cooldown:
            return

        self.last_key_time = current_time
        if keycode in [53, 65307]:
            self.close_window()
        elif keycode in [15, 114]:
            self.maze.generate()
            self.render_maze()
        elif keycode in [8, 99]:
            self.theme_idx = (self.theme_idx + 1) % len(self.themes)
            self.render_maze()
        elif keycode in [35, 112]:
            self.show_path = not self.show_path
            self.render_maze()

    def run(self) -> None:
        """
        Initializes event hooks and launches the main MLX event loop.

        Returns:
            None: This method does not return a value.
        """
        self.setup_hooks()
        self.mlx_wrap.mlx_loop(self.mlx_ptr)
