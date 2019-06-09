
import subprocess, os, sys, time

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
    log = open('iwdp.txt', 'a')
    log.write('some text, as header of the file\n')
    log.flush()
    popen = subprocess.Popen(cmd, shell=True,stdout=log, universal_newlines=True,preexec_fn=os.setsid)
    #stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ap.append(popen)
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

'''
    ios_webkit_debug_proxy -c <udid>:<27753+x*1000> -d -F
    
    
    '''

udid = sys.argv[-2]
i = int(sys.argv[-1])
ctx = 'ios_webkit_debug_proxy -c '+udid+':'+str(8000+i) +' -d -F'

j = 0
while 1:
    j+=1
    try:
        ic = execute(ctx)
    except:pass
    if (j==20):
        exit(-1)
