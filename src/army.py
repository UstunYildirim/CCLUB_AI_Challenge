"""
three types of soldier: rock, paper, scissors
1 rock beats 2 scissors
1 paper beats 2 rocks
1 scissors beats 2 papers
"""


class Army():
  def __init__(self, armyID, startCityID, endCityID, ownerID, numberOfTurns, currentSoldiers, startCityCoordinates, endCityCoordinates):
    self.armyID = armyID
    self.startCityID = startCityID
    self.endCityID = endCityID
    self.ownerID = ownerID
    self.numberOfTurns = numberOfTurns
    self.currentSoldiers = currentSoldiers
    self.remainingTurns = numberOfTurns + 1
    self.startCityCoordinates = startCityCoordinates
    self.currentCoordinates = startCityCoordinates
    self.endCityCoordinates = endCityCoordinates

  def getOwnerID(self):
    return self.ownerID

  def getSourceID(self):
    return self.startCityID

  def getDestinationID(self):
    return self.endCityID

  def getSoldiers(self):
    return self.currentSoldiers

  def nextTurn(self):
    self.currentCoordinates = list(map(lambda x: x[0]+(x[1]-x[0])*(1-(self.remainingTurns-1)/self.numberOfTurns), list(zip(self.startCityCoordinates, self.endCityCoordinates))))
    self.currentCoordinates = list(map(int, self.currentCoordinates))
    self.remainingTurns -= 1
    if self.remainingTurns == 0:
      return "finished"


  def toStr(self, playerNo):
    if playerNo == 1:
      return "%d %d %d %d %d %d %d %d %d" \
        % (self.armyID, self.startCityID, self.endCityID, self.ownerID, self.numberOfTurns, self.remainingTurns, \
        self.currentSoldiers[0], self.currentSoldiers[1], self.currentSoldiers[2])
    else:
      return "%d %d %d %d %d %d %d %d %d" \
        % (self.armyID, self.startCityID, self.endCityID, (3-self.ownerID)%3, self.numberOfTurns, self.remainingTurns, \
        self.currentSoldiers[0], self.currentSoldiers[1], self.currentSoldiers[2])