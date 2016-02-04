# -*- coding: latin-1 -*-

import os
import jpype

jvmPath=jpype.getDefaultJVMPath()
print jvmPath

# jpyejvm
# if(jpype.isJVMStarted()):
# 	print "attachToJVM"
# 	jpyejvm = jpype.attachToJVM()
# else:
print "startJVM"
jpyejvm = jpype.startJVM(jvmPath)

def JPypeCall():
	print "start jpype"
	if(jpyejvm):
		jpype.java.lang.System.out.println("hello world!")
	else:
		InitJPypeJVM()
		jpype.java.lang.System.out.println("hello world from new jvm!")
	# jpype.shutdownJVM()


def PyjniusCall():
	pass

def InitJPypeJVM():
	# if(jpyejvm):
	# 	print "jvm is already running"
	# 	jpyejvm = jpype.attachToJVM()
	# else:
    print "init jvm for jpype"
    try:
        jpyejvm = jpype.startJVM(jvmPath)
    except Exception, e:
        print e
        jpype.shutdownJVM();
        jpyejvm = jpype.startJVM(jvmPath)
    
	print "JVM is started"
	
def ShutdownJpypeJVM():
	if(jpyejvm):
		jpype.shutdownJVM()
		print "JVM is shuted down"
	print "the end"


for i in range(100):
	JPypeCall()

ShutdownJpypeJVM()