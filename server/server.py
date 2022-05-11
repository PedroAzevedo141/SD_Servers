import argparse
import sys
import yaml
import socket
import numpy as np
import threading

clients = []

ARGS = None


def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run the server."
    )
    parser.add_argument("--n_max", type=int,
                        default="10", help="Maximum value to serve requests at the same time. (INT)")
    parser.add_argument("--port", type=int, default=20001,
                        help="host's port Ex. 8080, 3001, 8553, etc")
    parser.add_argument("--hostname", type=str, default="127.0.0.1",
                        help="hostname or ip. Ex. 'localhost', '127.0.0.1', etc")

    args = parser.parse_args(args=args)

    return args

def multMatrix_client(listMatrix):

    """
    listMatrix -> Lista de dicionarios, que contem as informacoes das matrizes enviadas pelo cliente.
    dataMatrix -> Lista com todas as matrizes enviadas pelo cliente, matrizes numpy.
    """
    
    dataMatrix = list()
    for dictMatrix in listMatrix:
        dataMatrix.append(np.array([dictMatrix[i] for i in list(dictMatrix.keys())]))
    

    result_mult = np.matmul(dataMatrix[0], dataMatrix[1])
    if len(dataMatrix) > 2:
        dataMatrix.pop(0)
        dataMatrix.pop(0)
        for oneMatrix in dataMatrix:
            result_mult = np.matmul(result_mult, oneMatrix)
            
    return np.array2string(result_mult)

def messagesTreatment(message, address, server):
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)
    
    message = ((message.decode()).split(" || "))[:-1]

    list_aux = list()
    for x in message:        
        dictConfig_matrix = dict()
        dictConfig_matrix.update(yaml.safe_load(x))
        list_aux.append(dictConfig_matrix)
    
    msgFromServer = multMatrix_client(list_aux)
    bytesToSend = str.encode(msgFromServer)
    
    server.sendto(bytesToSend, address)


def main():
    
    args = define_and_get_arguments()

    print(f"N = {args.n_max}")
    
    localIP = args.hostname
    localPort = args.port
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
        
        thread = threading.Thread(target=messagesTreatment, args=[message, address, server])
        thread.start()

if __name__ == "__main__":
    main()