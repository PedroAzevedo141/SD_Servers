from time import sleep
import yaml
import socket
import numpy as np
import threading

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

    # list_aux = list()
    # for x in message:        
    #     dictConfig_matrix = dict()
    #     dictConfig_matrix.update(yaml.safe_load(x))
    #     list_aux.append(dictConfig_matrix)
    
    # msgFromServer = multMatrix_client(list_aux)
    # bytesToSend = str.encode(msgFromServer)
    
    # sleep(15)
    
    # client.sendto(bytesToSend)

def server_partner():
    
    localIP = "127.0.0.1"
    localPort = 20001
    bufferSize = 1024
    
    n_max = 2

    # Create a datagram socket
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        # Bind to address and ip
        client.connect((localIP, localPort))
        print("TCP server up and listening")
    except:
        return print('\nNão foi possível iniciar o servidor!\n')
    

    # Listen for incoming datagrams

    client.send((str(n_max)).encode("utf-8"))
    
    while True:
        message = client.recv(1024)
        
        if message.decode() == "":
            continue
        
        condition = threading.Condition()
        thread = threading.Thread(target=messagesTreatment, args=[message, client])
        thread.start()

        
if __name__ == "__main__":
    server_partner()