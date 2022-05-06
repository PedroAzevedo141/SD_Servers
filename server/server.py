import yaml
import socket
import numpy as np

clients = []

def matrix(dictMatrix):
    orderedNames = list(dictMatrix.keys())
    dataMatrix = np.array([dictMatrix[i] for i in orderedNames])
    print(dataMatrix)

def main():
    localIP = "127.0.0.1"
    localPort = 20001
    bufferSize = 1024

    # Create a datagram socket
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    try:
        # Bind to address and ip
        server.bind((localIP, localPort))
        print("UDP server up and listening")
    except:
        return print('\nNão foi possível iniciar o servidor!\n')
    

    # Listen for incoming datagrams
    while(True):

        bytesAddressPair = server.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)
        
        dictConfig_matrix = dict()
        dictConfig_matrix.update(yaml.safe_load(message.decode()))
        
        matrix(dictConfig_matrix)
        
        msgFromServer = "Hello UDP Client"
        bytesToSend = str.encode(msgFromServer)
        
        server.sendto(bytesToSend, address)

if __name__ == "__main__":
    main()
