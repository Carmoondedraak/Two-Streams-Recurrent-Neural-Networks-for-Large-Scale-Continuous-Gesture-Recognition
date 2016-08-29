# -*- coding: cp936 -*-
#funtion:read ChaLearn dataset
#author@zhipeng.liu
#date:2016.7.29
#input:Txtpath
#output:list:data and label
import sys,os
import scipy.io as sio
import matplotlib.pyplot as plt
from numpy import *
from readTxt import readMatrixFromTxt
from GetSubfileName import *
from scipy.linalg.misc import norm
import scipy.io as sio
from readHandHog import *
import h5py
import re
from math import *
def IsInlist(onelist, key):
	for element in onelist:
		if element == key:
			return 1
	return 0
def Generate_final_submission_file(resulth5filename = None, seginfopath = None, myConGsubfile = None, testvideolistfile = None):
	r = re.compile('[ \t\n\r:,/]+')

	h5stream = h5py.File(resulth5filename, 'r')
	videoid = h5stream['xtestVideoId'][:]
	result_class = h5stream['result_class'][:]
	h5stream.close()

	NumAviVideo = videoid.shape[0]
	resultvideoDic = {-1: -1}			#videoid to result lineid
	for i in range(NumAviVideo):
		onevideoId = videoid[i]
		resultvideoDic[onevideoId] = i


	
	validvideoLabel = []
	validvideoDevel = []
	validlabestr = []
	listvideoid = []

	teststream = open(testvideolistfile, 'r')
	testAlline = teststream.readlines()
	testfilelineNum = len(testAlline)
	teststream.close()
	for i in range(testfilelineNum):
		oneline = testAlline[i]
		linespilt = r.split(oneline)
		Develid = int(linespilt[0])
		videoid = int(linespilt[1])

		validvideoDevel.append(Develid)
		validvideoLabel.append([])		
		listvideoid.append(videoid)

		oneisosefinfo = seginfopath + '/' + linespilt[0] + '/' + linespilt[1] + ".txt"
		oneseginfo_stream = open(oneisosefinfo, 'r')
		alllines = oneseginfo_stream.readlines()##it may be void
		oneseginfo_stream.close()
		print "%d/%d" % (Develid, videoid)
		numline = len(alllines)	

		strtmp = ""
		resultvideoidbegin = (Develid * 10000 + (videoid % 50) ) * 100
		print "resultvideoidbegin:", resultvideoidbegin

		if numline == 0:
			k = 1					##if segfile is void, we count Isovidos from one.
			resultvideoid = resultvideoidbegin + k
			if resultvideoDic.has_key(resultvideoid):				
				lineid = resultvideoDic[resultvideoid]
				oneIsovideoLabel = result_class[lineid] + 1
				validvideoLabel[i].append(oneIsovideoLabel)
				strtmp = " 1,10:" + str(oneIsovideoLabel)
				print "first has key"
			else:
				print "first no key"
				oneIsovideoLabel = 1
				validvideoLabel[i].append(oneIsovideoLabel)
				strtmp = " 1,10:1"	
			print "Void!"			
		else:
			startlist = []
			endlist = []
			for j in range(numline):
				resultvideoid = resultvideoidbegin + j ##count from 0
				if resultvideoDic.has_key(resultvideoid):
					lineid = resultvideoDic[resultvideoid]
					oneIsovideoLabel = result_class[lineid] + 1
					validvideoLabel[i].append(oneIsovideoLabel)
					start = 0
					end = 1
					seginfostr = alllines[j]
					seginforsplit = r.split(seginfostr)

					start = int(seginforsplit[0])
					end = int(seginforsplit[1])
					startlist.append(start)
					endlist.append(end)
					
			numlabel = len(validvideoLabel[i])
			
			for j in range(numlabel):
				label = validvideoLabel[i][j]
				start = startlist[j]
				end = endlist[j]
				strtmp = strtmp + " %d,%d:%d" % (start, end, label)
			if numlabel == 0:  # if the seg file is deleted in the resultvideoDic
				strtmp = " 1,10:1"
				print 'second no key'
		validlabestr.append(strtmp)
	substream = open(myConGsubfile, 'w')
	for i in range(testfilelineNum):
		strtmp = "%03d/%05d" % (validvideoDevel[i], listvideoid[i])  + validlabestr[i] + "\n"
		substream.write(strtmp)
	substream.close()	

if __name__ == '__main__':
	resulth5filename = '/home/zhipengliu/ChaLearn2016/experimentResult/ConG/result_ConGTesthogDim_testVideoId_V3_Depth_RGB_SkeHandHogTest_SimpleRNN_LSTM_ regular000_000_00_l2(0.01)T10.h5'
	seginfopath = '/home/zhipengliu/ChaLearn2016/ConGTestSegInfo'
	myConGsubfile = '/home/zhipengliu/ChaLearn2016/ConGResult/sub.txt'
	testvideolistfile = '/home/zhipengliu/ChaLearn2016/ConGResult/test.txt'
	Generate_final_submission_file(resulth5filename, seginfopath, myConGsubfile, testvideolistfile)


	