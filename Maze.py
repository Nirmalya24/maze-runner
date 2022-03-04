# Maze generator -- Randomized Prim Algorithm

## Imports
import random
import time
import os

class Maze:

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.maze_data = self.generateMaze()
    self.start = (0, 0)
    self.end = (0, 0)
    self.wall = 'w'
    self.cell = 'c'
    self.unvisited = 'u'
    self.visited = []
    self.path = []
    # Player position
    self.starting_posX = -1
    self.starting_posY = -1
    # Finish position
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

  def printMaze(self):
  # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, self.height):
      for j in range(0, self.width):
        if (self.maze_data[i][j] == 'u'):
          print(" u", end=" ")
        elif (self.maze_data[i][j] == 'c'):
          print("  ", end=" ")
        elif (self.maze_data[i][j] == 'f'):
          print(self.FINISH, end=" ")
        elif (self.maze_data[i][j] == 's'):
          print(self.PLAYER, end=" ")
        else:
          print(self.MAZE_WALL, end=" ")
        
      print('\n')

  # Find number of surrounding cells
  def surroundingCells(self, rand_wall):
    s_cells = 0
    if (self.maze_data[rand_wall[0]-1][rand_wall[1]] == 'c'):
      s_cells += 1
    if (self.maze_data[rand_wall[0]+1][rand_wall[1]] == 'c'):
      s_cells += 1
    if (self.maze_data[rand_wall[0]][rand_wall[1]-1] == 'c'):
      s_cells +=1
    if (self.maze_data[rand_wall[0]][rand_wall[1]+1] == 'c'):
      s_cells += 1

    return s_cells
  
  # Maze generation algorithm
  def _generateMaze(self):
    # Denote all cells as unvisited
    for i in range(0, self.height):
      line = []
      for j in range(0, self.width):
        line.append(self.unvisited)
      self.maze_data.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random()*self.height)
    starting_width = int(random.random()*self.width)
    if (starting_height == 0):
      starting_height += 1
    if (starting_height == self.height-1):
      starting_height -= 1
    if (starting_width == 0):
      starting_width += 1
    if (starting_width == self.width-1):
      starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    self.maze_data[starting_height][starting_width] = self.cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    self.maze_data[starting_height-1][starting_width] = 'w'
    self.maze_data[starting_height][starting_width - 1] = 'w'
    self.maze_data[starting_height][starting_width + 1] = 'w'
    self.maze_data[starting_height + 1][starting_width] = 'w'

    while (walls):
      # Pick a random wall
      rand_wall = walls[int(random.random()*len(walls))-1]

      # Check if it is a left wall
      if (rand_wall[1] != 0):
        if (self.maze_data[rand_wall[0]][rand_wall[1]-1] == 'u' and self.maze_data[rand_wall[0]][rand_wall[1]+1] == 'c'):
          # Find the number of surrounding cells
          s_cells = self.surroundingCells(rand_wall)

          if (s_cells < 2):
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            # Upper cell
            if (rand_wall[0] != 0):
              if (self.maze_data[rand_wall[0]-1][rand_wall[1]] != 'c'):
                self.maze_data[rand_wall[0]-1][rand_wall[1]] = 'w'
              if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                walls.append([rand_wall[0]-1, rand_wall[1]])


            # Bottom cell
            if (rand_wall[0] != self.height-1):
              if (self.maze_data[rand_wall[0]+1][rand_wall[1]] != 'c'):
                self.maze_data[rand_wall[0]+1][rand_wall[1]] = 'w'
              if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                walls.append([rand_wall[0]+1, rand_wall[1]])

            # Leftmost cell
            if (rand_wall[1] != 0):	
              if (self.maze_data[rand_wall[0]][rand_wall[1]-1] != 'c'):
                self.maze_data[rand_wall[0]][rand_wall[1]-1] = 'w'
              if ([rand_wall[0], rand_wall[1]-1] not in walls):
                walls.append([rand_wall[0], rand_wall[1]-1])
          

          # Delete wall
          for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
              walls.remove(wall)

          continue

      # Check if it is an upper wall
      if (rand_wall[0] != 0):
        if (self.maze_data[rand_wall[0]-1][rand_wall[1]] == 'u' and self.maze_data[rand_wall[0]+1][rand_wall[1]] == 'c'):

          s_cells = self.surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            # Upper cell
            if (rand_wall[0] != 0):
              if (self.maze_data[rand_wall[0]-1][rand_wall[1]] != 'c'):
                self.maze_data[rand_wall[0]-1][rand_wall[1]] = 'w'
              if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                walls.append([rand_wall[0]-1, rand_wall[1]])

            # Leftmost cell
            if (rand_wall[1] != 0):
              if (self.maze_data[rand_wall[0]][rand_wall[1]-1] != 'c'):
                self.maze_data[rand_wall[0]][rand_wall[1]-1] = 'w'
              if ([rand_wall[0], rand_wall[1]-1] not in walls):
                walls.append([rand_wall[0], rand_wall[1]-1])

            # Rightmost cell
            if (rand_wall[1] != self.width-1):
              if (self.maze_data[rand_wall[0]][rand_wall[1]+1] != 'c'):
                self.maze_data[rand_wall[0]][rand_wall[1]+1] = 'w'
              if ([rand_wall[0], rand_wall[1]+1] not in walls):
                walls.append([rand_wall[0], rand_wall[1]+1])

          # Delete wall
          for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
              walls.remove(wall)

          continue

      # Check the bottom wall
      if (rand_wall[0] != self.height-1):
        if (self.maze_data[rand_wall[0]+1][rand_wall[1]] == 'u' and self.maze_data[rand_wall[0]-1][rand_wall[1]] == 'c'):

          s_cells = self.surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            if (rand_wall[0] != self.height-1):
              if (self.maze_data[rand_wall[0]+1][rand_wall[1]] != 'c'):
                self.maze_data[rand_wall[0]+1][rand_wall[1]] = 'w'
              if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                walls.append([rand_wall[0]+1, rand_wall[1]])
            if (rand_wall[1] != 0):
              if (self.maze_data[rand_wall[0]][rand_wall[1]-1] != 'c'):
                self.maze_data[rand_wall[0]][rand_wall[1]-1] = 'w'
              if ([rand_wall[0], rand_wall[1]-1] not in walls):
                walls.append([rand_wall[0], rand_wall[1]-1])
            if (rand_wall[1] != self.width-1):
              if (self.maze_data[rand_wall[0]][rand_wall[1]+1] != 'c'):
                self.maze_data[rand_wall[0]][rand_wall[1]+1] = 'w'
              if ([rand_wall[0], rand_wall[1]+1] not in walls):
                walls.append([rand_wall[0], rand_wall[1]+1])

          # Delete wall
          for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
              walls.remove(wall)


          continue

      # Check the right wall
      if (rand_wall[1] != self.width-1):
        if (self.maze_data[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze_data[rand_wall[0]][rand_wall[1]-1] == 'c'):

          s_cells = self.surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.maze_data[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            if (rand_wall[1] != self.width-1):
              if (self.maze_data[rand_wall[0]][rand_wall[1]+1] != 'c'):
                self.maze_data[rand_wall[0]][rand_wall[1]+1] = 'w'
              if ([rand_wall[0], rand_wall[1]+1] not in walls):
                walls.append([rand_wall[0], rand_wall[1]+1])
            if (rand_wall[0] != self.height-1):
              if (self.maze_data[rand_wall[0]+1][rand_wall[1]] != 'c'):
                self.maze_data[rand_wall[0]+1][rand_wall[1]] = 'w'
              if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                walls.append([rand_wall[0]+1, rand_wall[1]])
            if (rand_wall[0] != 0):	
              if (self.maze_data[rand_wall[0]-1][rand_wall[1]] != 'c'):
                self.maze_data[rand_wall[0]-1][rand_wall[1]] = 'w'
              if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                walls.append([rand_wall[0]-1, rand_wall[1]])

          # Delete wall
          for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
              walls.remove(wall)

          continue

      # Delete the wall from the list anyway
      for wall in walls:
        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
          walls.remove(wall)
      


    # Mark the remaining unvisited cells as walls
    for i in range(0, self.height):
      for j in range(0, self.width):
        if (self.maze_data[i][j] == 'u'):
          self.maze_data[i][j] = 'w'

    # Set starting position of the player
    for i in range(0, self.width):
      if (self.maze_data[1][i] == 'c'):
        self.maze_data[0][i] = 's'
        self.starting_posX = 0
        self.starting_posY = i
        break

    # Set finish position of the maze
    for i in range(self.width-1, 0, -1):
      if (self.maze_data[self.height-2][i] == 'c'):
        self.maze_data[self.height-1][i] = 'f'
        self.finish_posX = self.height - 1
        self.finish_posY = i
        break

  def get_maze(self):
    return self.maze_data

  def is_valid_move(self, player_posX, player_posY, order):
    x_move = -1
    y_move = -1
    # Player Movement

    # Illegal move
    INVALID_MOVE_TEXT = "Cannot go there"


    # Left
    if order == "a":
        y_move = self.player_posY - 1
        # if reach a wall then game over
        if self.maze_data[self.player_posX][y_move] == "w":
            print(INVALID_MOVE_TEXT)
            return False

        else:
            self.maze_data[self.player_posX][self.player_posY], self.maze_data[self.player_posX][y_move] = self.maze_data[self.player_posX][y_move], self.maze_data[self.player_posX][self.player_posY]
            self.player_posY = y_move
            self.printMaze()

    # Down
    elif order == "s":
        x_move = self.player_posX + 1
        if self.maze_data[x_move][self.player_posY] == "w":
            print(INVALID_MOVE_TEXT)
            return False
        else:
            self.maze_data[self.player_posX][self.player_posY], self.maze_data[x_move][self.player_posY] = self.maze_data[x_move][self.player_posY], self.maze_data[self.player_posX][self.player_posY]
            self.player_posX = x_move
            self.printMaze()

    # Right
    elif order == "d":
        y_move = self.player_posY + 1
        if self.maze_data[self.player_posX][y_move] == "w":
            print(INVALID_MOVE_TEXT)
            return False
        else:
            self.maze_data[self.player_posX][self.player_posY], self.maze_data[self.player_posX][y_move] = self.maze_data[self.player_posX][y_move], self.maze_data[self.player_posX][self.player_posY]
            self.player_posY = y_move
            self.printMaze()
            

    # Up
    elif order == "w":
        x_move = self.player_posX - 1
        if self.maze_data[x_move][self.player_posY] == "w":
            print(INVALID_MOVE_TEXT)
            return False
        else:
            self.maze_data[self.player_posX][self.player_posY], self.maze_data[x_move][self.player_posY] = self.maze_data[x_move][self.player_posY], self.maze_data[self.player_posX][self.player_posY]
            self.player_posX = x_move
            self.printMaze()

    # invalid input
    else:
        print("Please enter a valid letter (w,a,s,d)!")
        return False
    
    
    # Check if the player has reached the finish line
    if self.maze_data[self.player_posX][self.player_posY] == self.maze_data[self.finish_posX][self.finish_posY]:
        print("You win!")
        return True
  
  def startGame(self, player_posX, player_posY):
    self.printMaze()
    x_move = -1
    y_move = -1
    # Player Movement

    # Illegal move
    INVALID_MOVE_TEXT = "Cannot go there"

    while True:

        order = input("Please Enter (a: LEFT, s: DOWN, d: RIGHT, w: UP): ")

        # Left
        if order == "a":
            y_move = self.player_posY - 1
            # if reach a wall then game over
            if self.maze_data[self.player_posX][y_move] == "w":
                print(INVALID_MOVE_TEXT)
                continue

            else:
                self.maze_data[self.player_posX][self.player_posY], self.maze_data[self.player_posX][y_move] = self.maze_data[self.player_posX][y_move], self.maze_data[self.player_posX][self.player_posY]
                self.player_posY = y_move
                self.printMaze()

        # Down
        elif order == "s":
            x_move = self.player_posX + 1
            if self.maze_data[x_move][self.player_posY] == "w":
                print(INVALID_MOVE_TEXT)
                continue
            else:
                self.maze_data[self.player_posX][self.player_posY], self.maze_data[x_move][self.player_posY] = self.maze_data[x_move][self.player_posY], self.maze_data[self.player_posX][self.player_posY]
                self.player_posX = x_move
                self.printMaze()

        # Right
        elif order == "d":
            y_move = self.player_posY + 1
            if self.maze_data[self.player_posX][y_move] == "w":
                print(INVALID_MOVE_TEXT)
                continue
            else:
                self.maze_data[self.player_posX][self.player_posY], self.maze_data[self.player_posX][y_move] = self.maze_data[self.player_posX][y_move], self.maze_data[self.player_posX][self.player_posY]
                self.player_posY = y_move
                self.printMaze()
                

        # Up
        elif order == "w":
            x_move = self.player_posX - 1
            if self.maze_data[x_move][self.player_posY] == "w":
                print(INVALID_MOVE_TEXT)
                continue
            else:
                self.maze_data[self.player_posX][self.player_posY], self.maze_data[x_move][self.player_posY] = self.maze_data[x_move][self.player_posY], self.maze_data[self.player_posX][self.player_posY]
                self.player_posX = x_move
                self.printMaze()

        # invalid input
        else:
            print("Please enter a valid letter (w,a,s,d)!")
            continue
        
        
        # Check if the player has reached the finish line
        if self.maze_data[self.player_posX][self.player_posY] == self.maze_data[self.finish_posX][self.finish_posY]:
            print("You win!")
            break



# playerMaze = Maze(20, 10)
# playerMaze.generateMaze()
# playerMaze.startGame()