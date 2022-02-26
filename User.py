from http import client
import Game

class User:
  def __init__(self, client_socket):
    self.isSpectator = True
    self.socket = client_socket
    self.username = client_socket.send(str.encode(";USERNAME;"))
    self.posX = -1
    self.posY = -1

  def set_player(self):
    self.isSpectator = False

  def set_spectator(self):
    self.isSpectator = True

  def player_move(self, x, y):
    pass

