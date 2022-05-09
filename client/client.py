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
    
    print("\nResult: ")
    print(msgFromServer[0].decode())
    
if __name__ == "__main__":
    
    num_matrix = int(input("\n Enter the number of arrays: "))
    size_matrix = int(input("\n Enter the size of your square matrix: "))

    string_aux = ""
    for z in range(num_matrix):
        dictConfig_matrix = dict()
        print(f"\nCreating the {z + 1} matrix!")
        for x in range(size_matrix):
            listaux = list()
            for y in range(size_matrix):
                listaux.append(int(input("\n Insert a number: ")))
        
            dictConfig_matrix.update({str(x+1): listaux})
            print(dictConfig_matrix)
        print(f"\nFinishing the {z + 1} matrix!")
        string_aux += str(dictConfig_matrix) + " || "
        
    main(string_aux)
