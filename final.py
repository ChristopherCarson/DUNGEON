#FINAL PROJECT CST 205
#JOHN COFFELT, MICHAEL ROSE, RAUL RAMIREZ, CHRISTOPHER CARSON
#Goal of the game is to navigate the map using N,S,E,W to collect enough keys to open the door and escape the labyrinth.
#BEWARE OF MONSTERS!
#Monsters move around the map and will eat the player if the players lands on them or they land on the player.
import random

#GLOBAL VARIABLES
MAP_SIZE = 5 #Exponential, so MAP_SIZE = 4 would mean 16 squares and so on.
NUM_MONSTERS = 5 #Monsters that search for the player.
NUM_SPINNING_ROOMS = 2 #Spinning rooms send player off in random direction!
NUM_KEYS = 3 #Keys needed to unlock an escape door.
NUM_DOORS = 1 #Number of escape doors.

#Creates the blank map.                
def createMap(size):
   import random
   map = []
   for x in range(size):
     map.append([''] * size)
   return map

#Creates a shuffled array of map features so that they can be randomly placed on the map.
def createFeatureRandomSeed(mapSize, nMonsters, nSpinning_Rooms, nKeys, nDoors):            
   features = [0] * (mapSize ** 2)
   for i in range(0, mapSize ** 2):
     if nMonsters > 0:
       features[i] = "M"
       nMonsters -= 1
     elif nSpinning_Rooms > 0:
       features[i] = "S"
       nSpinning_Rooms -= 1
     elif nKeys > 0:
       features[i] = "K"
       nKeys -= 1
     elif nDoors > 0:
       features[i] = "D"
       nDoors -= 1
     else:
       features[i] = "E"
   random.shuffle(features)
   
   return features

#Places the randomized features onto the map.            
def addFeaturesToMap(map, features):
  index = 0  
  for x in range(len(map)):
    for y in range(len(map)):
      map[x][y] = features[index]
      index += 1
  return map    

#Determines a random start position for the player.
def getRandomStart(map):
  x = random.randint(0,len(map) - 1)
  y = random.randint(0,len(map) - 1)
  while map[x][y] != 'E':
    x = random.randint(0,len(map) - 1)
    y = random.randint(0,len(map) - 1)
  return {'X' : x, 'Y' : y}

#Takes player direction and returns true or false if that direction is valid.
def movePlayer(map, player_pos, direction):
  change = false
  if direction == 'N' and player_pos['Y'] + 1 < len(map):
    player_pos['Y'] =  player_pos['Y'] + 1
    change = true
  elif direction == 'S' and  player_pos['Y'] - 1 >= 0:
    player_pos['Y'] =  player_pos['Y'] - 1
    change = true
  elif direction == 'E' and  player_pos['X'] + 1 < len(map):
    player_pos['X'] =  player_pos['X'] + 1
    change = true
  elif direction == 'W' and  player_pos['X'] - 1 >= 0:
    player_pos['X'] =  player_pos['X'] - 1
    change = true
  return change

#Gets a random direction for the spinning room.
def getRandomDirection():
  direction = random.randint(0,3)
  if direction == 0:
    return 'S'
  elif direction == 1:
    return 'N'
  elif direction == 2:
    return 'W'
  elif direction == 3:
    return 'E'

#Moves the monsters around the map.
#Monsters can move in all directions, but will only move to featureless rooms.
def moveMonsters(map):
  for x in range(len(map)):
    for y in range(len(map)):
      if map[x][y] == 'M':
        spot_taken = true
        newX = 0
        newY = 0
        while newX >= len(map) or newX < 0 or newY >= len(map) or newY < 0 or spot_taken:
          newX = random.randint(-1,1) + x
          newY = random.randint(-1,1) + y
          if newX < len(map) and newX >= 0 and newY < len(map) and newY >= 0:
            if map[newX][newY] != 'E' and (newX != x or newY != y):
              spot_taken = true
            else:
              spot_taken = false             
        map[x][y] = 'E' #Set monster's current position to empty.
        map[newX][newY] = 'T' #Sets monsters new position to T to avoid the same monster moving twice.
  
  #Changes temp designation to M.
  for x in range(len(map)):
    for y in range(len(map)):
      if map[x][y] == 'T':
        map[x][y] = 'M'

#Display the map with a P for player's current position.
def printMap(map, player):
  current_room = game_map[player['X']][player['Y']]  
  map[player['X']][player['Y']] = 'P'
  
  for y in range(len(map)):
    for x in range(len(map)):
      print map[x][len(map) - y - 1],
    print '' 
  
  map[player['X']][player['Y']] = current_room

#Create the game map.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
blank_map = createMap(MAP_SIZE)
features = createFeatureRandomSeed(MAP_SIZE, NUM_MONSTERS, NUM_SPINNING_ROOMS, NUM_KEYS, NUM_DOORS)
game_map = addFeaturesToMap(blank_map, features)
player = getRandomStart(game_map)

#Start the game.
game_over = false
key_count = 0
printMap(game_map, player)
while game_over == false:
  move_direction = raw_input("Enter a direction (Ex. 'N','S','E','W'): ")
  
  player_moved = false
  if game_map[player['X']][player['Y']] == 'S': #Check for Spinning Room
    while not player_moved:
      move_direction = getRandomDirection()
      player_moved = movePlayer(game_map,player,move_direction)
  else:
    player_moved = movePlayer(game_map,player,move_direction.upper())                
  
  if player_moved:
    moveMonsters(game_map)
    if game_map[player['X']][player['Y']] == 'K': #GET THE KEY
      key_count += 1
      game_map[player['X']][player['Y']] = 'E'
    elif game_map[player['X']][player['Y']] == 'D' and key_count == NUM_KEYS: #WIN THE GAME!
      printNow("YOU WIN! You escaped the labyrinth!")
      game_over = true
    elif game_map[player['X']][player['Y']] == 'M': #OH NO MONSTER
      printNow("YOU LOSE! You were eaten by a monster! OH THE HORROR!")
      game_over = true
    printMap(game_map, player)
  else:
    printNow("Invalid move!")

  
