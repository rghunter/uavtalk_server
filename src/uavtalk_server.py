import socket
import time

# Globals

UDP_IP = "192.168.4.22"
UDP_PORT = 5005

def main():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(UDP_IP,UDP_PORT)
    
    while(1):
        
        
    
if __name__ == "__main__":
    main()