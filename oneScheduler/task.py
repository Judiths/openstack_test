import random, time
from random import choice

#  
#
def lambds(num, start, end, bit):
    lambds = []
    for i in range(num):
	    delta = (end-start)/num
            it = round(random.uniform(start + i*delta, start + (i+1)*delta),bit)
            lambds.append(it)
    return lambds

def creator(num, lambd):
    task = {}
    for i in range(num):
	ISOTIMEFORMAT = '%Y-%m-%dT%XZ'
    	start_response = time.strftime(ISOTIMEFORMAT,time.localtime())
        vm_name = "vm_"+ str(random.randint(0,10000))+random.choice('abcdefghijklmnopqrstuvwxyz')
        interval = round(random.expovariate(lambd),4)
        task.setdefault(vm_name,{})["interval"]=interval
        flag = random.uniform(0.0, 1.0)
        if flag < 0.1:
            task.setdefault(vm_name,{})["status"] = "error"
        if flag > 0.1:
            task.setdefault(vm_name,{})["status"] = "right"
        task.setdefault(vm_name,{})["start_response"] = start_response
    return task

def creator_x(num, lambd):
    task = {}
    images = ['cirros','fedora','ubuntu']
    flavors = ['m1.test', 'm1.tiny', 'm1.small', 'm1.medium']
    networks_labels = ['private']
    key_names = ['demo_keypair']
    for i in range(num):
	ISOTIMEFORMAT = '%Y-%m-%dT%XZ'
    	start_response = time.strftime(ISOTIMEFORMAT,time.localtime())
        vm_name = "vm_"+ str(random.randint(0,10000))+random.choice('abcdefghijklmnopqrstuvwxyz')
	image_name = choice(images)
	flavor_name = choice(flavors)
	net_label = choice(networks_labels)
	key_name = choice(key_names)
        interval = round(random.expovariate(lambd),4)
        task.setdefault(vm_name,{})['interval']=interval
        task.setdefault(vm_name,{})['image_name'] = image_name
        task.setdefault(vm_name,{})['flavor_name'] = flavor_name
        task.setdefault(vm_name,{})['net_label'] = net_label
        task.setdefault(vm_name,{})['key_name'] = key_name
        task.setdefault(vm_name,{})["start_response"] = start_response
    return task

def unpack_x(tasklist):
    vm_name = tasklist[0][0]
    start_response = tasklist[0][1].values()[0]
    delay = tasklist[0][1].values()[1]
    image_name = tasklist[0][1].values()[2]
    net_label = tasklist[0][1].values()[3]
    flavor_name = tasklist[0][1].values()[4]
    key_name = tasklist[0][1].values()[5]
    return vm_name, key_name, image_name, delay, flavor_name, net_label, start_response


def re_creator_x(vm_name, miup):
    task = {}
    images = ['cirros','fedora','ubuntu']
    flavors = ['m1.test', 'm1.tiny', 'm1.small', 'm1.medium']
    networks_labels = ['private']
    key_names = ['demo_keypair']
    ISOTIMEFORMAT = '%Y-%m-%dT%XZ'
    
    start_response = time.strftime(ISOTIMEFORMAT,time.localtime())
    vm_name = vm_name
    interval = round(random.expovariate(miup),4)
    image_name = choice(images)
    flavor_name = choice(flavors)
    net_label = choice(networks_labels)
    key_name = choice(key_names)
    task.setdefault(vm_name,{})['interval']=interval
    task.setdefault(vm_name,{})['image_name'] = image_name
    task.setdefault(vm_name,{})['flavor_name'] = flavor_name
    task.setdefault(vm_name,{})['net_label'] = net_label
    task.setdefault(vm_name,{})['key_name'] = key_name
    task.setdefault(vm_name,{})["start_response"] = start_response
    return task

def re_creator(vm_name, miup, fault):
    task = {}
    vm_name = vm_name
    interval = round(random.expovariate(miup),4)
    task.setdefault(vm_name,{})["interval"]=interval
    flag = random.uniform(0.0, 1.0)
    if flag < fault:
        task.setdefault(vm_name,{})["status"] = "error"
    if flag > fault:
        task.setdefault(vm_name,{})["status"] = "right"
    ISOTIMEFORMAT = '%Y-%m-%dT%XZ'
    start_response = time.strftime(ISOTIMEFORMAT,time.localtime())
    task.setdefault(vm_name,{})["start_response"] = start_response
    return task

def task_partial(startT, xtask, xtask_maxsize, extask):
    tmp = {}
    for i in range(xtask_maxsize):
        key = choice(startT.keys())
        value = startT.get(key)
        tmp[key] = value
        xtask.update(tmp)
        startT.pop(key)
    extask = startT
    return xtask,extask
    
def unpack(tasklist):
    vm_name = tasklist[0][0]
    status = tasklist[0][1].values()[0]
    start_response = tasklist[0][1].values()[1]
    delay = tasklist[0][1].values()[2]
    return vm_name, status, start_response, delay

def glists(task, g, glists):
    for j in task.items():
        status = j[1].values()[0]
        delay = j[1].values()[2]
        print "status: ", status
        print "delay: " , delay
        time.sleep(delay)
    glists = [task.items()[i:i+g] for i in range(len(task.items())) if i%g==0]
    return glists

def miux(vm_size, miu0, miux):
    if vm_size == 0:
	return miux0
    else:
    	level = vm_size/1   # floor 
    	rank = {}
    	#miu0 = 0.001; 
    	d = 1.0
    	for i in range(level):
            rank_title = i
            miux = round(miu0*(d**i), 4)
            rank[rank_title] = miux
        return rank.values()[vm_size-1]

