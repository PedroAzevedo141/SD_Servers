import socket

def main(msg):
    bytesToSend = str.encode(msg)
    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)
    
if __name__ == "__main__":
    
    width_matrix = int(input("\n Enter the width: "))
    height_matrix = int(input("\n Enter the height: "))

    dictConfig_matrix = dict()
    for x in range(height_matrix):
        listaux = list()
        for y in range(width_matrix):
            listaux.append(int(input("\n Insert a number: ")))
    
        dictConfig_matrix.update({str(x+1): listaux})
        print(dictConfig_matrix)
        
    main(str(dictConfig_matrix))
