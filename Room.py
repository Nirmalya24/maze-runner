import random
import Maze

class Room:
  def __init__(self, client_socket):
    self.roomID = self.create_room()
    self.players = []
    self.spectators = []
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
    if len(self.players < 2):
      self.players.append(player)
      return True
    
    return False

  def get_players(self):
    return self.players

  def get_spectator(self):
    return self.spectators

  def set_maze(self, maze_data):
    self.maze = maze_data

  def get_maze(self):
    return self.maze

  def join_as_spectator(self, user):
    self.spectators.append(user)

  def isEmpty(self):
    if len(self.players) > 2:
      return False
    return True





    


