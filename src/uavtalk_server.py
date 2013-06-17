import socket
import time
import thread

# Globals

UDP_IP = "192.168.4.22"
HARDWARE_PORT = 46274
GCS_PORT = 2020

def main():
    hardware_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hardware_side.bind((UDP_IP,HARDWARE_PORT))
    
    gcs_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gcs_side.bind(("127.0.0.1", GCS_PORT))
    
    gcs_to_hardware = []
    hardware_to_gcs = []
    hardware_addr = ("192.168.4.53", 46274)
    gcs_addr = -1
    while gcs_addr == -1:
        data, addr = gcs_side.recvfrom(1024)
        gcs_addr = addr
        gcs_to_hardware.append(data)
    
    thread.start_new(gcs_send, (gcs_side, hardware_to_gcs, gcs_addr))
    thread.start_new(gcs_receive, (gcs_side, gcs_to_hardware))
    
    thread.start_new(hardware_send, (hardware_side, gcs_to_hardware, hardware_addr))
    thread.start_new(hardware_receive, (hardware_side, hardware_to_gcs))
    
    while(1):
        time.sleep(1)
        
        
def gcs_send(socket, hardware_to_gcs, gcs_addr):
    '''This sends data to the GCS
    '''
    while 1:
        if len(hardware_to_gcs) > 0:
            for available_packet in hardware_to_gcs:
                socket.sendto(available_packet, gcs_addr)
            del hardware_to_gcs[:]
        time.sleep(0.001)

def gcs_receive(socket, gcs_to_hardware):
    '''This recieved data from the GCS
    '''
    while 1:
        gcs_to_hardware.append(socket.recv(1024))
        time.sleep(0.001)

def hardware_send(socket, gcs_to_hardware, hardware_addr):
    '''This sends to the hardware
    '''
    while 1:
        if len(gcs_to_hardware) > 0:
            for available_packet in gcs_to_hardware:
                socket.sendto(available_packet, hardware_addr)
            del gcs_to_hardware[:]
        time.sleep(0.001)

def hardware_receive(socket, hardware_to_gcs):
    while 1:
        hardware_to_gcs.append(socket.recv(1024))    
        time.sleep(0.001)
        
        

if __name__ == "__main__":
    main()