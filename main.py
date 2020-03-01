# -*- encoding: utf-8 -*-
"""
A program that reads mazes from png files and converts them to a graph which is
used then to find various kinds of solutions.

:author: Andre Filliettaz
:email: andrentaz@gmail.com
:github: https://github.com/andrentaz
"""
from __future__ import absolute_import, unicode_literals

import argparse

from PIL import Image

from graph import Graph


def create_grid_from_image(maze):
    """Create the grid from the png images so we can create the graph later"""
    img = Image.open(maze, 'r')

    # get image metadata and pixels
    width = img.size[0]
    height = img.size[1]
    pixels = list(img.getdata(0))

    grid = []
    for i in range(height):
        offset = i * width
        row = pixels[offset:offset+width]
        grid.append(row)

    return grid


def create_adjacency_list(grid):
    pass

def main(maze, algorithm):
    """Solve the maze using graphs"""
    grid = create_grid_from_image(maze)
    adjacency_list = create_adjacency_list(grid)


if __name__ == '__main__':
    # handle script arguments
    parser = argparse.ArgumentParser(
        description='Calculate paths in mazes.'
    )
    parser.add_argument('maze',
                        help='path to png file containing the the maze')
    parser.add_argument('type',
                        help='what algorithm to find the path')
    args = parser.parse_args()

    # call main function
    main(
        maze=args.maze,
        algorithm=args.type,
    )
