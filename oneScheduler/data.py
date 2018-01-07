import os, re, time
import os.path
import numpy as np
import ceilometerclient.client
from credentials import get_nova_credentials_v2
from novaclient.client import Client

def c_client():
    cclient = ceilometerclient.client.get_client(2,
                           os_username='demo',
                           os_password='demo',
                           os_tenant_name='demo',
			   os_auth_url='http://172.20.52.39:5000')
    return cclient

def get_instance_info(vm_name):
    str0 = os.popen("nova show "+ vm_name + "|grep status").read()
    a0 = re.sub(r'\s', "", str0)
    b0 = re.sub(r'\|', "", a0)
    status = re.sub(r'[a-z]',"",b0)
    str1 = os.popen("nova show "+ vm_name + "|grep created").read()
    a1 = re.sub(r'\s', "", str1)
    b1 = re.sub(r'\|', "", a1)
    if status == 'ERROR':
	c1 = re.sub(r'fault.*$',"",b1)
	created_time = re.sub(r'[a-z]',"",c1)
	return created_time
    else:
	created_time = re.sub(r'[a-z]',"",b1)
        return created_time	

def get_instance_status(vm_name):
    str0 = os.popen("nova show "+ vm_name + "|grep status").read()
    a0 = re.sub(r'\s', "", str0)
    b0 = re.sub(r'\|', "", a0)
    status = re.sub(r'[a-z]',"",b0)
    return status

def filenames(lambds):
    filenames = []
    for lambd in lambds:
        print lambd
        a= str(lambd)
        x = re.sub(r'\.', "", a)
        filename = 'tmpfile'+x; print filename
   	filenames.append(filename)
    return filenames

def write2file(filename, vm_name,
			 start_response, start_createtime, 
			 created_time, instance_final, status):
    f = file('/home/controller/oneScheduler/'+ filename,'a+')
    line = vm_name+'\t'+start_response+'\t'+start_createtime+'\t'+created_time+'\t'+ instance_final +'\t'+status+'\n'
    f.writelines(line)
    f.close()

def dataHandler(filename,A):
    array = []
    history_response = []
    for line in open('./'+ filename):
	linex = line.replace('\n','')
   	it = linex.split('\t');print it
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
    return history_response, array, level_num

def oneScheduler(level_num):
    
   return ''
