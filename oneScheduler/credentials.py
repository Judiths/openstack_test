from os import environ as env
#import keystoneclient.v2_0.client as ksclient

def get_nova_credentials_v2():
    d={}
    d['version'] = '2'
    d['username'] = env['OS_USERNAME']
    d['api_key'] = env['OS_PASSWORD']
    d['auth_url'] = env['OS_AUTH_URL']
    d['project_id'] = env['OS_TENANT_NAME']
    return d
#credentials = get_nova_credentials_v2()

def get_ceilometer_credentials_v2():
    d={}
    d['os_username'] = 'demo'
    d['os_password'] = 'demo'
    d['os_auth_url'] = 'http://172.20.52.39:5000'
    d['os_tenant_name'] = 'demo'
    return d
