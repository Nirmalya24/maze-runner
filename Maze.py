# Maze generator -- Randomized Prim Algorithm

import os
import random


class Maze:

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.maze_data = None
    self.generate_maze()
    self.start = (0, 0)
    self.end = (0, 0)
    self.wall = 'w'
    self.cell = 'c'
    self.unvisited = 'u'
    self.visited = []
    self.path = []
    # Starting position for players
    self.starting_posX = -1
    self.starting_posY = -1
    # Ending Position for players
    self.finish_posX = -1
    self.finish_posY = -1
    # Maze Emoji's
    self.MAZE_WALL = "\U0001F7E8"
    self.FINISH = "\U0001F3C1"
    self.PLAYER = "\U0001F3C3"

  # Return the finish x, y position
  def get_finish_pos(self):
    return [self.finish_posX, self.finish_posY]

  # Return the starting x, y position
  def get_start_pos(self):
    return [self.starting_posX, self.starting_posY]

  def print_maze(self):
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, self.height):
      for j in range(0, self.width):
        if self.maze_data[i][j] == 'u':
          print(" u", end=" ")
        elif self.maze_data[i][j] == 'c':
          print("  ", end=" ")
        elif self.maze_data[i][j] == 'f':
          print(self.FINISH, end=" ")
        elif self.maze_data[i][j] == 's':
          print(self.PLAYER, end=" ")
        else:
          print(self.MAZE_WALL, end=" ")

      print('\n')

  # Find number of surrounding cells
  def surrounding_cells(self, rand_wall):
    s_cells = 0
    if self.maze_data[rand_wall[0] - 1][rand_wall[1]] == 'c':
      s_cells += 1
    if self.maze_data[rand_wall[0] + 1][rand_wall[1]] == 'c':
      s_cells += 1
    if self.maze_data[rand_wall[0]][rand_wall[1] - 1] == 'c':
      s_cells += 1
    if self.maze_data[rand_wall[0]][rand_wall[1] + 1] == 'c':
      s_cells += 1

    return s_cells

  # Maze generation algorithm
  def generate_maze(self):
    # Denote all cells as unvisited
    for i in range(0, self.height):
      line = []
      for j in range(0, self.width):
        line.append(self.unvisited)
      self.maze_data.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random() * self.height)
    starting_width = int(random.random() * self.width)
    if starting_height == 0:
      starting_height += 1
    if starting_height == self.height - 1:
      starting_height -= 1
    if starting_width == 0:
      starting_width += 1
    if starting_width == self.width - 1:
      starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    self.maze_data[starting_height][starting_width] = self.cell
    walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
             [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

    # Denote walls in maze
    self.maze_data[starting_height - 1][starting_width] = 'w'
    self.maze_data[starting_height][starting_width - 1] = 'w'
    self.maze_data[starting_height][starting_width + 1] = 'w'
    self.maze_data[starting_height + 1][starting_width] = 'w'

    while walls:
      # Pick a random wall
      rand_wall = walls[int(random.random() * len(walls)) - 1]

      # Check if it is a left wall
      if rand_wall[1] != 0:
        if (self.maze_data[rand_wall[0]][rand_wall[1] - 1] == 'u' and self.maze_data[rand_wall[0]][
          rand_wall[1] + 1] == 'c'):
          # Find the number of surrounding cells
          s_cells = self.surrounding_cells(rand_wall)

          if s_cells < 2:
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            # Upper cell
            if rand_wall[0] != 0:
              if self.maze_data[rand_wall[0] - 1][rand_wall[1]] != 'c':
                self.maze_data[rand_wall[0] - 1][rand_wall[1]] = 'w'
              if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] - 1, rand_wall[1]])

            # Bottom cell
            if rand_wall[0] != self.height - 1:
              if self.maze_data[rand_wall[0] + 1][rand_wall[1]] != 'c':
                self.maze_data[rand_wall[0] + 1][rand_wall[1]] = 'w'
              if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] + 1, rand_wall[1]])

            # Leftmost cell
            if rand_wall[1] != 0:
              if self.maze_data[rand_wall[0]][rand_wall[1] - 1] != 'c':
                self.maze_data[rand_wall[0]][rand_wall[1] - 1] = 'w'
              if [rand_wall[0], rand_wall[1] - 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] - 1])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Check if it is an upper wall
      if rand_wall[0] != 0:
        if (self.maze_data[rand_wall[0] - 1][rand_wall[1]] == 'u' and self.maze_data[rand_wall[0] + 1][
          rand_wall[1]] == 'c'):

          s_cells = self.surrounding_cells(rand_wall)
          if s_cells < 2:
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            # Upper cell
            if rand_wall[0] != 0:
              if self.maze_data[rand_wall[0] - 1][rand_wall[1]] != 'c':
                self.maze_data[rand_wall[0] - 1][rand_wall[1]] = 'w'
              if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] - 1, rand_wall[1]])

            # Leftmost cell
            if rand_wall[1] != 0:
              if self.maze_data[rand_wall[0]][rand_wall[1] - 1] != 'c':
                self.maze_data[rand_wall[0]][rand_wall[1] - 1] = 'w'
              if [rand_wall[0], rand_wall[1] - 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] - 1])

            # Rightmost cell
            if rand_wall[1] != self.width - 1:
              if self.maze_data[rand_wall[0]][rand_wall[1] + 1] != 'c':
                self.maze_data[rand_wall[0]][rand_wall[1] + 1] = 'w'
              if [rand_wall[0], rand_wall[1] + 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] + 1])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Check the bottom wall
      if rand_wall[0] != self.height - 1:
        if (self.maze_data[rand_wall[0] + 1][rand_wall[1]] == 'u' and self.maze_data[rand_wall[0] - 1][
          rand_wall[1]] == 'c'):

          s_cells = self.surrounding_cells(rand_wall)
          if s_cells < 2:
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            if rand_wall[0] != self.height - 1:
              if self.maze_data[rand_wall[0] + 1][rand_wall[1]] != 'c':
                self.maze_data[rand_wall[0] + 1][rand_wall[1]] = 'w'
              if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] + 1, rand_wall[1]])
            if rand_wall[1] != 0:
              if self.maze_data[rand_wall[0]][rand_wall[1] - 1] != 'c':
                self.maze_data[rand_wall[0]][rand_wall[1] - 1] = 'w'
              if [rand_wall[0], rand_wall[1] - 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] - 1])
            if rand_wall[1] != self.width - 1:
              if self.maze_data[rand_wall[0]][rand_wall[1] + 1] != 'c':
                self.maze_data[rand_wall[0]][rand_wall[1] + 1] = 'w'
              if [rand_wall[0], rand_wall[1] + 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] + 1])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Check the right wall
      if rand_wall[1] != self.width - 1:
        if (self.maze_data[rand_wall[0]][rand_wall[1] + 1] == 'u' and self.maze_data[rand_wall[0]][
          rand_wall[1] - 1] == 'c'):

          s_cells = self.surrounding_cells(rand_wall)
          if s_cells < 2:
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            if rand_wall[1] != self.width - 1:
              if self.maze_data[rand_wall[0]][rand_wall[1] + 1] != 'c':
                self.maze_data[rand_wall[0]][rand_wall[1] + 1] = 'w'
              if [rand_wall[0], rand_wall[1] + 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] + 1])
            if rand_wall[0] != self.height - 1:
              if self.maze_data[rand_wall[0] + 1][rand_wall[1]] != 'c':
                self.maze_data[rand_wall[0] + 1][rand_wall[1]] = 'w'
              if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] + 1, rand_wall[1]])
            if rand_wall[0] != 0:
              if self.maze_data[rand_wall[0] - 1][rand_wall[1]] != 'c':
                self.maze_data[rand_wall[0] - 1][rand_wall[1]] = 'w'
              if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] - 1, rand_wall[1]])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Delete the wall from the list anyway
      for wall in walls:
        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
          walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, self.height):
      for j in range(0, self.width):
        if self.maze_data[i][j] == 'u':
          self.maze_data[i][j] = 'w'

    # Set starting position of the player
    for i in range(0, self.width):
      if self.maze_data[1][i] == 'c':
        self.maze_data[0][i] = 's'
        self.starting_posX = 0
        self.starting_posY = i
        break

    # Set finish position of the maze
    for i in range(self.width - 1, 0, -1):
      if self.maze_data[self.height - 2][i] == 'c':
        self.maze_data[self.height - 1][i] = 'f'
        self.finish_posX = self.height - 1
        self.finish_posY = i
        break

  def get_maze(self):
    return self.maze_data

  # Takes players current position and checks if the desired player movement is valid
  def is_valid_move(self, player_posX, player_posY, order):
    # w stands for wall

    # Left
    if order == "a":
      return self.maze_data[player_posX][player_posY - 1] == "w"

    # Down
    elif order == "s":
      return self.maze_data[player_posX + 1][player_posY] == "w"

    # Right
    elif order == "d":
      return self.maze_data[player_posX][player_posY + 1] == "w"

    # Up
    elif order == "w":
      return self.maze_data[player_posX - 1][player_posY] == "w"

    # invalid input
    else:
      return False
