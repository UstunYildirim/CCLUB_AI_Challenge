import os
import sys
import time

if os.fork() == 0:
	while True:
		try:
			if len(os.listdir("/var/www/pyStuff/pending/")) == 0:
				time.sleep(1)
			elif "hebele" in os.listdir("/var/www/pyStuff/pending/"):
				time.sleep(1)
			else:
				fName = os.listdir("/var/www/pyStuff/pending/")[0]
				os.system("python3.1 /var/www/pyStuff/ozChallenger.py " + fName)
				os.system("rm -f '/var/www/pyStuff/pending/" + fName +"'")
		except:
			pass
		finally:
			time.sleep(1)
else:
	exit()
