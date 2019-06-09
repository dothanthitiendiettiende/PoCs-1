
import subprocess, os, sys, time

reload(sys)
sys.setdefaultencoding('utf8')

time.sleep(5)
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
    log = open('yy.txt', 'a')
    log.write('some text, as header of the file\n')
    log.flush()
    popen = subprocess.Popen(cmd, stdout=log, universal_newlines=True, preexec_fn=os.setsid)
        #for stdout_line in iter(popen.stdout.readline, ""):
        #    log.write(stdout_line)
        #   yield stdout_line
        #popen.stdout.close()
    ap.append(popen)
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

'''
    ['/usr/bin/xcodebuild',
    #     '-project', 'WebDriverAgent.xcodeproj',
    #     '-scheme', 'WebDriverAgentRunner',
    #     '-destination', 'id='+self.udid, 'test']
'''

with open('error.txt', mode="w") as t:
    g = sys.argv[-1]
    os.chdir(os.path.abspath(g))
    udid = sys.argv[-2]
    ctx = ['xcodebuild','test-without-building',
         '-project', 'WebDriverAgent.xcodeproj',
         '-scheme', 'WebDriverAgentRunner',
        '-destination', 'id='+udid, 'test']

    execute(ctx)
    
#for l in execute(ctx):
        #print l
#t.write(l)


