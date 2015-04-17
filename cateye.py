#!/usr/bin/python

import os
import sys
import getopt
import time
import string


cateye_ctl={"q":0, "r":0, "l":0, "c":0, "rec_cnt":0, "f_type":'f', "l_path":""}

def cateye_usage():
	"""Usage of cateye.py."""
	print ""
	print "usage: cateye.py [path] [OPTION]"
	print ""
	print "[OPTION]:"
	print "-c            : Turn colorization off. for dumping output information to file."
	print "-d seconds    : Update regularly at interval of seconds, where the \"seconds\" can be float point number. "
	print "-h,--help     : It shows this usage."
	print "-l            : To show symbolic link's real path, and to prevent infinite loop.(available when -q option is enabled.)"
	print "-r            : It recursively works in folder for list function. (likes tree)"
	print "-s parameters : To write parameters to file. use \"\" when parameters more than one."
	print "-q            : Quiet, It shows filename only, no content of file."
	print ""


def cateye_docat(path, isfile):
	"""To dump content of path"""
	
	if isfile:
		try:
			f = open(path, "r")
		except IOError as err:
			ret = str(err)
			return ret
		try:
			ret = f.read()
		except IOError as err:
			ret = str(err)
		f.close()
	else:
		ret=""
	return ret


def cateye_dowrite(path, sval):
	"""To write data to specified file"""
	if os.path.isfile(path):
		try:
			fd=os.open(path, os.O_RDWR)
		except OSError as err:
			print str(err)
			return 
		try:
			os.write(fd, sval)
		except OSError as err:
			print str(err)
		os.close(fd)


def cateye(ctl, basefolder="/sys"):
	"""
	To dump content of entries, it's useful to show information at /proc or /sys folder.
	use cateye.ctl for first argument.
	"""

	indent=[]
	for level in range(ctl["rec_cnt"]):
		indent.append("    ")

	dirs=[]
	try:
		dirs = os.listdir(basefolder)
	except OSError:
		dirs.append(basefolder)

	for leaf in dirs:
		info=[]
		isfile=False
		isDir=False
		isLink=False
		fullleaf = os.path.join(basefolder,leaf)
		isfile = os.path.isfile(fullleaf)
		if(isfile == False):
			isDir = os.path.isdir(fullleaf)
		isLink = os.path.islink(fullleaf)

		if isfile:
			ctl["f_type"]='f'
		elif isDir:
			ctl["f_type"]='d'
		else:
			ctl["f_type"]='s'

		ctl["l_path"]=""
		if isLink:
			ctl["f_type"] = ctl["f_type"].upper()
			try:
				ctl["l_path"] = os.path.realpath(fullleaf)
			except OSError as err:
				ctl["l_path"] = str(err)

		info.extend(indent)
		info.append((ctl['c']==0 and "\033[1m" or "")) 
		info.append(" [")

		if isLink:
			info.append((ctl['c']==0 and "\033[36m" or ""))

		info.append(ctl["f_type"])
		info.append((ctl['c']==0 and "\033[0m\033[1m" or ""))
		info.append("] ")
		info.append(leaf) 


		if ctl['q']:
			if ctl['l'] and isLink:
				info.append(": ")
				info.append((ctl['c']==0 and "\033[0m" or ""))
				info.append(ctl["l_path"])
			else:
				info.append((ctl['c']==0 and "\033[0m" or ""))
		
		else:
			if isDir:
				info.append((ctl['c']==0 and "\033[0m" or ""))
			else:
				info.append(": ")
				info.append((ctl['c']==0 and "\033[0m" or ""))
				info.append(cateye_docat(fullleaf, isfile))
		
		
		print(string.join(info,""))

		
		if ctl['r']:
			if ctl['l'] and isLink:
				pass

			elif isDir:
				ctl["rec_cnt"]+=1;
				cateye(ctl, fullleaf)
				ctl["rec_cnt"]-=1;


def cateye_errexit(err, ret_code, show_usage=False):
	""" error processing function """
	print "!!! Terminated by " + str(err)
	if show_usage is True:
		cateye_usage()
	sys.exit(ret_code)
	

if __name__ == "__main__":
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], "cd:hls:qr", ["help",])
	except getopt.GetoptError as err:
		cateye_errexit(err, 2, True)
	
	regular_time=0
	sval=""
	for op, ar in opts:
		if op == "-d":
			try:
				regular_time = float(ar)
			except ValueError as err:
				cateye_errexit(err, 3, True)	
		elif op in ("-h","--help"):
			cateye_usage()
			sys.exit(0)
		elif op == "-s":
			sval = ar
		elif op == "-q":
			cateye_ctl['q']=1
		elif op == "-r":
			cateye_ctl['r']=1
		elif op == "-l":
			cateye_ctl['l']=1
		elif op == "-c":
			cateye_ctl['c']=1
			

	while True:
		if len(args) is not 1:
			cateye_errexit("wrong path specified", 5, True)
			
		if sval is not "":
			cateye_dowrite(str(args[0]), sval)
			sys.exit(0)

		try:
			cateye(cateye_ctl, str(args[0]))
		except IndexError as err:
			cateye_errexit(err, 4)

		if not regular_time:
			sys.exit(0)

		time.sleep(regular_time)


