import socket
from _thread import *
from threading import Thread
import sys
import pickle
class Seed:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listening_socket.bind((self.ip,int(self.port)))
        self.PeerList = []

        self.listening_socket.listen()  
    
    def handle_peer(self,peer_socket):
        msg = peer_socket.recv(4096).decode('utf-8')
        if(msg=='register'):
            peer_socket.send("OK".encode('utf-8'))
            msg2 = peer_socket.recv(4096).decode('utf-8')
            if(msg2 == 'PeerRequest'):
                peer_socket.send(pickle.dumps(self.PeerList))
        
        else:
            raise Exception("Invalid peer message")



if __name__ == "__main__":
    seed = Seed(sys.argv[1],sys.argv[2])
    while True:
        # Accept a client connection
        peer_socket, addr = seed.listening_socket.accept()
        peer_ip,peer_port = addr[0],addr[1]
        print(f"Server {seed.ip}:{seed.port} accepted connection from peer {peer_ip}:{peer_port} ")
        with open("output.txt",'a') as f:
            f.write(f"Server {seed.ip}:{seed.port} accepted connection from peer {peer_ip}:{peer_port} "+"\n")
        seed.PeerList.append(f"{peer_ip} {peer_port}")
        start_new_thread(seed.handle_peer,(peer_socket,))



    

