import socket
import threading
import auth
import time
import json

class ThreadedServer(object):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind((self.host, self.port))
    print("[SERVER STARTED]")

  def listen(self):
    self.server_socket.listen(5)
    while True:
      client, address = self.server_socket.accept()
      print("[CLIENT CONNECTED]", address)
      client.settimeout(60)
      threading.Thread(target = self.listen_to_client,args = (client,address)).start()
  
  def listen_to_client(self, client, address):
    client.send(str.encode("\nWelcome to the server!\n"))
    time.sleep(0.1)
    client.send(str.encode("0"))
    SIZE = 2048
    while True:
      try:
        data = client.recv(SIZE).decode()
        if not data or data == "exit":
          print("[CLIENT DISCONNECTED] Closing connection", address)
          client.close()
          break
        # Receive data from client
        if data == "0":
          """
          Welcome Menu
          Press 1 to Login
          Press 2 to Register
          Type exit to disconnect
          """
          client.send(str.encode("0"))
        elif data == "1":
          """
          Login dialog
          Getting Username and Password for Login
          """
          # Send Login menu code to client
          client.send(str.encode("1"))
          # Login
          username = client.recv(SIZE).decode()
          password = client.recv(SIZE).decode()
          print(f"[LOGIN] {username} | {password}")
          # Check if username in users.json
          if auth.check_user_exist(username) == False:
            client.send(str.encode("5"))
            print("[LOGIN FAILED] Username does not exist")
          else:
            # Check if password is correct
            print("Checking password...")
            if auth.check_user_password(username, password) == False:
              client.send(str.encode("6"))
              print("[LOGIN FAILED] Password is incorrect")
            else:
              client.send(str.encode("3"))
              print("[LOGIN SUCCESS]", username)
        elif data == "2":
          """
          Register dialog
          Getting Username and Password for Registration
          """
          # Send Register menu code to client
          client.send(str.encode("2"))
          # Register
          username = client.recv(SIZE).decode()
          password = client.recv(SIZE).decode()
          print(f"[REGISTER] {username} | {password}")
          # Check if username in users.json
          if auth.check_user_exist(username) == True:
            client.send(str.encode("4"))
            print("[REGISTER FAILED] Username already exists")
          else:
            # Add user to users.json
            auth.add_user(username, password)
            client.send(str.encode("7"))
            print("[REGISTER SUCCESS]", username)
        elif data == "3":
          """
          Game Menu
          Press 1 to see high scores
          Press 2 to see game rules
          Press 3 to play/view a game
          Type exit to disconnect
          """
          client.send(str.encode("3"))
        elif data == "8":
          """
          High scores dialog
          Press 1 to see top 5 records
          Press 2 to see my record
          """
          client.send(str.encode("8"))
        elif data == "9":
          """
          Game rules dialog
          The client will see the game rules
          """
          rules= ""
          rules += ("Game Rules\n")
          rules += ("\nDisplay:")
          rules += ("\nEach game, you and your opponent will start with a unique "
                + "maze. You will be\nable to see your opponent's progress on "
                + "the side maze map in live.\n👀 indicates your location; 👻 "
                + "indicates your opponent's; 🏁 indicates\nthe exit.\n")
          rules += ("\nInstructions:")
          rules += ("\nPress \"W\" to go up, \"A\" to go left, \"S\" to go down, "
                + "and \"D\" to go right. You\nwon't be able to move if you hit "
                + "a wall. Your goal is to reach the exit point\nbefore your "
                + "opponent. You will automatically be sent back to the lobby "
                + "if you\nidle for 5 secones during the game.\n")
          rules += ("\nScores:")
          rules += ("\nThe time you spent on each round is your score. A timer "
                + "will start when the\ngame begins and stop as soon as you "
                + "reach the exit point. Your best score\nwill be updated to "
                + "the record board where you may visit from Game Menu.\n")
          client.send(str.encode(rules))
        elif data == "10":
          """
          Game
          The client will play/see a game
          """
          client.send(str.encode("10"))
        elif data == "11":
          """
          Display top 5 records
          """
          display = ""
          file = "scores.json"
          with open(file, "r") as scores :
            record = json.load(scores)
            rank = ["First", "Second", "Third", "Fourth", "Fifth"]
            for i in range(0, 5) :
              display += (rank[i] + " place:\t" + record[i]["name"] 
                          + " in " + str(record[i]["time"]) + " seconds!\n")
            scores.close
          client.send(str.encode(display))  
        elif data == "12":
          """
          Display player's top record
          """
          name = "mazeRunner"   #user.get_name PENDING USER CLASS
          display = ""
          with open(file, "r") as scores :
            record = json.load(scores)
            found = False
            for ele in record :
              if ele["name"] == name :
                display += (ele["name"] + "'s best score: " 
                            + str(ele["time"]) + " seconds.\n")
                found = True
                break
            if not found :
              display = (name + " is not found in record.\n")
            scores.close
          client.send(str.encode(display))
          
      except:
        client.close()
        return False

if __name__ == "__main__":
  while True:
    PORT = input("Port: ")
    try:
      PORT = int(PORT)
      break
    except ValueError:
      print("Invalid port number")
  HOST = socket.gethostbyname(socket.gethostname())
  ThreadedServer(HOST, PORT).listen()