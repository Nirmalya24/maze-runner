import maze_generator

def clear_screen():
    import os
    os.system("clear")

# Get maze
maze = maze_generator.MazeGenerator(10, 10)
map_data = maze.get_maze()

# Init player's position
x = 0
y = 1
end_x = 9
end_y = 8

map_data[x][y] = 'X'

def print_map():
    #Clear Console
    clear_screen()
    for chars in map_data:
        for char in chars:
            if char == 'w':
                print(" •", end=" ")
            elif (char == ' '):
                print("  ", end=" ")
            else:
                print(" X", end=" ")
        print("")

x_move = -1
y_move = -1

# Player Movement
while True:

    print_map()
    order = input("\nPlease Enter (a: LEFT,s: DOWN, d:RIGHT, w:UP): ")

    # Left
    if order == "a":
        y_move = y - 1
        # if reach a wall then game over
        if map_data[x][y_move] == 'w':
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x][y_move] = map_data[x][y_move], map_data[x][y]
            y = y_move
            print_map()

    # Down
    elif order == "s":
        x_move = x + 1
        if map_data[x_move][y] == 'w':
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x_move][y] = map_data[x_move][y], map_data[x][y]
            x = x_move
            print_map()

    # Right
    elif order == "d":
        y_move = y + 1
        if map_data[x][y_move] == 'w':
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x][y_move] = map_data[x][y_move], map_data[x][y]
            y = y_move
            print_map()
            
    # Up
    elif order == "w":
        x_move = x - 1
        if map_data[x_move][y] == 'w':
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x_move][y] = map_data[x_move][y], map_data[x][y]
            x = x_move
            print_map()

    # invalid input
    else:
        print("Please enter a valid letter (w,a,s,d)!")
        continue
    
    # Check if the player has reached the finish line
    if map_data[x][y] == map_data[end_x][end_y]:
        print("\nYou win!\n")
        break