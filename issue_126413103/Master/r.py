
import subprocess, os, sys, time, socket, signal


ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.connect(('8.8.8.8',80))
ip = ss.getsockname()[0]


reload(sys)
sys.setdefaultencoding('utf8')

def stop(pd):
    os.kill(pd.pid, signal.SIGTERM) #or signal.SIGKILL


import atexit
ap = []

def cleanup():
    for p in ap:
        stop(p)
        try:
            p.kill()
        except:pass



atexit.register(cleanup)

#def hook(exctype, value, traceback):
#    if exctype == KeyboardInterrupt:
#        cleanup()
#    else:
#       cleanup()

#sys.excepthook = hook

def execute(cmd):
    
    log = open('run.txt', 'a')
    log.write('some text, as header of the file\n')
    log.flush()
    fd = open('pid.txt', 'w')
    os.chdir(os.path.abspath(os.path.abspath(os.curdir).split('/Desktop')[0]+'/Desktop/automation'))
    
    popen = subprocess.Popen(cmd, shell=True, stdout=log, stderr=log, universal_newlines=True,preexec_fn=os.setsid)
    
    #print popen.pid
    fd.write(str(popen.pid))
    fd.close()
    ap.append(popen)
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)





argfile = 'args.txt'
arguments = ''
t_ = sys.argv[-1]

with open(argfile,mode='r') as args:
    for line in args.readlines():
        if line == '' or line == None:
            continue
        if '&&&&&&&&&&&&&&&&' in line:
            arguments += ' '+line.replace('\n','').replace('&&&&&&&&&&&&&&&&',t_)
        else:
            arguments += ' '+line.replace('\n','')

if (len(arguments.split(' '))<3):
    exit(-17)

ctx = 'java -jar runner.jar'+arguments

j = 0
try:
    ic = execute(ctx)
except Exception as e:
    #print e
    exit(-1)
    pass

