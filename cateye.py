#!/usr/bin/python

import os
import sys
import getopt
import time
import string

__all__ = ('cateye', 'cateye_ctl',)

cateye_ctl={"q":0, "r":0, "l":0, "c":0, "rec_cnt":0, "f_type":'f', "l_path":"", "d_except":"", "regular_time":0.0, "sval":""}

def _cateye_usage():
	"""Usage of cateye.py."""
	print ""
	print "usage: cateye.py [path] [OPTION]"
	print ""
	print "[OPTION]:"
	print "-c             : Turn colorization off. for dumping output information to file."
	print "-d seconds     : Update regularly at interval of seconds, where the \"seconds\" can be float point number. "
	print "-h,--help      : It shows this usage."
	print "-l             : To show symbolic link's real path, and to prevent infinite loop.(available when -q option is enabled.)"
	print "-r             : It recursively works in folder for list function. (likes tree)"
	print "-s parameters  : To write parameters to file. use \"\" when parameters more than one."
	print "-q             : Quiet, It shows filename only, no content of file."
	print "-x foldernames : ignores specified folders. (foldernames: \"folder1 folder2 ...\")" 
	print ""


def _cateye_docat(path, isFile):
	"""To dump content of path"""
	
	if isFile:
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


def _cateye_dowrite(path, sval):
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


def _info_highlight(info, ctl, leaf, isLink):	
	startHighlight = (ctl['c']==0 and "\033[1m" or "")
	restartHighlight = (ctl['c']==0 and "\033[0m\033[1m" or "")
	linkHighlight = (ctl['c']==0 and "\033[36m" or "")
	stopHighlight = (ctl['c']==0 and "\033[0m" or "")

	info.append(startHighlight) 
	info.append(" [")

	if isLink:
		info.append(linkHighlight)

	info.append(ctl["f_type"])
	info.append(restartHighlight)
	info.append("] ")
	info.append(leaf) 


	if ctl['q']:
		if ctl['l'] and isLink:
			info.append(": ")
			info.append(stopHighlight)
			info.append(ctl["l_path"])
		else:
			info.append(stopHighlight)
	else:
		if ctl["f_type"] == 'd':
			info.append(stopHighlight)
		else:
			info.append(": ")
			info.append(stopHighlight)

def _info_formating(info, ctl, leaf, isLink):	
	info.append("["+ctl["f_type"]+"]")
	info.append(leaf) 


	if ctl['q']:
		if ctl['l'] and isLink:
			info.append(": ")
			info.append(ctl["l_path"])
	else:
		if ctl["f_type"] == 'd':
                    pass
		else:
			info.append(": ")




def _leaf_type(ctl, fullleaf):
	isFile=False
	isDir=False
	isLink=False
	isFile = os.path.isfile(fullleaf)
	if(isFile == False):
		isDir = os.path.isdir(fullleaf)
	isLink = os.path.islink(fullleaf)

	if isFile:
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

	return (isFile,isDir,isLink)


ret_data = []

def cateye(ctl, basefolder="/sys"):
	"""
	To dump content of entries, it's useful to show information at /proc or /sys folder.
	use cateye.ctl for first argument.
	"""
        global ret_data

        if __name__ == "__main__":
	    indent=[]
	    for level in range(ctl["rec_cnt"]):
		    indent.append("    ")

	dirs=[]
	try:
		dirs = os.listdir(basefolder)
	except OSError:
		dirs.append(basefolder)
	
	if ctl["d_except"] != "":
            for folder in ctl["d_except"].split(" "): #ar.split(" "):
			try:
				dirs.remove(folder)
			except ValueError:
				pass

	for leaf in dirs:
		 
		info=[]
		fullleaf = os.path.join(basefolder,leaf)
		isFile=False
		isDir=False
		isLink=False
		
		(isFile,isDir,isLink) = _leaf_type(ctl, fullleaf)

                if __name__ == "__main__":
		    info.extend(indent)
		    _info_highlight(info, ctl, leaf, isLink)
                else:
                    _info_formating(info, ctl, leaf, isLink)

		if not ctl['q'] and not isDir: 
				info.append(_cateye_docat(fullleaf, isFile))
		
                if __name__ == "__main__":		
		    print(string.join(info,""))
                else:
                    ret_data += info

		
		if ctl['r']:
			if ctl['l'] and isLink:
				pass

			elif isDir:
				ctl["rec_cnt"]+=1;
				cateye(ctl, fullleaf)
				ctl["rec_cnt"]-=1;

        return ret_data


def _cateye_errexit(err, ret_code, show_usage=False):
	""" error processing function """
	print "!!! Terminated by " + str(err)
	if show_usage is True:
		_cateye_usage()
	sys.exit(ret_code)

	

def _opts_parse(ctl):
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], "cd:hls:qrx:", ["help",])
	except getopt.GetoptError as err:
		_cateye_errexit(err, 2, True)
	
	for op, ar in opts:
		if op == "-d":
			try:
				cateye_ctl["regular_time"] = float(ar)
			except ValueError as err:
				_cateye_errexit(err, 3, True)	
		elif op in ("-h","--help"):
			_cateye_usage()
			sys.exit(0)
		elif op == "-s":
			cateye_ctl["sval"] = ar
		elif op == "-q":
			cateye_ctl['q']=1
		elif op == "-r":
			cateye_ctl['r']=1
		elif op == "-l":
			cateye_ctl['l']=1
		elif op == "-c":
			cateye_ctl['c']=1
		elif op == "-x":
			cateye_ctl["d_except"]=ar
			
	if len(opts) != 1 and cateye_ctl["sval"] != "":
		_cateye_errexit("Warning: -s option shall not use with other options.", 6, True)

	return args


if __name__ == "__main__":

	args = _opts_parse(cateye_ctl)
		
	while True:
		if len(args) is not 1:
			_cateye_errexit("wrong path specified", 5, True)
			
		if cateye_ctl["sval"] is not "":
			_cateye_dowrite(str(args[0]), cateye_ctl["sval"])
			sys.exit(0)

		try:
			cateye(cateye_ctl, str(args[0]))
		except IndexError as err:
			_cateye_errexit(err, 4)

		if not cateye_ctl["regular_time"]:
			sys.exit(0)

		time.sleep(cateye_ctl["regular_time"])


