import Grammar
import Files

import random

for _ in range(12000):
	try:
		Grammar.main()
	except:
		print "Exception, but that's OK"
