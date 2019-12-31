
from sys import stdout
import random

turn = 0

def readAndWrite():
  aL = input()
  return aL

numberOfCities = int(readAndWrite())
i = 0
while i < numberOfCities:
  i += 1
  readAndWrite()

while True:
  myCities = []
  otherCities = []
  allCities = []
  numCities = readAndWrite()
  i = 0
  while i < int(numCities):
    aLine = readAndWrite().split()
    if aLine[1] == "1":
      myCities.append(aLine)
    else:
      otherCities.append(aLine)
    allCities.append(aLine)
    i+=1
  numArmies = readAndWrite()
  i = 0
  while i < int(numArmies):
    readAndWrite()
    i+=1
  if readAndWrite() == "metu cclub":
    if len(otherCities) == 0:
      stdout.write("0\n")
      stdout.flush()
      continue
    stdout.write(str(len(myCities)) + "\n")
    stdout.flush()
    for aCity in myCities:
      selectedCity = random.randint(0, numberOfCities-1)
      while selectedCity == aCity[0]:
        selectedCity = random.randint(0, numberOfCities-1)
      stdout.write("%s %s %d %d %d\n" % (aCity[0], allCities[selectedCity][0], int(aCity[2])/2, int(aCity[3])/2, int(aCity[4])/2))
      stdout.flush()

    