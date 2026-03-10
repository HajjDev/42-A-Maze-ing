#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cel-hajj <cel-hajj@student.s19.be>        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/02 07:38:57 by cel-hajj        #+#    #+#               #
#  Updated: 2026/03/02 08:38:05 by cel-hajj        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
TODO
"""
import sys
from parsing.parse_config import parse_config
from maze_generator import MazeGenerator


def a_maze_ing() -> None:
    """
    TODO
    """
    config_data = parse_config(len(sys.argv), sys.argv)
    if config_data != -1:
        maze = MazeGenerator(config_data)


if __name__ == "__main__":
    a_maze_ing()
