import task, time, random
import server, data
from credentials import get_nova_credentials_v2
from novaclient.client import Client
from threading import Thread, Lock
from Queue import Queue

admQ = Queue(30)
recQ = Queue()
glist = []
tmplist = []
vm_maxsize = 16
vm_size = 0
theta = 0.373
g = 6

lock = Lock()
lambas = []
lambds = task.lambds(10,0.008,0.08,4)
filenames = []
filenames = data.filenames(lambds)

#lambd = lambds[4] 
#filename = filenames[4]
lambd=0.0431
filename='tmpfile00431'
miup = 1.3*lambd 
servers_list = []
ISOTIMEFORMAT = '%Y-%m-%dT%XZ'
credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)

class DetVMThread(Thread):
    def run(self):
	global recQ
	global tmplist, servers_list
	global miup, vm_maxsize, vm_size
	global nova_client
	global filename
	while True:
	    try:
	        lock.acquire()
   	        servers_list = nova_client.servers.list()
	        vm_size = len(servers_list); print "SIZE: ", vm_size
	        lock.release()
	    except:
		print "servers_list tmp error"
		pass
	    if len(tmplist) != 0:
	        for s in servers_list:
		    for item in tmplist:
		        (vm_name, start_response, start_create)=(item[0], item[1],item[2])
	                if s.name == vm_name:
	                    print vm_name, start_response, start_create
                            status = data.get_instance_status(vm_name)
	                    created_time = data.get_instance_info(vm_name)
	                    if status == "ERROR":
				instance_final = time.strftime(ISOTIMEFORMAT,time.localtime())
	                        print "error\n", status, item
	                        data.write2file(filename, vm_name, start_response, start_create, created_time, instance_final, status) 
                                new_rec = task.re_creator_x(vm_name, miup)
                                new_lt = new_rec.items()
				
     	                        recQ.put(new_lt); 
                                recQ.task_done()
				tmplist.remove(item)
                                nova_client.servers.delete(s)
				servers_list.remove(s)
		                print "delete error instance\n"
	    	            if status == "ACTIVE":
				instance_final = time.strftime(ISOTIMEFORMAT,time.localtime())
	    	                print "XXX\n",status, item
	        	        time.sleep(30)
	                        data.write2file(filename, vm_name, start_response, start_create, created_time, instance_final, status)
				tmplist.remove(item)
                                nova_client.servers.delete(s)
				servers_list.remove(s)
	                        print "completed server: ", vm_name

class ProducerThread(Thread):
    def run(self):
	global admQ, recQ
	global tmplist, servers_list
	global start_response, vm_size, vm_maxsize
	global lambd
        while True:	
	    t = task.creator_x(1, lambd)
	    lt = t.items()
	    vm_name, flavor_name, key_name, start_response, image_name, delay, net_label = task.unpack_x(lt)
	    if not admQ.full():
	        admQ.put(lt)
	        time.sleep(delay)	
	    else:
                x0 = random.uniform(0.0, 1.0)
	        if x0 < theta:
           	    continue
	   	else:
		    recQ.put(lt)
		    time.sleep(delay)	
	    print "\nProducer admQ size: ", admQ.qsize()
 	    print 'Producer recQ: ',recQ.qsize()
	    print 'Producer tmplist ',len(tmplist)
	    print 'Producer servers_list ',servers_list
	    print 'Producer vm_size ',vm_size
	    print 'Producer lambd ',lambd
	    print 'Producer filename ',filename
	    print '\n'

class ConsumerThread(Thread):
    def run(self):
	global admQ, recQ
	global tmplist, servers_list
	global vm_size, vm_maxsize, lock
	while True:
	    try :
 	        if vm_size <= vm_maxsize:
	            item = admQ.get()
	    	    vm_name, flavor_name, key_name, start_response, image_name, delay, net_label = task.unpack_x(item)
                    start_create = server.create_x(vm_name, image_name, flavor_name, net_label, key_name)
                    tmplist.append((vm_name, start_response, start_create))
	    except ImportError:
		print "create server error\n"
		pass

class RecycleThread(Thread):
    def run(self):
	global admQ, recQ, vmQ
	global g, vm_size, vm_maxsize
	while True:
            if recQ.qsize() >= g:
	        print 'recycle'
                for i in range(g):
                    rec_t = recQ.get()
	    	    vm_name, flavor_name, key_name, start_response, image_name, delay, net_label = task.unpack_x(rec_t)
                    if not admQ.full():
			time.sleep(delay)
                        admQ.put(rec_t); print "Produced recQ's task enter admQ"
                    else:
                        x00 = random.uniform(0.0, 1.0);
                        if x00 < theta:
                            continue
                        else:
                            recQ.put(rec_t)

ProducerThread().start()
ConsumerThread().start()
DetVMThread().start()
RecycleThread().start()
