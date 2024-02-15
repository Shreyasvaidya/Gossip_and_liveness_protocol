import socket
import random

import pickle
import sys
class Peer:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listening_socket.bind((ip,int(port)))
        self.peers = []



    def register(self):
        seeds_list = [details.split() for details in open('config.txt',"r").readlines()]
        n = len(seeds_list)
        seeds_to_connect = random.sample(seeds_list,n//2+1)
        seed_sockets = []
        for ip,port in seeds_to_connect:
            register_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            register_socket.connect((ip,int(port)))
            register_socket.send("register".encode('utf-8'))
            
            if(register_socket.recv(4096).decode('utf-8')!='OK'):
                raise Exception(f"Didnt get response from seed with ip {ip} and port {port}")
            
            register_socket.send("PeerRequest".encode('utf-8'))
            server_peer_list = pickle.loads(register_socket.recv(4096))
            print(f"Peer node {self.ip}:{self.port} connected to server {ip}:{port} and received Peers list ",server_peer_list)
            with open("output.txt",'a') as f:
                f.write(f"Peer node {self.ip}:{self.port} connected to server {ip}:{port} and received Peers list "+ repr(server_peer_list)+"\n")

            self.peers.extend([i for i in server_peer_list if i not in self.peers]) #Union of received peer lists
            seed_sockets.append(register_socket) #list of connected seed sockets
            
            
if __name__ == "__main__":
    ip,port = sys.argv[1],sys.argv[2]
    peer = Peer(ip,port)
    peer.register()
    while True:
        peer.listening_socket.listen()


        



        