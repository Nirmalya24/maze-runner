# Read and write scores record with JSON

import json

# Add new player name and score pair to the score board
def new_score(name, time) :
    player = {
        "name" : name,
        "time" : time
    }
    updat_record(player)

# Read and re-write the updated record back to scores file
def updat_record(player, file = "scores.json") :
    with open(file, "r+") as scores :
        record = json.load(scores)
        insert_sorted_score(record, player)
        scores.seek(0)
        json.dump(record, scores)
        scores.close

# Insert the new record in ascending (time) order <or> 
# Update the better score for existing player
def insert_sorted_score(record, player) :

    # Insert score for existing player
    if exisit_player(record, player["name"]) :
        for ele in record :
            if ele["name"] == player["name"] and ele["time"] > player["time"] :
                    ele["time"] = player["time"]

    # Insert score for new player
    else :
        count = 0
        for ele in record :
            if ele["time"] < player["time"] :
                count += 1
            else :
                break
        record.insert(count, player)

# Check if player already exist
def exisit_player(record, name) :
    for ele in record :
        if ele["name"] == name :
            return True
    return False

# Run newScore("name", score) in server.py to add new record
new_score("mazeRunner", 7)

#/////////////////////////////////////////////////////////////////////////////#

def print_top_record(file = "scores.json") :
    with open(file, "r") as scores :
        record = json.load(scores)
        rank = ["First", "Second", "Third"]

        for i in range(0, 3) :
            print(rank[i] + " place: " + record[i]["name"] 
            + " in " + str(record[i]["time"]) + " seconds!\n")
        scores.close

# Run printTopRecord() in server.py to display top 3 winners
print_top_record()

#/////////////////////////////////////////////////////////////////////////////#

def get_my_record(name, file = "scores.json") :
    with open(file, "r") as scores :
        record = json.load(scores)

        found = False
        for ele in record :
            if ele["name"] == name :
                print(ele["name"] + "'s best score: " + str(ele["time"]) + " seconds.\n")
                found = True
                break
        if not found :
            print(name + " is not found in record.")
        scores.close

# Run get_my_record() in server.py to display player's best score
get_my_record("turtle")