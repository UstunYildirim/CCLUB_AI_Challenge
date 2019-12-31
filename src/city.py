"""
City class
"""
import game

class City():
  """
  Class instance created with given coordinates as a tuple, production type,
  production amount and a vector of current soldier numbers.
  """
  def __init__(self, cityID, coordinates, ownerID, productionType, productionAmount, currentSoldiers):
    self.cityID = cityID
    self.coordinates = coordinates # (x,y)
    self.ownerID = ownerID
    self.productionType = productionType
    self.productionAmount = productionAmount
    self.currentSoldiers = currentSoldiers # amounts of (r,p,s)

  def getCityID(self):
    return self.cityID

  def getCoordinates(self):
    return self.coordinates

  def setSoldiers(self, currentSoldiers):
    self.currentSoldiers = currentSoldiers
    for aCnt in self.currentSoldiers:
      if aCnt < 0:
        raise game.CommandError()

  def getSoldiers(self):
    return self.currentSoldiers

  def increaseSoldiers(self, increaseSoldiers):
    self.currentSoldiers = list(map(lambda tpl: tpl[0]+tpl[1], list(zip (self.currentSoldiers, increaseSoldiers))))
    for aCnt in self.currentSoldiers:
      if aCnt < 0:
        raise game.CommandError()

  def decreaseSoldiers(self, decreaseSoldiers):
    self.currentSoldiers = list(map(lambda tpl: tpl[0]-tpl[1], list(zip (self.currentSoldiers, decreaseSoldiers))))
    for aCnt in self.currentSoldiers:
      if aCnt < 0:
        raise game.CommandError()

  def turnSeed(self):
    if self.ownerID == 0:
      return
    else:
      if self.productionType == "R":
        self.increaseSoldiers([self.productionAmount, 0, 0])
      elif self.productionType == "P":
        self.increaseSoldiers([0, self.productionAmount, 0])
      else:
        self.increaseSoldiers([0, 0, self.productionAmount])

  def setOwner(self, ownerID):
    self.ownerID = ownerID

  def getOwner(self):
    return self.ownerID

  def toStr(self, playerNo):
    if playerNo == 1:
      return "%d %d %d %d %d" %(self.cityID, self.ownerID, self.currentSoldiers[0], self.currentSoldiers[1], self.currentSoldiers[2])
    else:
      return "%d %d %d %d %d" %(self.cityID, (3-self.ownerID)%3, self.currentSoldiers[0], self.currentSoldiers[1], self.currentSoldiers[2])