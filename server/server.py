import argparse
from multiprocessing import Process
import sys
from time import sleep
import yaml
import socket
import numpy as np
import threading


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

def messagesTreatment(message, address, server, clients, condition):
    
    condition.acquire()
    
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
    
    sleep(15)
    clients.remove(address)
    
    condition.notify()
    condition.release()
    
    server.sendto(bytesToSend, address)

def listen_partner(partners, address):
    
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        # Bind to address and ip
        server.bind(address)
        print("TCP server up and listening")
    except NameError:
        return print(f'\nNão foi possível iniciar o servidor! Error -> {NameError}\n')

    while True:
        server.listen()
        print()
        print(partners)

        conn, addr = server.accept()
        
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        print(data)
        if not data:
            break
        
        data = int(data.decode())
        partners.append((addr, data, conn))

def send_message_to_partner(server, partners, bufferSize, bytesAddressPair):
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    print(f"\npartners: {partners[0][2]}\n")
    
    partners[0][2].sendto(message, partners[0][0])
    response = server.recvfrom(bufferSize)
    server.sendto(response, address)

def main():
    
    args = define_and_get_arguments()

    print(f"N = {args.n_max}")
    
    localIP = args.hostname
    localPort = args.port
    bufferSize = args.bufferSize

    # Create a datagram socket
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    try:
        # Bind to address and ip
        server.bind((localIP, localPort))
        print("UDP server up and listening")
    except NameError:
        return print(f'\nNão foi possível iniciar o servidor! Error -> {NameError}\n')
    
    clients = []
    partners = []

    thread = threading.Thread(target=listen_partner, args=[partners, (localIP, localPort)])
    thread.start()

    # Listen for incoming datagrams
    while(True):
        
        bytesAddressPair = server.recvfrom(bufferSize)
        
        if len(clients) >= args.n_max:
            proc = Process(target=send_message_to_partner, args=(server, partners, bufferSize, bytesAddressPair))
            proc.start()
            continue

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        clients.append(address)
        
        condition = threading.Condition()
        thread = threading.Thread(target=messagesTreatment, args=[message, address, server, clients, condition])
        thread.start()

if __name__ == "__main__":
    main()