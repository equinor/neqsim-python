import os
from os import path
from py4j.java_gateway import JavaGateway
import pkg_resources
local_os_name = os.name
colon = ':'
if local_os_name == 'nt':
    colon = ';'

try:
    port
except NameError:
    #print("port not defined. setting it to port=0")
    port=0
else:
    port = port
    #print("port defined")
    
def create_classpath(jars):
    resources_dir = pkg_resources.resource_filename('neqsim', 'lib/')
    return colon.join([path.join(resources_dir, jar) for jar in jars])


def start_server():
    jars = ['NeqSim.jar']
    classpath = create_classpath(jars)
    if port==0:
       return JavaGateway.launch_gateway(classpath=classpath, die_on_exit=True)
    else:
       return JavaGateway.launch_gateway(port=port,classpath=classpath, die_on_exit=True)


