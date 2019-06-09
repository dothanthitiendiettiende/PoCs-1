
import subprocess, os, sys, time, socket


ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.connect(('8.8.8.8',80))
ip = ss.getsockname()[0]


reload(sys)
sys.setdefaultencoding('utf8')

import atexit
ap = []

def cleanup():
    for p in ap:
        p.kill()



atexit.register(cleanup)

def hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        cleanup()
    else:
        cleanup()

sys.excepthook = hook

def execute(cmd):
    log = open('appium.txt', 'a')
    log.write('some text, as header of the file\n')
    log.flush()
    popen = subprocess.Popen(cmd, shell=True, stdout=log, universal_newlines=True, preexec_fn=os.setsid)
    #stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ap.append(popen)
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

'''
  appium --address <ip address> --port <4723+x> --webkit-debug-proxy-port <27753 + x * 1000>
    '''

if not sys.argv[-1] == 'localhost':

    udid = sys.argv[-2]
    i = int(sys.argv[-1])
    wp = str(8000+i)
    p = str(4723+i)
    ctx = 'appium --address '+ip+' --port '+p+' --webkit-debug-proxy-port '+wp

    j = 0
    while 1:
        j+=1
        try:
            ic = execute(ctx)
        except:pass
        if (j==20):
            exit(-1)

else:

    udid = sys.argv[-3]
    i = int(sys.argv[-2])
    wp = str(8000+i)
    p = str(4723+i)
    ctx = 'appium --address localhost --port '+p+' --webkit-debug-proxy-port '+wp
    
    j = 0
    while 1:
        j+=1
        try:
            ic = execute(ctx)
        except:pass
        if (j==20):
            exit(-1)

