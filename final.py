#FINAL PROJECT CST 205
#JOHN COFFELT, MICHAEL ROSE, RAUL RAMIREZ, CHRISTOPHER CARSON
#Goal of the game is to navigate the map using W,A,S,D to collect enough keys to open the door and escape the labyrinth.
#BEWARE OF MONSTERS!
#Monsters move around the map and will eat the player if the players lands on them or they land on the player.
import random
import time
import java.awt.Font as Font

#GLOBAL VARIABLES
MAP_SIZE = 7 #Exponential, so MAP_SIZE = 4 would mean 16 squares and so on.
NUM_MONSTERS = 5 #Monsters that search for the player.
NUM_SPINNING_ROOMS = 2 #Spinning rooms send player off in random direction!
NUM_KEYS = 3 #Keys needed to unlock an escape door.
NUM_DOORS = 1 #Number of escape doors.
NUM_DEMON = 1 #Number of evil chasing demons

#Creates the blank map.                
def createMap(size):
   import random
   map = []
   for x in range(size):
     map.append([''] * size)
   return map

#Creates a shuffled array of map features so that they can be randomly placed on the map.
def createFeatureRandomSeed(mapSize, nMonsters, nSpinning_Rooms, nKeys, nDoors, nDemons):            
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
     elif nDemons > 0:#demon stuff
       features[i] = "C"
       nDemons -= 1
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
  if direction == 'W' and player_pos['Y'] + 1 < len(map):
    player_pos['Y'] =  player_pos['Y'] + 1
    change = true
  elif direction == 'S' and  player_pos['Y'] - 1 >= 0:
    player_pos['Y'] =  player_pos['Y'] - 1
    change = true
  elif direction == 'D' and  player_pos['X'] + 1 < len(map):
    player_pos['X'] =  player_pos['X'] + 1
    change = true
  elif direction == 'A' and  player_pos['X'] - 1 >= 0:
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
#Move the demon towards the player
#This may still have infinite loop bugs in the marked part will test throughout day
def moveDemon(map,player):
  playerX = player['X']
  playerY = player['Y']
  for x in range(len(map)):
    for y in range(len(map)):
      if map[x][y] == 'C':
        spot_taken = true
        demonX = 0
        demonY = 0
        while demonX >= len(map) or demonX < 0 or demonY >= len(map) or demonY < 0 or spot_taken:
          if playerX - x > 0 and map[x+1][y] == 'E':#player is to right
            demonX = x + 1 #move right

          elif playerX - x < 0 and map[x-1][y] == 'E':#player is to left
            demonX = x - 1 #move left
          else:
            demonX = x
          if playerY - y > 0 and map[x][y+1] == 'E':#player is above
            demonY = y + 1
          elif playerY - y < 0 and map[x][y-1] == 'E': #player is below
            demonY = y - 1
          else:
            demonY = y
          if demonX < len(map) and demonX >= 0 and demonY < len(map) and demonY >= 0:
          #infinite loop bugs here. possibly fixed but needs more testing
            if (map[demonX][demonY] != 'E' or map[demonX][demonY] != 'E') and (demonX != x or demonY != y):
              demonX = x
              demonY = y
              spot_taken = false
            else:
              spot_taken = false
        map[x][y] = 'E' #Set demon's current position to empty.
        map[demonX][demonY] = 'T' #Sets demon's new position to T. not sure if needed just copied the monster move function
  
  #Changes temp designation to C.
  for x in range(len(map)):
    for y in range(len(map)):
      if map[x][y] == 'T':
        map[x][y] = 'C'
  
  
  
#Function to grab tile from tileset and copy it into world
def tileCopy(source, sourceX, sourceY, target, targetX, targetY):
  new_y = targetY - 1
  for y in range (sourceY,sourceY+32):
    if new_y < getHeight(target)-1:
      new_y = new_y + 1
      new_x = targetX - 1
    for x in range (sourceX, sourceX+32):
      if new_x < getWidth(target)-1:
        new_x = new_x + 1
      original=getPixel(source, x, y)
      new=getPixel(target, new_x, new_y)
      color=getColor(original)
      setColor(new, color)
  return target

def deathColoredGlasses(pic):
  pixels = getPixels(pic)
  for p in pixels:
    b = getBlue(p)
    setBlue(p, b*.5)
    g = getGreen(p)
    setGreen(p, g*.5)
    r = getRed(p)
    setRed(p, r*2)
  return pic
  
#Function to color a picture completely black
def turnBlack(pic):
  pixels = getPixels(pic)
  for i in pixels:
    setBlue(i,0)
    setGreen(i,0)
    setRed(i,0)
  return pic

#Create a blank "world" and turn it black  
world = makeEmptyPicture(64 + (32*MAP_SIZE), 64 + (32*MAP_SIZE))
blackCanvas = makeEmptyPicture(32*MAP_SIZE, 32*MAP_SIZE)
blackCanvas = turnBlack(blackCanvas)

#Open up tile set
dir = os.path.dirname(__file__)#uses the parent folder of the program
path = dir + "\\"+"DUNGEON.png"#creates a pathway with the desired file name
tile = makePicture(path)

#Create stone walls around edge of world
for x in range (0,MAP_SIZE+2):
  for y in range (0,2):
    tileCopy(tile, 448, 64, world, 1+(x*32), 1+(32*(MAP_SIZE+1)*y))
for x in range (0,MAP_SIZE+1):
  for y in range (0,2):
    tileCopy(tile, 448, 64, world, 1+(32*(MAP_SIZE+1)*y) , 1+(32*x))
show(world)

translate = []
u = MAP_SIZE-1
for s in range (MAP_SIZE):
  translate.append(u) #This translates the y postition of the player for the graphics
  u -= 1
  
#Display the map with a P for player's current position.
def printMap(map, player):
  current_room = game_map[player['X']][player['Y']]  
  map[player['X']][player['Y']] = 'P'
  copyInto(blackCanvas, world, 32, 32)#Set the middle of the room black
    
    #Add Graphics to room
  for y in range(len(map)):
    for x in range(len(map)):
      if map[x][len(map) - y - 1] == 'D':
        tileCopy(tile, 800, 160, world, 32+(32*x), 32+(32*y))
      elif map[x][len(map) - y - 1] == 'K':
        tileCopy(tile, 224, 256, world, 32+(32*x), 32+(32*y))
      elif map[x][len(map) - y - 1] == 'M':
        tileCopy(tile, 544, 416, world, 32+(32*x), 32+(32*y))
      elif map[x][len(map) - y - 1] == 'P':
        tileCopy(tile, 384, 320, world, 32+(32*x), 32+(32*y))   
      elif map[x][len(map) - y - 1] == 'S':
        tileCopy(tile, 256, 256, world, 32+(32*x), 32+(32*y)) 
      elif map[x][len(map) - y - 1] == 'C':
        tileCopy(tile, 800, 448, world, 32+(32*x), 32+(32*y))
        
  map[player['X']][player['Y']] = current_room
  
  #Animate the player at the end of move
  if game_map[player['X']][player['Y']] != 'S':#If he's not in a room spinner, normal animation
    for x in range(0,3):
      repaint(world)
      tileCopy(tile, 384+(32*x), 320, world, 32+(32*player['X']), 32+(32*translate[player['Y']]))
      time.sleep(.15)
  else:#Else, give him a spinner animation
    for x in range(0,3):
      repaint(world)
      tileCopy(tile, 384+(32*x), 480, world, 32+(32*player['X']), 32+(32*translate[player['Y']]))
      time.sleep(.15)

  repaint(world)
  
def createText(picture, text, size, x, y, c):
  myFont = makeStyle("Blackadder ITC", Font.BOLD, size) #you can change the font to anything in java awt
  if c == 0: addTextWithStyle(picture, x, y, text, myFont, yellow)
  else: addTextWithStyle(picture, x, y, text, myFont, red)
  
#Create the game map.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
blank_map = createMap(MAP_SIZE)
features = createFeatureRandomSeed(MAP_SIZE, NUM_MONSTERS, NUM_SPINNING_ROOMS, NUM_KEYS, NUM_DOORS, NUM_DEMON)
game_map = addFeaturesToMap(blank_map, features)
player = getRandomStart(game_map)

#Start the game.
game_over = false
death = false
win = false
key_count = 0
turncounter = 0 #turn counter
demonCounter = 20 #turns until demon becomes active
printMap(game_map, player)
print """Welcome to the dungeon! The goal is to navigate the map using W,A,S,D to collect enough keys to open the door and escape the labyrinth.\nBEWARE OF MONSTERS!
Monsters move around the map and will eat the player if you are on the same space as them.\nThe resident demon seems to be watching your progress with amusement. Better move quickly before he gets bored of you...\nGood luck!"""
while game_over == false:
  move_direction = requestString("Enter a direction:\n'W' to go up\n'A' to go left\n'S' to go down\n'D' to go right")
  moveMonsters(game_map)
  
  player_moved = false
  if game_map[player['X']][player['Y']] == 'S': #Check for Spinning Room
    while not player_moved:
      move_direction = getRandomDirection()
      player_moved = movePlayer(game_map,player,move_direction)
  else:
    player_moved = movePlayer(game_map,player,move_direction.upper())                
  
  if player_moved:
    if game_map[player['X']][player['Y']] == 'K': #GET THE KEY
      key_count += 1
      game_map[player['X']][player['Y']] = 'E'
    elif game_map[player['X']][player['Y']] == 'D' and key_count == NUM_KEYS: #WIN THE GAME!
      #printNow("YOU WIN! You escaped the labyrinth!")
      game_over = true
      win = true
    elif game_map[player['X']][player['Y']] == 'M': #OH NO MONSTER
      #showInformation("YOU LOSE! You were eaten by a monster! OH THE HORROR!")
      death = true
      game_over = true
    if turncounter == demonCounter/2:
      print "The demon seems to be losing interest. Better hurry up!"
    if turncounter == demonCounter:
      print "The demon is no longer amused by your presence and begins chasing you!"
    if turncounter >= demonCounter:#starts moving the demon after a certain turn count
      moveDemon(game_map,player)
    
    if game_map[player['X']][player['Y']] == 'C': #OH NO DEMON!!!!
      death = true
      game_over = true

    printMap(game_map, player)
    turncounter += 1 #increment turn counter
    if death == true and win != true:
      tileCopy(tile, 320, 128, world, 32+(32*player['X']), 32+(32*translate[player['Y']]))
      world = deathColoredGlasses(world)
      repaint(world)
      time.sleep(1)
      turnBlack(world)
      tileCopy(tile, 320, 128, world, 32+(32*player['X']), 32+(32*translate[player['Y']]))
      createText(world, "You're dead!", 40, 20, 50, 1)
      repaint(world)
    if win == true and death != true:
      turnBlack(world)
      tileCopy(tile, 384, 320, world, 100, 100)
      repaint(world)
      time.sleep(1)
      y = 0
      while y < 70:
        y += 10
        turnBlack(world)
        tileCopy(tile, 384, 320, world, 100, 100)
        tileCopy(tile, 672, 416, world, 100, y)
        repaint(world)
      turnBlack(world)
      tileCopy(tile, 960, 352, world, 100, 100)
      repaint(world)
      time.sleep(.5)
      turnBlack(world)
      tileCopy(tile, 992, 352, world, 100, 100)
      createText(world, "You win!", 40, 20, 50, 0)
      repaint(world)     
      
      
  else:
    printNow("Invalid move!")

  
