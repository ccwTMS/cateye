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
	print "-q\t\t\t: quiet, show filename only, no content of file."
	print "-r\t\t\t: recursively works in folder for list function. (likes tree)"
	print "-h,--help\t\t: shows this usage."
	print ""

def dols(path="."):
	"""To list entries of path."""
	fd = os.popen("ls -A "+path)
	dirlist = fd.read().split()
	fd.close()
	return dirlist

def docat(path):
	"""To dump content of path"""
	if os.path.isfile(path):
		fd = os.popen("cat "+path)
		ret = fd.read()
		fd.close()
	else:
		ret = ""
	return ret


def dowrite(path, sval):
	if os.path.isfile(path):
		fd=os.open(path, os.O_RDWR)
		os.write(fd, sval)
		os.close(fd)

def cateye(ctl, basefolder="/sys"):
	"""To dump content of entries, it's useful to show information at /proc or /sys folder."""

	indent=""
	for level in range(ctl["rec_cnt"]):
		indent+="    "

	for leaf in dols(basefolder):
		if os.path.isdir(basefolder):
			fullleaf = os.path.join(basefolder,leaf)
			ctl["f_type"]='d'
		elif os.path.isfile(basefolder):
			fullleaf = basefolder
			ctl["f_type"]='f'
		else:
			fullleaf = basefolder
			ctl["f_type"]='s'

		if os.path.islink(fullleaf):
			ctl["f_type"] = ctl["f_type"].upper()


		print(indent + (os.path.isdir(fullleaf) and "\033[1m" + " [" + ctl["f_type"] +"] " + leaf + "\033[0m" or "\033[1m" + " [" + ctl["f_type"] + "] " + leaf +(ctl['q'] and "\033[0m" or ": "+"\033[0m"+docat(fullleaf))))

		if ctl['r'] == 1:
			if os.path.isdir(fullleaf):
				ctl["rec_cnt"]+=1;
				cateye(ctl, fullleaf)
				ctl["rec_cnt"]-=1;


def err_exit(err, ret_code, show_usage=False):
	print "!!! Terminated by " + str(err)
	if show_usage is True:
		cateye_usage()
	sys.exit(ret_code)
	

if __name__ == "__main__":
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], "d:hs:qr", ["help",])
	except getopt.GetoptError as err:
		err_exit(err, 2, True)
	
	regular_time=0
	sval=""
	ctl={"q":0, "r":0, "rec_cnt":0, 'f_type':'f'}
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
		elif op == "-q":
			ctl['q']=1
		elif op == "-r":
			ctl['r']=1
			

	while True:
		if len(args) is not 1:
			err_exit("wrong path specified", 5)
			
		if sval is not "":
			dowrite(str(args[0]), sval)
			sys.exit(0)

		try:
			cateye(ctl, str(args[0]))
		except IndexError as err:
			err_exit(err, 4)

		if not regular_time:
			sys.exit(0)

		time.sleep(regular_time)


