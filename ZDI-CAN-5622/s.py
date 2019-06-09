
import socket

print('stealing heap data on localhost:50007')
HOST = ''                 
PORT = 50007           
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while 1:
    try:
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        data = conn.recv(1024)
        print(data)
        print('\n\n')
        print('..\n\n')
    except:pass
conn.close()
