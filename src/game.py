"""
Game class
"""

from math import ceil
import os
import time
import signal
import city
import army
import functools
import json

class CommandError(Exception):
  pass

class Game():
  def extract_map_information(self):
    cityFile = open(self.mapFile, "r")
    aLine = "#"
    while aLine[0] == "#":
      aLine = cityFile.readline()
    self.width = int(aLine.split()[0])
    self.height = int(aLine.split()[1])
    aLine = "#"
    while aLine[0] == "#":
      aLine = cityFile.readline()
    self.numCities = int(aLine)
    self.cities = []
    self.cityLines = []
    for aLine in cityFile:
      if aLine[0] == "#":
        continue
      self.cityLines.append(aLine)
      cityInfo = aLine.split()
      self.cityIDs.append(int(cityInfo[0]))
      if cityInfo[3] == "1":
        self.p1ChosenCity = int(cityInfo[0])
      if cityInfo[3] == "2":
        self.p2ChosenCity = int(cityInfo[0])
      cityInfo = list(map(int, cityInfo[:4])) + list(cityInfo[4]) + list(map(int, cityInfo[5:]))
      newCity = city.City(cityInfo[0], (cityInfo[1:3]), cityInfo[3], cityInfo[4], cityInfo[5], (cityInfo[6:]))
      self.cities.append(newCity)
      self.cityDictionary[int(cityInfo[0])] = newCity
  
  def __init__(self, mapFile = None, player1Command = None, player2Command = None, maxturn = 250, jsonFile = None, _debugMode = False):
    self.debugMode = _debugMode
    self.cities = []
    self.cityDictionary = {}
    self.cityIDs = []
    self.armies = []
    self.lastArmyID = 0
    self.width = 0
    self.height = 0
    self.numCities = 0
    self.mapFile = mapFile
    self.numMaxTurn = int(maxturn)
    self.currentTurn = 1
    self.jsonss = []
    self.jsonObjectsArray = []
    self.jsonFileName = jsonFile
    if player1Command == None or player2Command == None:
      print ("--player1 play.out")
      exit()
    if mapFile != None:
      self.extract_map_information()
    else:
      print ("map file name is not given")
      exit()
    if jsonFile == None:
      print ("json file not given")
      exit()
    self.p1Comm = player1Command
    self.p2Comm = player2Command

  def appendJsonFile(self, firstTurn = False):
    cityArray = []
    armyArray = []
    for aCity in self.cities:
      newDict = {}
      for aKey in aCity.__dict__.keys():
        if firstTurn:
          if aKey == "cityID":
            newDict["cID"] = aCity.__dict__[aKey]
          elif aKey == "coordinates":
            newDict["co"] = aCity.__dict__[aKey]
          elif aKey == "ownerID":
            newDict["oID"] = aCity.__dict__[aKey]
          elif aKey == "currentSoldiers":
            newDict["cS"] = aCity.__dict__[aKey]
          elif aKey == "productionType":
            newDict["pT"] = aCity.__dict__[aKey]
          elif aKey == "productionAmount":
            newDict["pA"] = aCity.__dict__[aKey]
        elif aKey == "ownerID":
          newDict["oID"] = aCity.__dict__[aKey]
        elif aKey == "currentSoldiers":
          newDict["cS"] = aCity.__dict__[aKey]
      cityArray.append(newDict)
    for anArmy in self.armies:
      newDict = {}
      for aKey in anArmy.__dict__.keys():
        if aKey == "ownerID":
          newDict["oID"] = anArmy.__dict__[aKey]
        elif aKey == "currentCoordinates":
          newDict["cC"] = anArmy.__dict__[aKey]
        elif aKey == "currentSoldiers":
          newDict["cS"] = anArmy.__dict__[aKey]
      armyArray.append(newDict)
    self.jsonObjectsArray.append({"cities":cityArray, "armies": armyArray})
    # self.jsonss.append(json.dumps({"cities":cityArray, "armies": armyArray}))

  def setMap(self, mapFile = None):
    if mapFile != None:
      self.mapFile = mapFile
      self.extract_map_information()
    else:
      print ("map file name is not given")

  def startGame(self):
    (self.player1ReadIn, self.player1ReadOut) = os.pipe()
    (self.player1WriteIn, self.player1WriteOut) = os.pipe()
    (self.player2ReadIn, self.player2ReadOut) = os.pipe()
    (self.player2WriteIn, self.player2WriteOut) = os.pipe()

    if not self.debugMode:
      os.close(2)

    try:
      self.process1 = os.fork()
      if self.process1 == 0:
        # process of player1

        os.dup2(self.player1WriteIn, 0)
        os.dup2(self.player1ReadOut, 1)
        #os.close(2)

        os.close(self.player1ReadIn)
        os.close(self.player1ReadOut)
        os.close(self.player1WriteIn)
        os.close(self.player1WriteOut)
        os.close(self.player2ReadIn)
        os.close(self.player2ReadOut)
        os.close(self.player2WriteIn)
        os.close(self.player2WriteOut)

        os.chdir("/home/player1")
        try:
          os.execvp("sudo", ["sudo", "-u", "player1", "bash" , "-c"] + [self.p1Comm])
        except:
          pass
        exit()

      self.process2 = os.fork()
      if self.process2 == 0:
        # process of player2

        os.dup2(self.player2WriteIn, 0)
        os.dup2(self.player2ReadOut, 1)
        #os.close(2)

        os.close(self.player1ReadIn)
        os.close(self.player1ReadOut)
        os.close(self.player1WriteIn)
        os.close(self.player1WriteOut)
        os.close(self.player2ReadIn)
        os.close(self.player2ReadOut)
        os.close(self.player2WriteIn)
        os.close(self.player2WriteOut)

        os.chdir("/home/player2")
        try:
          os.execvp("sudo", ["sudo", "-u", "player2", "bash" , "-c"] + [self.p2Comm])
        except:
          pass
        exit()

      time.sleep(3)

      os.close(self.player1WriteIn)
      os.close(self.player1ReadOut)
      os.close(self.player2WriteIn)
      os.close(self.player2ReadOut)

      signal.signal(signal.SIGALRM, self.timeoutHandler)

      turn = 0
      winner = 0
      result = self.sendMapInformation()
      if result == "error on 1":
        print (2, end = "")
        exit()
      elif result == "error on 2":
        print (1, end = "")
        exit()

      while turn < self.numMaxTurn:
        if turn == 0:
          self.appendJsonFile(True)
        else:
          self.appendJsonFile()
        turnInfo = self.currentGameInfo(1)
        os.write(self.player1WriteOut, turnInfo.encode())
        signal.alarm(1)
        try:
          player1Commands = self.requestTurnMove(1)
          signal.alarm(0)
        except IOError:
          winner = (2, "timeout")
          break
        turnInfo = self.currentGameInfo(2)
        os.write(self.player2WriteOut, turnInfo.encode())
        signal.alarm(1)
        try:
          player2Commands = self.requestTurnMove(2)
          signal.alarm(0)
        except IOError:
          winner = (1, "timeout")
          break
        if self.executeOrders(1, player1Commands) == "error":
          winner = (2, "wrong move")
          break
        if self.executeOrders(2, player2Commands) == "error":
          winner = (1, "wrong move")
          break
        self.makeTurnMoves()
        if not self.isAlive(1):
          winner = (2, "dead")
          break
        if not self.isAlive(2):
          winner = (1, "dead")
          break
        turn += 1
      time.sleep(1)
    except:
      pass
    os.system("sudo kill -9 " + str(self.process1))
    os.system("sudo kill -9 " + str(self.process2))
    if winner == 0:
      results = self.countSoldiers()
      if results[0] < results[1]:
        winner = (2, "soldier count")
        print ("the winner is:2")
      elif results[0] > results[1]:
        winner = (1, "soldier count")
        print ("the winner is:1")
      else:
        winner = (0, "draw")
        print ("the winner is:0")
    else:
      print ("the winner is:" +str(winner[0]))
    if self.jsonFileName.startswith("/var/www/aic/games/duel"):
    	self.jSonFile = open(str(self.jsonFileName[:-4] + "_" + str(winner[0]) + ".txt"),"w")
    else:
        self.jSonFile = open(self.jsonFileName, "w")
    self.jSonFile.write(json.dumps({"turns": self.jsonObjectsArray}))
    if winner != 0:
      pass
    else:
      pass

  def isAlive(self, playerNo):
    for aCity in self.cities:
      if aCity.getOwner() == playerNo:
        return True
    for anArmy in self.armies:
      if anArmy.getOwnerID() == playerNo:
        return True
    return False

  def countSoldiers(self):
    (frst, scnd) = [0,0]
    for aCity in self.cities:
      if aCity.getOwner() == 1:
        soldiers = aCity.getSoldiers()
        frst += soldiers[0]
        frst += soldiers[1]
        frst += soldiers[2]
      elif aCity.getOwner() == 2:
        soldiers = aCity.getSoldiers()
        scnd += soldiers[0]
        scnd += soldiers[1]
        scnd += soldiers[2]
    for anArmy in self.armies:
      if anArmy.getOwnerID() == 1:
        soldiers = anArmy.getSoldiers()
        frst += soldiers[0]
        frst += soldiers[1]
        frst += soldiers[2]
      elif anArmy.getOwnerID() == 2:
        soldiers = anArmy.getSoldiers()
        scnd += soldiers[0]
        scnd += soldiers[1]
        scnd += soldiers[2]
    return (frst, scnd)


  def makeTurnMoves(self):
    for aCity in self.cities:
      aCity.turnSeed()
    self.cityDictionary[self.p1ChosenCity].turnSeed()
    self.cityDictionary[self.p2ChosenCity].turnSeed()
    finishedArmies = []
    toDelete = []
    for anArmy in self.armies:
      if anArmy.nextTurn() == "finished":
        finishedArmies.append(anArmy)
        toDelete.append(anArmy)
    for anElement in toDelete:
      self.armies.remove(anElement)
    toDelete = []
    for aFinishedArmy in finishedArmies:
      if self.cityDictionary[aFinishedArmy.getDestinationID()].getOwner() == aFinishedArmy.getOwnerID():
        self.cityDictionary[aFinishedArmy.getDestinationID()].increaseSoldiers(aFinishedArmy.getSoldiers())
        toDelete.append(aFinishedArmy)
    for anElement in toDelete:
        finishedArmies.remove(anElement)
    # dusmanlara ulasan ordular kaldi sadece
    attackerList = {}
    for anID in self.cityIDs:
      attackerList[anID] = []
    for aFinishedArmy in finishedArmies:
      attackerList[aFinishedArmy.getDestinationID()].append(aFinishedArmy)
    for anID in self.cityIDs:
      if attackerList[anID] == []:
        continue
      elif self.cityDictionary[anID].getOwner() == 0:
        combinedArmy1 = [0, 0, 0]
        combinedArmy2 = [0, 0, 0]
        for anArmy in attackerList[anID]:
          if anArmy.getOwnerID() == 1:
            combinedArmy1 = list(map(lambda tpl: tpl[0]+tpl[1], list(zip (combinedArmy1, anArmy.getSoldiers()))))
          else:
            combinedArmy2 = list(map(lambda tpl: tpl[0]+tpl[1], list(zip (combinedArmy2, anArmy.getSoldiers()))))
        attackerList[anID] = [combinedArmy1, combinedArmy2]
      else:
        combinedArmy = [0, 0, 0]
        for anArmy in attackerList[anID]:
          combinedArmy = list(map(lambda tpl: tpl[0]+tpl[1], list(zip (combinedArmy, anArmy.getSoldiers()))))
        attackerList[anID] = combinedArmy
    for anID in self.cityIDs:
      if attackerList[anID] == []:
        continue
      elif len(attackerList[anID]) == 3: # one army
        if self.cityDictionary[anID].getOwner() == 1:
          results = self.battleThem(self.cityDictionary[anID].getSoldiers(), attackerList[anID])
        else:
          results = self.battleThem(attackerList[anID], self.cityDictionary[anID].getSoldiers())
        if results[0] == 0:
          self.cityDictionary[anID].setSoldiers(results[1])
        else:
          self.cityDictionary[anID].setOwner(results[0])
          self.cityDictionary[anID].setSoldiers(results[1])
      elif len(attackerList[anID]) == 2: # two armies
        results = self.battleThem(attackerList[anID][0], attackerList[anID][1])
        if results[0] == 1:
          results = self.battleThem(results[1], self.cityDictionary[anID].getSoldiers())
          self.cityDictionary[anID].setSoldiers(results[1])
          if results[0] == 1:
            self.cityDictionary[anID].setOwner(1)
        elif results[0] == 2:
          results = self.battleThem(self.cityDictionary[anID].getSoldiers(), results[1])
          self.cityDictionary[anID].setSoldiers(results[1])
          if results[0] == 2:
            self.cityDictionary[anID].setOwner(2)

  def battleThem(self, armySize1, armySize2):
    clearFight = list(map(lambda tpl: tpl[0]-tpl[1] , list(zip(armySize1, armySize2))))
    if clearFight[0] <= 0 and clearFight[1] <= 0 and clearFight[2] <= 0 or clearFight[0] >= 0 and clearFight[1] >= 0 and clearFight[2] >= 0:
      if clearFight[0] <= 0 and clearFight[1] <= 0 and clearFight[2] <= 0:
        if clearFight == [0, 0, 0]:
          return (0, clearFight)
        clearFight = list(map(abs, clearFight))
        return (2, clearFight)
      return (1, clearFight)
    
    for inds in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
      if clearFight[inds[0]] == 0:
        if abs(clearFight[inds[1]])-2*abs(clearFight[inds[2]]) < 0:
          if clearFight[inds[2]] < 0:
            clearFight[inds[2]] += ceil(abs(clearFight[inds[1]]/2))
          else:
            clearFight[inds[2]] -= ceil(abs(clearFight[inds[1]]/2))
          clearFight[inds[1]] = 0
          if clearFight[inds[2]] == 0:
            return (0, clearFight)
          if clearFight[inds[2]] > 0:
            return (1, clearFight)
          else:
            clearFight = list(map(abs, clearFight))
            return (2, clearFight)
        else:
          clearFight[inds[1]] += 2*clearFight[inds[2]]
          clearFight[inds[2]] = 0
          if clearFight[inds[1]] == 0:
            return (0, clearFight)
          if clearFight[inds[1]] > 0:
            return (1, clearFight)
          else:
            clearFight = list(map(abs, clearFight))
            return (2, clearFight)

    if clearFight[0]*clearFight[1]*clearFight[2] > 0:
      numRounds = []
      for anInd in range(3):
        if clearFight[anInd] > 0:
          numRounds.append(ceil(abs(clearFight[anInd])/3)) # here 3
        else:
          numRounds.append(ceil(abs(clearFight[anInd])))
      leastRounds = min(numRounds)
      for anInd in range(3):
        if clearFight[anInd] > 0:
          clearFight[anInd] -= 3*leastRounds # here 3
          if clearFight[anInd] < 0:
            clearFight[anInd] = 0
        else:
          clearFight[anInd] += leastRounds
          if clearFight[anInd] > 0:
            clearFight[anInd] = 0
    else:
      numRounds = []
      for anInd in range(3):
        if clearFight[anInd] < 0:
          numRounds.append(ceil(abs(clearFight[anInd])/3)) # here 3
        else:
          numRounds.append(ceil(abs(clearFight[anInd])))
      leastRounds = min(numRounds)
      for anInd in range(3):
        if clearFight[anInd] < 0:
          clearFight[anInd] += 3*leastRounds # here 3
          if clearFight[anInd] > 0:
            clearFight[anInd] = 0
        else:
          clearFight[anInd] -= leastRounds
          if clearFight[anInd] < 0:
            clearFight[anInd] = 0
    if clearFight[0] <= 0 and clearFight[1] <= 0 and clearFight[2] <= 0 or clearFight[0] >= 0 and clearFight[1] >= 0 and clearFight[2] >= 0:
      if clearFight[0] <= 0 and clearFight[1] <= 0 and clearFight[2] <= 0:
        if clearFight == [0, 0, 0]:
          return (0, clearFight)
        clearFight = list(map(abs, clearFight))
        return (2, clearFight)
      return (1, clearFight)
    for inds in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
      if clearFight[inds[0]] == 0:
        if abs(clearFight[inds[1]])-2*abs(clearFight[inds[2]]) < 0:
          if clearFight[inds[2]] < 0:
            clearFight[inds[2]] += ceil(abs(clearFight[inds[1]]/2))
          else:
            clearFight[inds[2]] -= ceil(abs(clearFight[inds[1]]/2))
          clearFight[inds[1]] = 0
          if clearFight[inds[2]] == 0:
            return (0, clearFight)
          if clearFight[inds[2]] > 0:
            return (1, clearFight)
          else:
            clearFight = list(map(abs, clearFight))
            return (2, clearFight)
        else:
          clearFight[inds[1]] += 2*clearFight[inds[2]]
          clearFight[inds[2]] = 0
          if clearFight[inds[1]] == 0:
            return (0, clearFight)
          if clearFight[inds[1]] > 0:
            return (1, clearFight)
          else:
            clearFight = list(map(abs, clearFight))
            return (2, clearFight)

  def executeOrders(self, playerNo, Commands):
    try:
      if playerNo == 1:
        p1Cities = []
        for aCity in self.cities:
          if aCity.getOwner() == 1:
            p1Cities.append(aCity)
        for aCommand in Commands:
          if aCommand.startswith("cclub power:"):
            self.p1ChosenCity = int(aCommand[len("cclub power:"):])
          else:
            [fCity, tCity, rock, paper, scissors] = aCommand.split()
            [fCity, tCity, rock, paper, scissors] = list(map(int, [fCity, tCity, rock, paper, scissors]))
            if rock < 0 or paper < 0 or scissors < 0:
              raise CommandError()
            worked = False
            for aCity in p1Cities:
              if aCity.getCityID() == fCity:
                worked = True
                break
            if not worked:
              raise CommandError()
            if not tCity in self.cityIDs:
              raise CommandError()
            for aCity in p1Cities:
              if aCity.getCityID() == fCity:
                theCity = aCity
                break
            theCity.decreaseSoldiers([rock, paper, scissors])
            self.armies.append(army.Army(self.lastArmyID+1, fCity, tCity, 1, self.distanceBetweenCitiesID(fCity, tCity) , [rock, paper, scissors], self.cityDictionary[fCity].getCoordinates(), self.cityDictionary[tCity].getCoordinates()))
            self.lastArmyID += 1
            
      elif playerNo == 2:
        p2Cities = []
        for aCity in self.cities:
          if aCity.getOwner() == 2:
            p2Cities.append(aCity)
        for aCommand in Commands:
          if aCommand.startswith("cclub power:"):
            self.p2ChosenCity = int(aCommand[len("cclub power:"):])
          else:
            [fCity, tCity, rock, paper, scissors] = aCommand.split()
            [fCity, tCity, rock, paper, scissors] = list(map(int, [fCity, tCity, rock, paper, scissors]))
            if rock < 0 or paper < 0 or scissors < 0:
              raise CommandError()
            worked = False
            for aCity in p2Cities:
              if aCity.getCityID() == fCity:
                worked = True
                break
            if not worked:
              raise CommandError()
            if not tCity in self.cityIDs:
              raise CommandError()
            for aCity in p2Cities:
              if aCity.getCityID() == fCity:
                theCity = aCity
                break
            theCity.decreaseSoldiers([rock, paper, scissors])
            self.armies.append(army.Army(self.lastArmyID+1, fCity, tCity, 2, self.distanceBetweenCitiesID(fCity, tCity) , [rock, paper, scissors], self.cityDictionary[fCity].getCoordinates(), self.cityDictionary[tCity].getCoordinates()))
            self.lastArmyID += 1
    except:
      return "error"

  def distanceBetweenCitiesID(self, cityId1, cityId2):
    firstCity = False
    secondCity = False
    for aCity in self.cities:
      if aCity.getCityID() == cityId1:
        firstCity = aCity
      elif aCity.getCityID() == cityId2:
        secondCity = aCity
      if firstCity != False and secondCity != False:
        break
    (x1, y1) = firstCity.getCoordinates()
    (x2, y2) = secondCity.getCoordinates()
    return ceil((((x1-x2)**2 + (y1-y2)**2)**0.5)/20)

  def timeoutHandler(self, signum, frame):
    raise IOError("timeout")

  def sendMapInformation(self):
    try:
      os.write(self.player1WriteOut, (str(self.numCities) + "\n").encode())
      for aLine in self.cityLines:
        os.write(self.player1WriteOut, aLine.encode())
    except:
      return "error on 1"
    try:
      os.write(self.player2WriteOut, (str(self.numCities) + "\n").encode())
      for aLine in self.cityLines:
        aLine = aLine.split()
        aLine[3] = str((3 - int(aLine[3]))%3)
        aLine = functools.reduce(lambda x,y: x + " " + y, aLine, "")[1:] + "\n"
        os.write(self.player2WriteOut, aLine.encode())
    except:
      return "error on 2"

  def requestTurnMove(self, playerNo):
    if playerNo == 1:
      commands = []
      readStr = self.readALine(self.player1ReadIn)
      numberOfCommands = (int(readStr))
      i = 0
      while i < numberOfCommands:
        commands.append(self.readALine(self.player1ReadIn))
        i += 1
      return commands
    elif playerNo == 2:
      commands = []
      readStr = self.readALine(self.player2ReadIn)
      numberOfCommands = (int(readStr))
      i = 0
      while i < numberOfCommands:
        commands.append(self.readALine(self.player2ReadIn))
        i += 1
      return commands

  def readALine(self, fD):
    line = ""
    while not (len(line) > 0 and line[-1] == "\n"):
      line += os.read(fD, 1).decode()
    return line

  def currentGameInfo(self, playerNo):
    retString = ''
    retString += str(self.numCities) + "\n"
    for aCity in self.cities:
      retString += aCity.toStr(playerNo) + "\n"
    retString += str(len(self.armies)) + "\n"
    for anArmy in self.armies:
      retString += anArmy.toStr(playerNo) + "\n"
    retString += "metu cclub\n"
    return retString
