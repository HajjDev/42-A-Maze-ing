#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cel-hajj <cel-hajj@student.s19.be>        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/02 07:38:57 by cel-hajj        #+#    #+#               #
#  Updated: 2026/03/10 23:45:13 by cel-hajj        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
Main entry point for the A-Maze-ing application. It coordinates parsing the
configuration file, initializing the maze generation engine, and launching
the graphical display loop.
"""
import sys
from src.parsing.parse_config import parse_config
from src.maze_generator import MazeGenerator
from src.display import MazeDisplay


def a_maze_ing() -> None:
    """
    Executes the main routine of the application. Extracts data from the
    configuration file via command-line arguments, instantiates the maze,
    triggers the generation process, and starts the MLX renderer.

    Returns:
        None: This function does not return a value.
    """
    sys.setrecursionlimit(40000)
    config_data = parse_config(len(sys.argv), sys.argv)
    if isinstance(config_data, dict):
        maze = MazeGenerator(width=config_data["WIDTH"],
                             height=config_data["HEIGHT"],
                             seed=config_data["SEED"],
                             cell_size=32,
                             entry_point=config_data["ENTRY"],
                             exit_point=config_data["EXIT"],
                             algorithm=config_data["ALGORITHM"],
                             maze_type=("perfect" if config_data["PERFECT"]
                             else "regular"),
                             output_filename=config_data["OUTPUT_FILE"])

        display = MazeDisplay(maze)
        maze.generate()
        display.run()


if __name__ == "__main__":
    a_maze_ing()
