#!/usr/bin/python

import os
import sys
import getopt
import time

def cateye_usage():
	"""Usage of cateye.py."""
	print ""
	print "usage: cateye.py [path] [OPTION]"
	print ""
	print "[OPTION]:"
	print "-d seconds\t\t: update regularly at interval of seconds, where the \"seconds\" can be float point number. "
	print "-s parameters\t\t: write parameters to file. use \"\" when parameters more than one."
	print "-h,--help\t\t: shows this usage."
	print ""

def dols(path="."):
	"""To list entries of path."""
	fd = os.popen("ls "+path)
	dirlist = fd.read().split()
	fd.close()
	return dirlist

def docat(path):
	"""To dump content of path"""
	fd = os.popen("cat "+path)
	ret = fd.read()
	fd.close()
	return ret

def dowrite(path, sval):
	if os.path.isfile(path):
		fd=os.open(path, os.O_RDWR)
		os.write(fd, sval)
		os.close(fd)

def cateye(basefolder="/sys"):
	"""To dump content of entries, it's useful to show information at /proc or /sys folder."""
	for leaf in dols(basefolder):
		if os.path.isfile(basefolder):
			fullleaf = basefolder
		else:
			fullleaf = os.path.join(basefolder,leaf)
		print (os.path.isdir(fullleaf) and "\033[1m" + " [d] " + leaf + "\033[0m" or "\033[1m" + " [f] " + leaf + ": " + "\033[0m"+docat(fullleaf))

def err_exit(err, ret_code, show_usage=False):
	print "!!! Terminated by " + str(err)
	if show_usage is True:
		cateye_usage()
	sys.exit(ret_code)
	

if __name__ == "__main__":
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], "d:hs:", ["help",])
	except getopt.GetoptError as err:
		err_exit(err, 2, True)
	
	regular_time=0
	sval=""
	for op, ar in opts:
		if op == "-d":
			try:
				regular_time = float(ar)
			except ValueError as err:
				err_exit(err, 3, True)	
		elif op in ("-h","--help"):
			cateye_usage()
			sys.exit(0)
		elif op == "-s":
			sval = ar

	while True:
		if len(args) is not 1:
			err_exit("wrong path specified", 5)
			
		if sval is not "":
			dowrite(str(args[0]), sval)
			sys.exit(0)

		try:
			cateye(str(args[0]))
		except IndexError as err:
			err_exit(err, 4)

		if not regular_time:
			sys.exit(0)

		time.sleep(regular_time)


