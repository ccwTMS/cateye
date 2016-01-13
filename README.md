# cateye
Cateye is a simple access tool used to explore the Linux system information (/proc and /sys)

　

usage: cateye.py [path] [OPTION]

[OPTION]:

-c　　　　　　: Turn colorization off. for dumping output information to file. 

-d seconds　　: Update regularly at interval of seconds, where the "seconds" can be float point number. 

-h,--help　　　: It shows this usage.

-l　　　　　　: To show symbolic link's real path, and to prevent infinite loop.(available when -q option is enabled.)

-r　　　　　　: It recursively works in folder for list function. (likes tree)

-s parameters　: To write parameters to file. use "" when parameters more than one.

-q　　　　　　: Quiet, It shows filename only, no content of file.

-x foldernames : ignores specified folders. (foldernames: "folder1 folder2 ...")
