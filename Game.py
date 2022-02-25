import Room

class Game:
  def __intit__(self):
    self.rooms = []

  def create_room(self):
    self.rooms.append(Room.create_room())

  def delete_room(self, roomID):
    for i in range(len(self.rooms)):
      if self.rooms[i].roomID == roomID:
        del self.rooms[i]

  def _find_empty_room(self):
    for i in range(len(self.rooms)):
      if self.rooms[i].isEmpty():
        return self.rooms[i]

  def add_player_to_room(self, player):
    room = self.find_empty_room()
    room.add_player(player)

  def show_ongoing_games(self):
    return self.rooms
    
