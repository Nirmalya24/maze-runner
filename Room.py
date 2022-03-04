import random
import Maze


class Room:
  def __init__(self):
    self.roomID = self.create_room()
    self.players = {}
    self.spectators = {}
    self.mazeGame = Maze.Maze(20, 10)
    self.finished = False
    self.started = True

  """
  Room Functions
  """

  # Creates a room with a random 3-letter code and returns it.
  @staticmethod
  def create_room():
    room_code = ""
    for i in range(3):
      room_code += chr(random.randint(ord('A'), ord('Z')))

    return room_code

  # Returns the roomID
  def get_room_id(self):
    return self.roomID

  # Check if the room is empty
  # If the room has less than 2 players, the room is considered empty
  def is_empty(self):
    if len(self.players) < 2:
      return True
    return False

  # Mark room as finished
  def room_finished(self):
    self.finished = True

    # Set player positions to -1
    for player in self.players:
      player.set_posX(-1)
      player.set_posY(-1)

  # Check if the room has finished the game
  def is_finished(self):
    return self.finished and self.started

  """
  User Functions (player/spectator)
  """

  # Add a user as a player to the room
  # Returns True if the user was added, False otherwise
  def add_player(self, user):
    user.set_player()  # Change the user to a player
    if len(self.players) < 2:
      self.players[user.get_username()] = user
      # TODO Update player position to starting position
      self.players[user.get_username()].posX, self.players[user.get_username()].posY = self.mazeGame.get_start_pos()
      return True
    return False

  # Add a user as a spectator to the room
  # Returns True if the user was added, False otherwise
  def add_spectator(self, user):
    user.set_spectator()  # Change the user to a spectator
    # Add spectator to the list of spectators
    self.spectators[user.get_username()] = user

  # Gets the list of players in the room
  # Returns a list of players
  def get_players(self):
    return self.players

  # Gets the list of spectators in the room
  # Returns the list of spectators in the room
  def get_spectators(self):
    return self.spectators

  """
  Player Functions
  """

  # Return a dictionary of the player positions in the room
  def get_player_positions(self):
    positions = {}
    for player in self.players:
      positions[player.get_username()] = (player.get_posX(), player.get_posY())
    return positions

  # Update player position
  def update_player_position(self, player_move, username):
    if player_move == "w":
      self.players[username].set_posX(self.players[username].get_posX() - 1)
    elif player_move == "s":
      self.players[username].set_posX(self.players[username].get_posX() + 1)
    elif player_move == "a":
      self.players[username].set_posY(self.players[username].get_posY() - 1)
    elif player_move == "d":
      self.players[username].set_posY(self.players[username].get_posY() + 1)

    # TODO: Check if the player has won the game
    self.check_win(username)

  """
  Maze functions
  """

  # Get the maze for the room
  # Returns the maze for the room
  def get_maze(self):
    return self.mazeGame.get_maze()

  # Returns True if the player has won the game, False otherwise
  def check_win(self, username):
    return self.players[username].get_pos() == self.mazeGame.get_finish_pos()

  def check_move(self, player_move, username):
    # DONE: Check if the player can move to the given position
    player_x, player_y = self.players[username].get_pos()
    return self.mazeGame.is_valid_move(player_x, player_y, player_move)
