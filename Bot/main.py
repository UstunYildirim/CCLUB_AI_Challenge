"""
METU CCLUB Sample AI
"""

from sys import stdout
from random import randint
from math import ceil

"""
You will mainly be changing myAI function below.
It is executed once every turn.
"""
def myAI(game):
  """
  Every time this function is called, it finds your the most productive city for 
  that turn and finds your city with the greatest number of total soldiers.
  Then, it will send two commands:
  First one selects your the most productive city to be your city with
  the CCLUB POWER which doubles the production.
  Second command sends all the soldiers in your strongest city to a randomly
  chosen city which is not yours.
  """
  cityList = game.getCityList()
  listOfMyCities = []
  otherCities = []
  for aCity in cityList:
    if aCity.getOwnerID() == 1:
      listOfMyCities.append(aCity)
    else:
      otherCities.append(aCity)
      
  if len(listOfMyCities) == 0 or len(otherCities) == 0:
    return
  maxIncome = 0
  maxIncomeCity = 0
  biggestArmy = 0
  biggestCity = 0

  for aCity in listOfMyCities:
    if aCity.getProductionAmount() > maxIncome:
      maxIncome = aCity.getProductionAmount()
      maxIncomeCity = aCity.getCityID()
    armySize = aCity.getSoldiers()
    armySize = armySize[0] + armySize[1] + armySize[2]
    if armySize > biggestArmy:
      biggestArmy = armySize
      biggestCity = aCity.getCityID()
  
  game.CCLUB_POWER(maxIncomeCity)
  selectedCity = randint(0, len(otherCities)-1)
  game.giveOrder(biggestCity, otherCities[selectedCity].getCityID(), game.getCityDictionary()[biggestCity].getSoldiers())

class mayIchallenge():
  def __init__(self):
    self.commands = []
    self.cities = {}
    self.armies = {}
    self.turn = 0
    self.numCities = int(self.readAline())
    self.numArmies = 0
    i = 0
    while i < self.numCities:
      newCity = city(self.readAline())
      self.cities[newCity.getCityID()] = newCity
      i+=1

  def startGame(self):
    while self.turn < 250:
      self.numCities = int(self.readAline())
      i = 0
      while i < self.numCities:
        newLine = self.readAline()
        self.cities[int(newLine.split()[0])].updateInfo(newLine)
        i+=1
      self.numArmies = int(self.readAline())
      i = 0
      while i < self.numArmies:
        newLine = self.readAline()
        self.armies[int(newLine.split()[0])] = army(newLine)
        i+=1
      if self.readAline() == "metu cclub":
        myAI(self)
      stdout.write(str(len(self.commands)) + "\n")
      stdout.flush()
      for aCommand in self.commands:
        stdout.write(aCommand)
        stdout.flush()
      self.commands = []
      self.armies = {}
      self.turn += 1

  def CCLUB_POWER(self, cityID):
    self.commands.append("cclub power:" + str(cityID) + "\n")

  def giveOrder(self,fromCity, toCity, soldiersList):
    fromCity = str(fromCity)
    toCity = str(toCity)
    (noRocks, noPapers, noScissors) = soldiersList
    self.commands.append(fromCity + " " + toCity + " " + str(noRocks) + " " + str(noPapers) + " " + str(noScissors) + "\n")

  def numberOfTurnsBetweenCities(self, cityID1, cityID2):
    (x1, y1) = self.cities[cityID1].getCoordinates()
    (x2, y2) = self.cities[cityID2].getCoordinates()
    return ceil((((x1-x2)**2 + (y1-y2)**2)**0.5)/20)
    

  def readAline(self):
    aL = input()
    return aL

  def getCityList(self):
    retList = []
    for aCityID in self.cities:
      retList.append(self.cities[aCityID])
    return retList

  def getCityDictionary(self):
    return self.cities

  def getArmyList(self):
    retList = []
    for anArmyID in self.armies:
      retList.append(self.armies[anArmyID])
    return retList

  def getArmyDictionary(self):
    return self.armies


class city():
  def __init__(self, cityInfoString):
    infoArray = cityInfoString.split()
    self.id = int(infoArray[0])
    self.x = int(infoArray[1])
    self.y = int(infoArray[2])
    self.ownerID = int(infoArray[3])
    self.productionType = infoArray[4]
    self.productionAmount = int(infoArray[5])
    self.soldiers = list(map(int, infoArray[6:9]))
  def updateInfo(self, newInfoString):
    infoArray = newInfoString.split()
    if int(infoArray[0]) == self.id:
      self.ownerID = int(infoArray[1])
      self.soldiers = list(map(int, infoArray[2:5]))
  def getCityID(self):
    return self.id
  def getOwnerID(self):
    return self.ownerID
  def getCoordinates(self):
    return (self.x, self.y)
  def getProductionAmount(self):
    return self.productionAmount
  def getProductionType(self):
    return self.productionType
  def getSoldiers(self):
    return self.soldiers

class army():
  def __init__(self, armyInfoString):
    infoArray = armyInfoString.split()
    self.id = int(infoArray[0])
    self.initialCityID = int(infoArray[1])
    self.destinationCityID = int(infoArray[2])
    self.ownerID = int(infoArray[3])
    self.totalNumberOfTurns = int(infoArray[4])
    self.remainingNumberOfTurns = int(infoArray[5])
    self.soldiers = list(map(int, infoArray[6:9]))
  def getOwnerID(self):
    return self.ownerID
  def getArmyID(self):
    return self.id
  def getInitialCityID(self):
    return self.initialCityID
  def getTargetCityID(self):
    return self.destinationCityID
  def getRemainingNumberOfTurns(self):
    return self.remainingNumberOfTurns
  def getTotalNumberOfTurns(self):
    return self.totalNumberOfTurns
  def getSoldiers(self):
    return self.soldiers


newGame = mayIchallenge()
newGame.startGame()
