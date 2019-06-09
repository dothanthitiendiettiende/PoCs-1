#!/usr/bin/python
import os, subprocess, sys, time, atexit, datetime, socket
import signal

import traceback

ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.connect(('8.8.8.8',80))
gip = ss.getsockname()[0]

reload(sys)
sys.setdefaultencoding('utf8')

pipe = subprocess.Popen('id',
                        shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = pipe.communicate()

def cls():

    from platform   import system as system_name  # Returns the system/OS name
    from subprocess import call   as system_call  # Execute a shell command

    def clear_screen():

        command = 'cls' if system_name().lower()=='windows' else 'clear'
    
        system_call([command])

    clear_screen()

@atexit.register
def cleanup():
    d = '.'
    rmlist = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    pipe = subprocess.Popen("ps aux |grep python |grep -v 'master.py' |awk '{print $2}' |xargs kill",
                            shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for r in rmlist:
        pipe = subprocess.Popen("rm -r "+r,
                                shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        cleanup()
    else:
        cleanup()
        sys.__excepthook__(exctype, value, traceback)

sys.excepthook = hook

def _stop(p):
    os.kill(p.pid, signal.SIGTERM) #or signal.SIGKILL


if 'uid=0' in out:
    print 'never run this program as root!'
    print 'please run this as a normal user and try again'
    exit(-1)

class Utils:
    def __init__(self):
        self.wd = os.getcwd()
    
    def runcommand(self,c):
        try:
            pipe = subprocess.Popen(c,
                                    shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,preexec_fn=os.setsid)
            return True
        except Exception as e:
            return False

    def runcommandAndGetOutPut(self,c):
        try:
            pipe = subprocess.Popen(c,
                                    shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,preexec_fn=os.setsid)
            out, err = pipe.communicate()
            return out.decode()
        except Exception as e:
            return e
    def checkfile(self,p):
        return os.path.isfile(p)

    def checkdir(self,p):
        return os.path.exists(p)

    def createfile(self,n):
        return self.runcommand("touch "+n)

    def createdir(self,n):
        return self.runcommand("mkdir "+n)

    def nothing(self):
        print('...')
        time.sleep(30)

    def runcommandReturnP(self,wdir,c):
        os.chdir(wdir)
        pipe = subprocess.Popen(c,
                                shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)

        os.chdir(self.wd)
        return pipe

class Commander:
    
    def __init__(self):
        
        self.nord = 0
        
        dg = raw_input('would you like to use nordvpn? (yes/no)')
        if (dg == 'yes'):
            self.nord = 1
        elif (dg == 'no'):
            pass
        else:
            print 'invalid answer'
            exit(-1)
        
        
        try:
            p = os.path.abspath(os.curdir).split('/Desktop')[0]
            prefix = p+'/Desktop/automation/dict/locations.txt'
            cnt = 0
            prefix1 = p+'/Desktop/automation/dict/search.txt'
            cnt1 = 0
            locations = []
            with open(os.path.abspath(prefix),mode='r') as loc:
                for l in loc.readlines():
                      cnt += 1
                      if ' ' in l:
                        lst = l.split(' ')
                        le = len(lst)
                        if (le != 3) and (le != 2):
                            print 'locations file error at line ' + str(cnt) + ':\n'+l
                            print 'example line:\nSan%20Francisco &tci=g:1014221 &uule=w+CAIQICImU2FuIEZyYW5jaXNjbyxDYWxpZm9ybmlhLFVuaXRlZCBTdGF0ZXM'
                            print 'please correct this line.'
                            exit(-1)
                        else:
                            if ('tci' in l) and ('uule' in l):
                                locations.append(lst[0].lower().replace('%20',' '))
                                continue
                            else:
                                print 'locations file error at line ' + str(cnt) + ':\n'+l
                                print 'example line:\nSan%20Francisco &tci=g:1014221 &uule=w+CAIQICImU2FuIEZyYW5jaXNjbyxDYWxpZm9ybmlhLFVuaXRlZCBTdGF0ZXM'
                                print 'please correct this line.'
                                exit(-1)
            with open(os.path.abspath(prefix1),mode='r') as loc:
                for l in loc.readlines():
                    l = l.replace('#','')
                    cnt1 += 1
                    if ' ' in l:
                      lst = l.split(' ')
                      if not (lst[0].lower() in locations) and not ((lst[0].lower()+' '+lst[1].lower()) in locations):
                            print 'you are trying to search from locations that are not enlisted at the locations.txt file.'
                            print 'please correct line '+str(cnt1)+':\n'+l
                            print 'remove this search location, or add the location to locations.txt'
                            os.system('open -a safari http://isearchfrom.com/')
                            exit(-1)
        except Exception as error:
            print error
            
            print 'cannot locate locations.txt or search.txt at the /Desktop/automation/dict directory.'
            exit(-1)
        
                      
        prefix = gip.split('.')
        dip = ''
        for i in range(len(prefix)-1):
            dip += prefix[i] + '.'
        self.gip = dip
        
        self.Threads = []
        self.Slaves = {}
        self.devices = {}
        
        self.wd = os.getcwd()
        self.root = self.wd.split('/Desktop')[0]
        self.u = Utils()
        
        self.u.runcommand('killall -s SIGTERM node')
        self.u.runcommand('killall -s SIGINT node')
        self.u.runcommand('killall node')
        self.u.runcommand('killall xcodebuild')
        self.u.runcommand('killall ios_webkit_debug_proxy')
        self.u.runcommand('killall java')
        
        re = self.u.runcommandAndGetOutPut('instruments -s devices')
                      
        o = re.split('\n')
        y = 1
                      
        for j in o:
            if not ('(' in j) or ('Simulator' in j) or (len(j.split(' '))!=3):
                pass
            else:
                try:
                    lst = j.split(' ')
                    dname = lst[0]
                    osver = lst[1].replace('(','').replace(')','')
                    udid = lst[2].replace('[','').replace(']','')
                    self.devices[str(y)] = {}
                    self.devices[str(y)]['dname'] = dname
                    self.devices[str(y)]['osv'] = osver
                    self.devices[str(y)]['udid'] = udid
                    self.Threads.append([])
                    y += 1
                except Exception as err:
                    print err
                    exit(-1)
        
        
        Flag = False
                      
        while 1:
                      
            cls()
            print 'please reboot all ios devices connected to this computer'
            reboot = raw_input('would you like this program to reboot all connected devices(yes/no)?')
            if reboot == 'yes':
                print 'any device that is not successfuly rebooted by this program is invalid for installation..'
                print 'please check that the device is connected and trusts the computer.'
                print 'please see that the device is connected to the same wifi network as the computer as well.'
                print 'all invalid devices would be reported soon..'
                for dv in self.devices.keys():
                    #print self.devices[dv]['udid']
                    o = self.u.runcommandAndGetOutPut('idevicediagnostics -u '+self.devices[dv]['udid']+' restart')
                    #print o
                Flag = True
                print 'waiting for the devices to reboot.'
                print 'please make sure that all the devices are unlocked.'
                print 'please see that Nordvpn is installed and that the "disconnect"'
                print 'or the "connect" button are visable on screen.'
                print 'please see that if you open the settings application'
                print 'then its on the main screen or at the safari settings'
                print 'now please wait a few minutes for the devices to cool down'
                print 'go make yourself a coffee and come back.'
                for i in range(4):
                      self.u.nothing()
                break
            elif reboot == 'no':
                break
        
        counter = 0
        
        while 1:
            if Flag == True:
                break
            cls()
            print 'please reboot all ios devices connected to this computer'
            g = raw_input('did you reboot all devices(yes/no)?')
            if g == 'yes':
                print 'please make sure that all the devices are unlocked.'
                print 'please see that Nordvpn is installed and that the "disconnect"'
                print 'or the "connect" button are visable on screen.'
                print 'please see that if you open the settings application'
                print 'then its on the main screen or at the safari settings'
                print 'now please wait a few minutes for the devices to cool down'
                print 'go make yourself a cup of coffee and come back.'
                break
            elif g == 'no':
                pass
    
    def run(self):
        
        def removekey(d, key):
            try:
                r = dict(d)
                del r[key]
                return r
            except Exception as e:
                print e
                return d
                
        
        #if not (ord(sys.argv[-1][0]) == 100):
            #self.u.nothing()
        
        
        

        print 'available devices on the system:'
        for dv in self.devices.keys():
            print '[' + dv + ']: ' + self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv']
            self.Threads.append([])
        
        re = self.u.runcommandAndGetOutPut('idevice_id -l').split('\n')
        #print re
        for dvc in self.devices.keys():
            #print dvc
            #print self.devices[dvc]['udid'] in re
            if not (self.devices[dvc]['udid'] in re):
                print 'Error: the device ' + self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv'] + ' is not connected properly'
                print 'please reboot the device, dissconnect from the computer, reconnect and try again.'
                print 'please make sure that the device is connected to the same wifi network as the computer\nand that the computer is trusted by the device.'
                print 'when you are done you would be able to issue a reload command:'
                print '>reload '+self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv']
                print 'and try again.'
                print 'lets install other devices:please wait for the ">" to appear at the commandline to reload.'
                self.devices[dvc]['lock'] = True

        print 'would you like to run the program on all devices (yes/no)?'
        h = False
        while 1:
            g = raw_input('')
            if g == 'yes':
                break
            elif g == 'no':
                h = True
                break
            else:
                self.u.runcommand('clear')
                print 'would you like to run the program on all devices (yes/no)?'
    
        if h:
            le = len(self.devices)
            for t in range(1,le+1):
                while 1:
                    g = raw_input('would you like to operate device '+str(t) +'(yes/no)')
                    if g == 'yes':
                        break
                    elif g == 'no':
                        self.devices = self.devices[str(t)]['dont install'] = True
                        break

        cls()
                    
        print '[*] installing devices:'
        for dv in self.devices.keys():
            print '[' + dv + ']: ' + self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv']

        print 'please wait a few moments for the installation to finish..'
        
        counter = 0
        
        for dv in self.devices.keys():
            #self.u.mkdir(dv)
            if 'dont install' in self.devices[dv].keys():continue
            self.installDevice(dv,counter)
                    
            counter += 1
                


        while 1:
            
            cls()
            
            now = datetime.datetime.now()
            print now
            print 'Connected devices:'
            for dv in self.devices.keys():
                #self.u.mkdir(dv)
                print '[' + dv + ']: ' + self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv']

            print 'Installed Devices:'
            for dv in self.devices.keys():
                if 'wdurl' in self.devices[dv].keys():
                    print '[' + dv + ']: ' + self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv']
            
            print 'Running Devices:'
            tmp = []
            for dv in self.Slaves.keys():
                if not self.Slaves[dv]['process'].poll() == None:
                    tmp.append(dv)
                else:
                    for dvc in self.devices.keys():
                        if dv == self.devices[dvc]['dname']:
                            print '[' + dvc + ']: ' + self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv']

            for t in tmp:
                self.Slaves = removekey(self.Slaves,t)
            
            print 'to list available commands run:\n>help\n'

            ir = raw_input('>')
    
            if ir == 'help':
                print 'commands:'
                print '>reload [device name]'
                print '\nthe command checks if the device can be installed,\nif there was an installation error with the device before then you need to use this command\nto make installation available again.\nexample:\n>reload a'
                print '>install [device name]'
                print '\nthe command would try to install the automation on the device.\nexample:>install a'
                print '>reinstall [device name]'
                print '\nthe command would try to reinstall the automation on the device.\nexample:>reinstall a'
                print '>run [device name] [url]'
                print 'the command would run the automation on the specified device.\nonly devices that appear at the "installed devices" list can be run...'
                print 'example:\n>run a abc.xyz'
                print '>stop [device name]\nthecommand would stop the automation running at the device by name.\nthis would not remove the device from the "installed devices" list.\nexample:\n>stop a'
                print '>status\nThe command would refrash this screen'
                print '>show log\nThe command would print the log file.'
                print '>erase log\nThe command would erase the contents of the log file.'
                print '>[device name].arguments\nThe command would show the automation arguments for the device.'
                print '>[device name].arguments.add [argument]\nThe command would add an argument to the device.'
                print 'example:\n>a.arguments.add -changeip=false\nWARNING: adding invalid arguments might cause dysfunction.'
                print '>[device name].arguments.remove [argument]\nThe command would remove an argument from the device arguments list.'
                print 'WARNING: removing needed arguments might cause dysfunction.'
                print '>refrash devices\nThe command checks if any new device was connected to the computer.'
                print 'remeber that any device who is screen locked would not be recognized...'
                print '>exit\nterminate the programm and uninstall all devices.'
                itr = raw_input('enter anything to go back to main menu:')
            elif 'reload' in ir:
                try:
                    dn = ir.split(' ')[1]
                    re = self.u.runcommandAndGetOutPut('idevice_id -l').split('\n')
                    #print re
                    for dvc in self.devices.keys():
                        if not self.devices[dvc]['dname'] == dn:continue
                        #print dvc
                        #print self.devices[dvc]['udid'] in re
                        if not (self.devices[dvc]['udid'] in re):
                            print 'Error: the device ' + self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv'] + ' is not connected properly'
                            print 'please reboot the device, dissconnect from the computer, reconnect and try again.'
                            print 'please make sure that the device is connected to the same wifi network as the computer\nand that the computer is trusted by the device.'
                            print 'when you are done you would be able to issue a reload command:'
                            print '>reload '+self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv']
                            print 'and try again.'
                            self.devices[dvc]['lock'] = True
                            time.sleep(7)
                            break
                        else:
                            print 'The device '+self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv']+' is now connected correctly and can be installed.'
                            self.devices[dvc] = removekey(self.devices[dvc], 'lock')
                            time.sleep(7)
                            break
                except:
                    print 'error! invalid command'
                    time.sleep(7)
                
                
            elif 'install' in ir:
                try:
                    dn = ir.split(' ')[1]
                    re = self.u.runcommandAndGetOutPut('idevice_id -l').split('\n')
                    for dvc in self.devices.keys():
                        if not self.devices[dvc]['dname'] == dn:continue
                        #print dvc
                        #print self.devices[dvc]['udid'] in re
                        if 'wdurl' in self.devices[dvc].keys():
                            print 'Error: the device ' + self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv'] + ' is already installed..'
                            print 'if the device is causeing problems then please reinstall it with the "reinstall" command.'
                            time.sleep(7)
                            break
                        else:
                            try:
                                ij = self.installDevice(dvc,int(dvc)-1)
                                if ij == 0:
                                    print 'the device: '+ self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv'] + ' was installed.'
                                    time.sleep(7)
                                    break
                                else:
                                    print 'cound not install device.'
                                    time.sleep(7)
                                    pass
                            except:
                                print 'cound not install device.'
                                time.sleep(7)
                                pass
            
                except:
                    print 'error! invalid command'
                    time.sleep(7)

            elif 'run' in ir:
                try:
                    aaa = ir.split(' ')
                    t = aaa[2]
                    dn = aaa[1]
                    stop = False
                    for dvc in self.devices.keys():
                        if stop == True:
                            print 'success'
                            time.sleep(4)
                            break
                        if not self.devices[dvc]['dname'] == dn:continue
                        else:
                            if not self.devices[dvc]['dname'] in self.Slaves.keys():
                                runner = self.u.runcommandReturnP(os.path.abspath(os.curdir+'/'+dv),'python r.py '+t)
                                print 'loading ...'
                                for y in range(4):
                                    time.sleep(15)
                                    try:
                                        with open(os.path.abspath(os.curdir+'/'+dv+'/run.txt'),mode='r') as log:
                                            if runner.poll() == None:
                                                self.Slaves[self.devices[dvc]['dname']] = {}
                                                self.Slaves[self.devices[dvc]['dname']]['process'] = runner
                                                stop = True
                                                print 'the device: '+self.devices[dvc]['dname'] + '  has started to run.'
                                                time.sleep(4)
                                                break
                                    except:
                                        print 'unable to run device, please make sure that the device is installed.'
                                        time.sleep(7)
                                        break
                            else:
                                print 'error! device is already running, please stop the device and try again.'
                                time.sleep(7)
                                break

                except Exception as err:
                    #print err
                    #.print_exc()
                    print 'error! invalid command'
                    time.sleep(7)

            elif 'stop' in ir:
                try:
                    abc = ir.split(' ')
                    dn = abc[1]
                    for dv in self.Slaves.keys():
                        if not dv == dn:continue
                        else:
                            try:
                                xx = ''
                                for dvc in self.devices.keys():
                                    if dv == self.devices[dvc]['dname']:
                                        xx = dvc
                                _stop(self.Slaves[dv]['process'])    #.kill()
                                self.Slaves[dv]['process'].kill()
                                self.Slaves = removekey(self.Slaves,dv)
                                with open(os.path.abspath(os.curdir+'/'+xx+'/pid.txt')) as pds:
                                    
                                    suid = int(pds.read())
                                    
                                    os.kill(suid, signal.SIGTERM) #or signal.SIGKILL
                                
                                print 'successfully stopped device: '+ dv
                                time.sleep(7)
                                break
                            except Exception as ec:
                                print ec
                                print 'error! cannot stop the device: try to reboot the computer.'
                                time.sleep(7)
                                break
                except:
                    print 'error! invalid command'
                    time.sleep(7)

            elif 'status' == ir:
                continue
            
            elif ('arguments' in ir) and not ('add' in ir) and not ('remove' in ir):
                try:
                    dn = ir.split('.')[0]
                    for dv in self.devices.keys():
                        
                        if self.devices[dv]['dname'] == dn:
                            try:

                                prefix = os.curdir+'/'+dv+'/args.txt'
                                with open(os.path.abspath(prefix),mode='r') as a:
                                    for l in a.readlines():
                                        if 'tar' not in l:
                                            if l != '':
                                                if l != '\n':
                                                    print l.replace('\n','')
                                time.sleep(12)
                                break
                        
                            except:
                                print 'are you sure that the device is installed?'
                                time.sleep(7)
                                break

                except:
                    print 'error! invalid command'
                    time.sleep(7)

            elif 'arguments.add' in ir:
                try:
                    acx = ir.split(' ')
                    dn = acx[0].split('.')[0]
                    arg = acx[1]
                    for dv in self.devices.keys():
                        
                        if self.devices[dv]['dname'] == dn:
                            prefix = os.curdir+'/'+dv+'/args.txt'
                            with open(os.path.abspath(prefix),mode='a') as a:
                                a.write(arg+'\n')
                except:
                    print 'error! invalid command'
                    time.sleep(7)
                        
            elif 'arguments.remove' in ir:
                try:
                    acx = ir.split(' ')
                    dn = acx[0].split('.')[0]
                    arg = acx[1]
                    for dv in self.devices.keys():
            
                        if self.devices[dv]['dname'] == dn:
                            prefix = os.curdir+'/'+dv+'/args.txt'
                            na = []
                            with open(os.path.abspath(prefix),mode='r') as a:
                                for l in a.readlines():
                                    if not arg in l:
                                        na.append(l)
                            with open(os.path.abspath(prefix),mode='w') as a:
                                a.write('')
                            with open(os.path.abspath(prefix),mode='w') as a:
                                for l in na:
                                    a.write(l)
                            
                except:
                    print 'error! invalid command'
                    time.sleep(7)

            elif 'show log' == ir:
                try:
                    prefix = os.path.abspath(os.curdir).split('/Desktop')[0]+'/Desktop/automation/dict/log.txt'
                    with open(os.path.abspath(prefix),mode='r') as log:
                            for l in log.readlines():
                              print l
                    time.sleep(30)
                except:
                    print 'error cannot locate log file.'
                    time.sleep(7)

            elif 'erase log' == ir:
                try:
                    prefix = os.path.abspath(os.curdir).split('/Desktop')[0]+'/Desktop/automation/dict/log.txt'
                    with open(os.path.abspath(prefix),mode='w') as log:
                        log.write('')
                except:
                    print 'error cannot locate log file.'
                    time.sleep(7)

            elif 'reinstall' in ir:
                try:
                    dn = ir.split(' ')[1]
                    re = self.u.runcommandAndGetOutPut('idevice_id -l').split('\n')
                    for dvc in self.devices.keys():
                        if not self.devices[dvc]['name'] == dn:continue
                            #               print dvc
                            #print self.devices[dvc]['udid'] in re
                        tmp = []
                        for i in self.Threads[int(dvc)-1]:
                            try:
                                i.kill()
                                tmp.append(i)
                            except Exception as e:
                                pass
                        for t in tmp:
                            try:
                                self.Thread[int(dvc)-1].remove(i)
                            except:pass
                        try:
                            self.installDevice(dvc,int(dvc)-1)
                            print 'the device: '+ self.devices[dvc]['dname'] + ' ' + self.devices[dvc]['osv'] + ' was reinstalled.'
                            time.sleep(7)
                        except:
                            print 'cound not reinstall device.'
                            time.sleep(7)
                            pass
                except:
                        print 'error! invalid command'
                        time.sleep(7)

            elif ir == 'refrash devices':
                
                re = self.u.runcommandAndGetOutPut('instruments -s devices')
                o = re.split('\n')
                y = 1
                
                
                        
                for j in o:
                    if not ('(' in j) or ('Simulator' in j) or (len(j.split(' '))!=3):
                        pass
                    else:
                        try:
                            lst = j.split(' ')
                            dname = lst[0]
                            osver = lst[1].replace('(','').replace(')','')
                            udid = lst[2].replace('[','').replace(']','')
                            
                            udids = []
                        
                            for k in self.devices.keys():
                                udids.append(self.devices[k]['udid'])
                                    
                            if udid in udids:
                                y += 1
                                continue
                                
                        
                        
                            self.devices[str(y)] = {}
                            self.devices[str(y)]['dname'] = dname
                            self.devices[str(y)]['osv'] = osver
                            self.devices[str(y)]['udid'] = udid
                            self.Threads.append([])
                            y += 1
                            
                        except Exception as err:
                            pass
                        
            elif ir == 'exit':
                exit(0)
            else:
                print 'invalid command'
                time.sleep(7)
                continue
                    
                              
                              
                              
        return 1
                               
    def installDevice(self,dv,counter):
        
        def removekey(d, key):
            r = dict(d)
            del r[key]
            return r
        
        
        #dv = str(counter + 1)
        if 'lock' in self.devices[dv].keys():
            print 'Error: the device ' + self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv'] + ' is not connected properly'
            print 'please reboot the device, dissconnect from the computer, reconnect and try again.'
            print 'please make sure that the device is connected to the same wifi network as the computer\nand that the computer is trusted by the device'
            print 'if you did the above already, then please issue a reload command:'
            print '>reload '+self.devices[dv]['dname']
            print 'and try again.'
            return 1
                
                
        if not self.u.checkdir(self.root+'/Desktop/wda'):
            print 'could not locate the "wda" directory at the desktop'
            print 'please follow the instructions at setup.pdf'
            exit(-1)
        if not self.u.checkdir(self.root+'/Desktop/automation'):
            print 'could not locate the "automation" directory at the desktop'
            print 'please follow the instructions at setup.pdf'
            exit(-1)
        self.u.createdir(dv)
        self.u.runcommand('cp -r '+self.root+'/Desktop/wda '+self.wd+'/'+dv)
        #self.u.runcommand('cp '+self.root+'/Desktop/master/slave.py '+self.wd+'/'+dv)
        self.u.runcommand('cp '+self.root+'/Desktop/master/dslave.py '+self.wd+'/'+dv)
        self.u.runcommand('cp '+self.root+'/Desktop/master/iwdp.py '+self.wd+'/'+dv)
        self.u.runcommand('cp '+self.root+'/Desktop/master/ap.py '+self.wd+'/'+dv)
        self.u.runcommand('cp '+self.root+'/Desktop/master/r.py '+self.wd+'/'+dv)
        
        cmdline1 = self.devices[dv]['udid']
        time.sleep(4)
            
        p = self.u.runcommandReturnP(os.path.abspath(os.curdir+'/'+dv),'python dslave.py '+cmdline1+' '+self.wd+'/'+dv+'/wda')
        self.Threads[counter].append(p)
        url = ''
        stop = False
        senity_check = 0
            
        while not stop:
            time.sleep(10)
            senity_check += 1
            if senity_check == 7:
                print 'Error: the device ' + self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv'] + ' is not connected properly'
                print 'please reboot the device, dissconnect from the computer, reconnect and try again.'
                print 'please make sure that the device is connected to the same wifi network as the computer\nand that the computer is trusted by the device'
                print 'if you did the above already, then please issue a reload command:'
                print '>reload '+self.devices[dv]['dname']
                print 'and try again.'
                self.devices[dv]['lock'] = True
                return 1
            with open(os.path.abspath(os.curdir+'/'+dv+'/wda/yy.txt'), mode='r') as data:
                for stdout_line in data.readlines():
                    if 'ServerURLHere->' in stdout_line:
                        url = stdout_line.split('ServerURLHere->')[1].split('<-ServerURLHere')[0]
                        #print url
                        self.devices[dv]['wdurl'] = url
                        self.devices[dv]['counter'] = counter
                        stop = True
                        break
        
        p1 = self.u.runcommandReturnP(os.path.abspath(os.curdir+'/'+dv),'python iwdp.py '+self.devices[dv]['udid']+' '+str(counter))
        self.Threads[counter].append(p1)
        if self.gip in self.devices[dv]['wdurl']:
            p2 = self.u.runcommandReturnP(os.path.abspath(os.curdir+'/'+dv),'python ap.py '+self.devices[dv]['udid']+' '+str(counter))
            self.Threads[counter].append(p2)
            with open(os.path.abspath(os.curdir+'/'+dv+'/args.txt'),mode='w') as arguments:
                arguments.write('-udid='+self.devices[dv]['udid']+'\n')
                arguments.write('-wdurl='+self.devices[dv]['wdurl']+'\n')
                osv = '0'
                arguments.write('-osv='+osv+'\n')
                arguments.write('-dname='+self.devices[dv]['dname']+'\n')
                arguments.write('-apurl=http://'+gip+':'+str(4723+counter)+'\n')
                arguments.write('-port=27753\n')
                arguments.write('-tar=&&&&&&&&&&&&&&&&\n')
                arguments.write('-mode=2\n')
                if self.nord == 0:
                    arguments.write('-changeip=false\n')
                return 0
                

        else:
            print 'Error: the device '+ self.devices[dv]['dname'] + ' ' + self.devices[dv]['osv'] +' is not connected to the same network as the computer.'
            print 'the computer internal ip is: '+gip
            print 'the device internal ip is: '+self.devices[dv]['wdurl'].replace('http://','').split(':')[0]
            print 'please connect the device to the same wifi network and issue the following commands:'
            print '>reload '+self.devices[dv]['dname']
            print '>install '+self.devices[dv]['dname']
            self.devices[dv] = removekey(self.devices[dv],'wdurl')
            for pd in self.Threads[counter]:
                try:
                    pd.kill()
                except:
                    pass
            self.Threads[counter] = []
            time.sleep(12)
            return -1



c = Commander()
c.run()


exit(0)

