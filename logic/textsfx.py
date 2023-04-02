from sys import stdout
from time import sleep

def slowprint(msg, end="\n"):
	for c in msg:
		stdout.write(c)
		stdout.flush()
		sleep(0.05)
	print(end)