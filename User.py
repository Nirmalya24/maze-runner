from http import client
import Game

class User:
  def __init__(self, client_socket):
    self.is_spectator = True
    self.socket = client_socket
    self.roomID = ""
    self.posX = -1
    self.posY = -1
    self.winner = False

    # Get the username from the server
    self.socket.send(str.encode(";USERNAME;"))
    self.username = self.socket.recv(2048).decode()

  def get_username(self):
    return self.username

  # Set the user as a player
  def set_player(self):
    self.is_spectator = False

  # Set the user as a spectator
  def set_spectator(self):
    self.is_spectator = True

  # Set the user RoomID to the given roomID
  def set_roomID(self, roomID):
    self.roomID = roomID

  """
  Player Movement Functions
  """

  def set_posX(self, x):
    self.posX = x

  def set_posY(self, y):
    self.posY = y

  def get_posX(self):
    return self.posX
  
  def get_posY(self):
    return self.posY

  def get_pos(self):
    return [self.posX, self.posY]
  
  def set_winner(self, winner):
    self.winner = winner


