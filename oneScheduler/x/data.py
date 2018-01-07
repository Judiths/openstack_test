import os, re, time
import os.path
import numpy as np

def dataHandler(filename,A):
    array = []
    history_response = []
    for line in open(filename):
	linex = line.replace('\n','')
   	it = linex.split('\t')#;print it
	if it[3] != '':
	    a = it[1].replace('Z','')
	    start = a.replace('T',' ')
	    b = it[3].replace('Z','')
	    end = b.replace('T',' ')
	    timeArray_start = time.strptime(start,'%Y-%m-%d %H:%M:%S')
	    timeArray_end = time.strptime(end,'%Y-%m-%d %H:%M:%S')
	    timeStamp_start = int(time.mktime(timeArray_start))
	    timeStamp_end = int(time.mktime(timeArray_end))
 	    response_time = timeStamp_end - timeStamp_start #response time
	    history_response.append(response_time)
	    it.append(response_time)
        array.append(it)
    level_num = sum(history_response)/len(history_response)*(1+A)
    return history_response, level_num

def oneScheduler(level_num):
    
   return ''
