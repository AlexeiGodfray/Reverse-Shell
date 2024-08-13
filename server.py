import socket 
import sys

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
        print("Sockt creation error: " + str(msg))

#Bind socket to port and wait for onnection from client 
def socket_bind():
    try:
        global host 
        global port 
        global s 
        print("Binding socket to port: " + str(port))
        s.bind((host,port))
        #allows server to accecpt coonection (5 tries before refeusing)
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
            conn, setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established " + address[0])
        except:
            print("Error accpeting connections")

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