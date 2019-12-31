"""
MapGenerator class
"""

import random

class MapGenerator():
  """
  instantiate the map with dimensions
  """
  def __init__(self, numberOfMaps = 100, dimensions = (800, 600), halfNumberOfCities = 6, symmetry = True):
    fileNames = ["./maps/%d.map" %x for x in range(numberOfMaps)]
    for aFileName in fileNames:
      self.generateMap(aFileName, dimensions, halfNumberOfCities, symmetry)

  def generateMap(self, fileName, dimensions, halfNumberOfCities, symmetry):
    aFile = open(fileName, 'w')
    aFile.write("# Width Height\n" + str(dimensions[0]) + " " + str(dimensions[1]) + "\n")
    aFile.write("# Number Of Cities\n" + str(halfNumberOfCities*2) + "\n")
    aFile.write("# City ID, X Coordinate, Y Coordinate, Owner ID, Production Type, Production Speed, Current Soldier Amounts of Rock, Paper, Scissors\n")
    cities = self.distributeCities(dimensions, halfNumberOfCities, symmetry)
    citiesWithAttributes = self.assignAttributes(cities)
    for aCity in citiesWithAttributes:
      aFile.write(str(aCity[0]) + ' ')
      aFile.write(str(aCity[1][0]) + ' ')
      aFile.write(str(aCity[1][1]) + ' ')
      aFile.write(str(aCity[2]) + ' ')
      aFile.write(str(aCity[3]) + ' ')
      aFile.write(str(aCity[4]) + ' ')
      aFile.write(str(aCity[5][0]) + ' ')
      aFile.write(str(aCity[5][1]) + ' ')
      aFile.write(str(aCity[5][2]) + '\n')
    

  def assignAttributes(self, cities):
    """
    attributes are Owner ID, City ID, Production Type, Production Speed, Current Number of Soldiers
    Current Soldier type is production type
    """
    zippedList = zip(cities[::2], cities[1::2])
    types = list(range(int(len(cities)/2)))
    random.shuffle(types)
    retList = []
    cityNo = 1
    for (aCity, bCity) in zippedList:
      prodType = types.pop()%3
      prodSpeed = random.randint(2,7)
      currentNumberOfSoldiers = [0,0,0]
      currentNumberOfSoldiers[prodType] = 10*(prodSpeed-1)
      if prodType == 0: prodType = "R"
      elif prodType == 1: prodType = "P"
      else: prodType = "S"
      if cityNo < 2:
        retList.append((1, aCity, 1, prodType, prodSpeed, currentNumberOfSoldiers))
        retList.append((2, bCity, 2, prodType, prodSpeed, currentNumberOfSoldiers))
        cityNo = 3
      else:
        retList.append((cityNo, aCity, 0, prodType, prodSpeed, currentNumberOfSoldiers))
        cityNo += 1
        retList.append((cityNo, bCity, 0, prodType, prodSpeed, currentNumberOfSoldiers))
        cityNo += 1
    return retList

  def distributeCities(self, dimensions, halfNumberOfCities, symmetry):
    def myDist(X1, X2):
      (x1,y1) = X1
      (x2,y2) = X2
      return (abs(x1-x2)**2 + abs(y1-y2)**2)**0.5
    lowerRadius = dimensions[0]/(2*halfNumberOfCities)
    if symmetry:
      cities = []
      for i in range(halfNumberOfCities):
        citiesIntersect = True
        while citiesIntersect:
          (x,y) = (random.randint(int(lowerRadius), int(dimensions[0]/2-lowerRadius)), random.randint(int(lowerRadius),int(dimensions[1]- lowerRadius)))
          citiesIntersect = False
          for aCity in cities:
            if myDist(aCity,(x,y)) < lowerRadius:
              citiesIntersect = True
              break
        cities.append((x,y))
      doubleCities = []
      for aCity in cities:
        doubleCities.append(aCity)
        doubleCities.append((dimensions[0] - aCity[0], dimensions[1] - aCity[1]))        
      return doubleCities
    else:
      pass