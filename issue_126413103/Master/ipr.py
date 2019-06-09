
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
    
    popen = subprocess.Popen(cmd, shell=True,preexec_fn=os.setsid)
    #stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ap.append(popen)
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

udid = sys.argv[-1]

ctx = 'iproxy 22222 8100 '+udid

j = 0
while 1:
    j+=1
    try:
        ic = execute(ctx)
    except:pass
    if (j==20):
        exit(-1)
