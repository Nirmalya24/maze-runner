# df_maze.py


import curses
#take a function and initialize a on object with the curses wrapper
from curses import wrapper
import sys
#already on macOS and linux
import numpy as np
import random
# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.

# Maze dimensions (ncols, nrows)
nx, ny = 4, 4
# Maze entry position
ix, iy = 0, 0

class Cell:
    """A cell in the maze.
    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.
    """
    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
    def has_all_walls(self):
        """Does this cell still have all its walls?"""
        return all(self.walls.values())
    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False
class Maze:
    """A Maze, represented as a grid of cells."""
    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).
        """
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""
        return self.maze_map[x][y]
    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * ((self.nx * 2)+1)]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if x == 0 and y == ny-1:
                    maze_row.append("🏃")
                    maze_row.append(" ")
                elif self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('--')
                else:
                    maze_row.append(' |')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows) 
    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""
        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx
        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""
            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)
        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            print('</svg>', file=f)
    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""
        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours
    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1
        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)
            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue
            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1

# Maze entry position
ix, iy = 0, 0
maze = Maze(nx, ny, ix, iy)
maze.make_maze()
maze.write_svg('maze.svg')

maze1 = maze.__str__()
maze1=maze1.split('\n')

res = []
for row in maze1:
  res.append(list(row))

intres = []
for row in res:
  temp = []
  for i in range(len(row)):
    if row[i]=="-":
      temp.append(0)
    elif row[i]==" ":
      temp.append(1)
    elif row[i]=="|":
      temp.append(2)
    else:
      temp.append(3)    
  intres.append(temp)        


map_data = intres

# init player's position
x = nx*2-1
y = 1
end_x = 1
end_y = 2*nx-1


# draw map
def print_map():
  map = []
  for row in map_data:
    temp = []
    for num in row:
      if num==0:
        temp.append("-")
      elif num==1:
        #print(" ", end = " ")
        temp.append(" ")
      elif num==2:
        #print("|", end = " ")
        temp.append("|")
      else:
        #print("🏃", end = "")    
        temp.append("🏃")
    map.append(temp) 
  npArr = np.array(map)
  string = '\n'.join(''.join(x+" " if x != "🏃" else x for x in y) for y in npArr)
  return string




# print out the map
print_map()


while True:

    order = input("Please Enter（a: LEFT，s: DOWN， d: RIGHT, w: UP）：")

    # UP
    if order == "a":
        y = y - 1
        # if reach a wall then game over
        if map_data[x][y] == "*" or map_data[x][y] == "|":
            print("Game over")
            break

        else:
            map_data[x][y], map_data[x][y + 1] = map_data[x][y + 1], map_data[x][y]
            stdscr.addstr(10,10,print_map())
            if map_data[x][y] == map_data[end_x][end_y]:
                print("You win")
                break

    # Down
    elif order == "s":
        x = x + 1
        if map_data[x][y] == 0 or map_data[x][y] == 2:
            print("Game over")
            break
        else:
            map_data[x][y], map_data[x - 1][y] = map_data[x - 1][y], map_data[x][y]
            stdscr.addstr(10,10,print_map())
            
            if map_data[x][y] == map_data[end_x][end_y]:
                print("You win")
                break

    # Right
    elif order == "d":
        y = y + 1
        if map_data[x][y] == 0 or map_data[x][y] == 2:
            print("Game over")
            break
        else:
            map_data[x][y], map_data[x][y - 1] = map_data[x][y - 1], map_data[x][y]
            stdscr.addstr(10,10,print_map())
            if map_data[x][y] == map_data[end_x][end_y]:
                print("You win")
                break

    # Left
    elif order == "w":
        x = x - 1
        if map_data[x][y] == 0 or map_data[x][y] == 2:
            print("Game over")
            break
        else:
            map_data[x][y], map_data[x + 1][y] = map_data[x + 1][y], map_data[x][y]
            stdscr.addstr(10,10,print_map())
            if map_data[x][y] == map_data[end_x][end_y]:
                print("You win")
                break

    # invalid input
    else:
        print("Please enter a valid letter (w,a,s,d)！")
        continue    
