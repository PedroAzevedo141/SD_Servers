import sys
import yaml
import socket
import argparse
import threading
import numpy as np
from time import sleep

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
    parser.add_argument("--bufferSize", type=int, default=1024,
                        help="bufferSize message. Ex. '1024', '2048', etc")

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

def messagesTreatment(message, client):
    
    print(message)
    message = ((message.decode()).split(" || "))[:-1]

    list_aux = list()
    for x in message:        
        dictConfig_matrix = dict()
        dictConfig_matrix.update(yaml.safe_load(x))
        list_aux.append(dictConfig_matrix)
    
    msgFromServer = multMatrix_client(list_aux)
    bytesToSend = str.encode(msgFromServer)
    
    sleep(15)
    
    client.sendto(bytesToSend)

def server_partner():
    
    args = define_and_get_arguments()
    
    localIP = args.hostname
    localPort = args.port
    bufferSize = args.bufferSize
    
    n_max = args.n_max

    # Create a datagram socket
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        # Bind to address and ip
        client.connect((localIP, localPort))
        print("TCP server up and listening")
    except NameError:
        return print(f'\nNão foi possível iniciar o servidor TCP! Error -> {NameError}\n')
    

    # Listen for incoming datagrams

    client.send((str(n_max)).encode("utf-8"))
    
    while True:
        message = client.recv(bufferSize)
        
        if message.decode() == "":
            continue
        
        thread = threading.Thread(target=messagesTreatment, args=[message, client])
        thread.start()

        
if __name__ == "__main__":
    server_partner()