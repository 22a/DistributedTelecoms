from socket import *
from thread import *
 
# Defining server address and port
host = 'localhost'
port = 5050
 
#Creating socket object
sock = socket()
#Binding socket to a address. bind() takes tuple of host and port.
sock.bind((host, port))
#Listening at the address
sock.listen(5) #5 denotes the number of clients can queue
 
def clientthread(conn):
#infinite loop so that function do not terminate and thread do not end.
     while True:
#Sending message to connected client
         conn.send('Hi! I am server\n') #send only takes string
#Receiving from client
         data = conn.recv(1024) # 1024 stands for bytes of data to be received
         print data
 
while True:
#Accepting incoming connections
    conn, addr = sock.accept()
#Creating new thread. Calling clientthread function for this function and passing conn as argument.
    start_new_thread(clientthread,(conn,)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
 
conn.close()
sock.close()