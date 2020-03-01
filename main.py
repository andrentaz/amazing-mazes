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
    """Crate adjacency list so we can create the graph"""

    def add_node_to_adjacency(adjacency, x, y, node_id):
        """Add edges to the nodes in the graph"""

        # check neighboors on the left
        for i in reversed(range(x)):
            # there is no edge if we find a wall
            if grid[y][i] == 0:
                break

            if isinstance(grid[y][i], str):
                # code to add edge in adjacency list
                weight = (x - i)
                adjacency.append(' '.join([
                    str(node_id),
                    str(grid[y][i]),
                    str(weight),
                ]))
                break

        # check neighboors on the top
        for i in reversed(range(y)):
            # there is no edge if we find a wall
            if grid[i][x] == 0:
                break

            if isinstance(grid[i][x], str):
                # code to add edge in adjacency list
                weight = (y - i)
                adjacency.append(' '.join([
                    str(node_id),
                    str(grid[i][x]),
                    str(weight),
                ]))
                break


    # adjacency list information
    adjacency = []
    height = len(grid)
    width = len(grid[0])
    node_count = 0

    # convert grid first row to list of adjacency
    import ipdb
    ipdb.set_trace()
    for idx, i in enumerate(grid[0]):
        if i == 0:
            continue

        if i == 1:
            add_node_to_adjacency(adjacency, 0, idx, node_count)
            grid[0][idx] = str(node_count)
            node_count += 1
            break

    # convert grid interior to list of adjacency
    for i, row in enumerate(grid[1:height-1], 1):
        for j, column in enumerate(row[1:width-1], 1):

            # if we are in a wall, just continue
            if column == 0:
                continue

            # check the neighboors
            top = grid[i-1][j]
            bottom = grid[i+1][j]
            left = grid[i][j-1]
            right = grid[i][j+1]

            # convert it to a number
            top = top if not isinstance(top, str) else 1
            bottom = bottom if not isinstance(bottom, str) else 1
            left = left if not isinstance(left, str) else 1
            right = right if not isinstance(right, str) else 1

            freedom_degree = top + bottom + left + right

            # 1) case we have a bifurcation
            if freedom_degree > 2:
                add_node_to_adjacency(adjacency, j, i, node_count)
                grid[i][j] = str(node_count)
                node_count += 1
                continue

            # 2) case we have a junction
            if top + bottom == 1 and left + right == 1:
                add_node_to_adjacency(adjacency, j, i, node_count)
                grid[i][j] = str(node_count)
                node_count += 1
                continue

            # 3) case a dead end
            if freedom_degree == 1:
                add_node_to_adjacency(adjacency, j, i, node_count)
                grid[i][j] = str(node_count)
                node_count += 1
                continue

    # convert grid last row to list of adjacency
    for idx, i in enumerate(grid[-1]):
        j = len(grid) - 1
        if i == 0:
            continue

        if i == 1:
            add_node_to_adjacency(adjacency, j, idx, node_count)
            grid[-1][idx] = str(node_count)
            node_count += 1
            break

    # return list of adjacency
    return adjacency


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
