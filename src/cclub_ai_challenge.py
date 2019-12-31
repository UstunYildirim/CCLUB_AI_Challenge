"""
main executable
start with something like:
python cclub_ai_challenge.py --map ./maps/0.map --player1 "python ./sourcecode.py" --player2 "./executable" --maxturn 500 --json ornekjson.txt
"""

__author__="freemind"
__date__ ="$Dec 9, 2010 1:03:15 AM$"

import sys
import game

if __name__ == "__main__":
    # a = MapGenerator(100)
    debugger = False
    map = None
    p1 = None
    p2 = None
    maxturn = 100
    json = "ornekjson.txt"
    found = False
    for anArgument in sys.argv:
      if found == False:
        if anArgument == "--map":
          found = "map"
        elif anArgument == "--player1":
          found = "p1"
        elif anArgument == "--player2":
          found = "p2"
        elif anArgument == "--maxturn":
          found = "maxturn"
        elif anArgument == "--json":
          found = "json"
        elif anArgument == "--debug":
          debugger = True
        else:
          found = False
      else:
        if found == "map":
          map = anArgument
        elif found == "p1":
          p1 = anArgument
        elif found == "p2":
          p2 = anArgument
        elif found == "maxturn":
          maxturn = anArgument
        elif found == "json":
          json = anArgument
        found = False
    theGame = game.Game(map, p1, p2, maxturn, json, debugger)
    theGame.startGame()

