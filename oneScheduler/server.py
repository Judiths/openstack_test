import time
from credentials import get_nova_credentials_v2
from novaclient.client import Client

ISOTIMEFORMAT = '%Y-%m-%dT%XZ'
def vm_size(server_list):
    vm_size = len(server_list)
    return vm_size

def vm_list():
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)
    server_list = nova_client.servers.list()
    return server_list
    
def create(vm_name):
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)
    start = time.time()
    start_create = time.strftime(ISOTIMEFORMAT,time.localtime())   
    try:
	print "Start Create Server"
	image = nova_client.images.find(name="cirros")
	flavor = nova_client.flavors.find(name="m1.tiny")
    	net = nova_client.networks.find(label="private_network")
    	nics = [{'net-id': net.id}]
	print vm_name, image, flavor, net,nics
    	instance = nova_client.servers.create(name=vm_name, image=image,flavor=flavor, key_name="mm-keypair", nics=nics)
        print "create vm delay %f s" % delay
        time.sleep(delay)
        print nova_client.servers.list()
	end = time.time()
	print "used time: %f s" %(end - start)
    finally:
	return start_create

def create_x(vm_name, image_name, flavor_name, net_label, key_name):
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)
    start = time.time()
    start_create = time.strftime(ISOTIMEFORMAT,time.localtime())   
    try:
	print "Start Create Server"
	image = nova_client.images.find(name=image_name)
	flavor = nova_client.flavors.find(name=flavor_name)
    	net = nova_client.networks.find(label=net_label)
    	nics = [{'net-id': net.id}]
#	print vm_name, image, flavor, net,nics
    	instance = nova_client.servers.create(name=vm_name, image=image,flavor=flavor, key_name=key_name, nics=nics)
        print "create vm delay %f s" % delay
        time.sleep(delay)
        print nova_client.servers.list()
	end = time.time()
	print "used time: %f s" %(end - start)
    finally:
	return start_create

def delete(vm_name):
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)
    servers_list = nova_client.servers.list()
    print servers_list
    start = time.time()
    server_exists = False
    for s in servers_list:
	if s.name == vm_name:
	    print "Start to Delete Server %s " % vm_name
	    server_exists = True
	    break
    if not server_exists:
	print "server %s does not exist" % vm_name
    else:
	nova_client.servers.delete(s)
	end = time.time()
	print "server %s deleted " % vm_name 
	print "used %f s" %(end-start)
    return True

def running_time(vm_name, active_time):
    try:
    	server.create(vm_name)
        time.sleep(active_time)
        server.delete(vm_name)
        print "server "+vm_name+"runing ",active_time
    finally:
	return "xxx"
