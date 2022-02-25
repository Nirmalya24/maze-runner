import random
import Maze

class Room:
  def __init__(self, client_socket):
    self.roomID = self.create_room
    self.players = []
    self.mazeGame = Maze(20, 10)
    self.finished = False

  def create_room(self):
    room_code = ""
    for i in range(3):
      room_code += chr(random.randint(ord('A'), ord('Z')))
    
    return room_code

  def get_roomID(self):
    return self.roomID

  def add_player(self, player):
    self.players.append(player)

  def get_players(self):
    return self.players

  def set_maze(self, maze_data):
    self.maze = maze_data

  def get_maze(self):
    return self.maze





    


