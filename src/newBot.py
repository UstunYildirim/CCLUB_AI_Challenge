
from sys import stdout

f = open("sampleIO.txt", "w")

def readAndWrite():
  aL = input()
  f.write(aL + "\n")
  return aL

numCities = int(readAndWrite())
i = 0
while i < numCities:
  readAndWrite()
  i+=1

while True:
  numCities = int(readAndWrite())
  i = 0
  while i < numCities:
    readAndWrite()
    i+=1
  numArmies = int(readAndWrite())
  i = 0
  while i < numArmies:
    readAndWrite()
    i+=1
  if readAndWrite() == "metu cclub":
    stdout.write("0\n")
    stdout.flush()

