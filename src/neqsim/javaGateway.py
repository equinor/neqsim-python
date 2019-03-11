import os
from os import path
import pkg_resources
import subprocess
import shlex
import os

def startServer():
    localosname = os.name
    colon = ':'
    if(localosname == 'nt'):
        colon=';'
    resources_dir = pkg_resources.resource_filename('neqsim', 'lib/')
    #resources_dir = "/usr/local/lib/python3.6/dist-packages/neqsim/lib"
    fullstring = shlex.split('java -classpath '+resources_dir+'/NeqSimpy4j.jar'+colon+resources_dir+'/NeqSimSource.jar'+colon+resources_dir+'/py4j0.10.8.1.jar neqsimpy4j.startJavaGateway')
    pipe = subprocess.Popen(fullstring,stdout=subprocess.PIPE, stderr=subprocess.PIPE)