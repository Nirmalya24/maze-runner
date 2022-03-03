from sys import flags
import Room

class Game:
  """
  Constructor.
  Initializes a Game object with no rooms.
  """
  def __intit__(self):
    self.rooms = []

  
  # Creates a room and append it to the list of rooms.
  def create_room(self):
    new_room = Room.Room() # Create a new room

    # Check if the room already exists
    while self.find_room(new_room.get_roomID()):
      # Generate a new room if the room already exists
      new_room = Room.Room()
    # Add the room to the rooms list
    self.rooms.append(new_room)

  # Finds a room with the given roomID
  # returns True if the room exists, False otherwise
  def find_room(self, roomID):
    for i in range(len(self.rooms)):
      if self.rooms[i].get_roomID() == roomID:
        return True
    return False

  """
  Finds a room with the given roomID and checks if the room
  has finished playing the game.
  Deletes the room if it has finished and returns True.
  """
  def delete_room(self, roomID):
    for i in range(len(self.rooms)):
      if self.rooms[i].get_roomID() == roomID and self.rooms[i].is_finished():
        del self.rooms[i]
        return True
    return False

  # Private function. Returns a room that is empty
  def find_empty_room(self):
    for i in range(len(self.rooms)):
      if self.rooms[i].is_empty():
        return self.rooms[i]
    return []

  # Adds a user to a room as a player and returns the roomID.
  def join_as_player(self, player):
    room = self.find_empty_room()
    room.add_player(player)
    return room

  # Adds a user to a room as a spectator.
  def join_as_spectator(self, user, roomID):
    self.rooms[roomID].add_spectator(user)

  # Returns a list of all rooms that are full and not in finished state.
  def show_ongoing_games(self):
    ongoing = []
    for i in range(len(self.rooms)):
      if len(self.rooms[i].get_players()) == 2 and not self.rooms[i].is_finished():
        ongoing.append(self.rooms[i])
    
    return ongoing

