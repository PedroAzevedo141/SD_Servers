import argparse
import socket


def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run the client."
    )
    parser.add_argument("--n_max", type=int,
                        default="10", help="Maximum value to serve requests at the same time. (INT)")
    parser.add_argument("--port", type=int, default=20001,
                        help="host's port Ex. 8080, 3001, 8553, etc")
    parser.add_argument("--hostname", type=str, default="127.0.0.1",
                        help="hostname or ip. Ex. 'localhost', '127.0.0.1', etc")

    args = parser.parse_args(args=args)

    return args

def get_int():
    userdata = input("\n Enter the number of arrays, or 'q' to quit:")
    if userdata == 'q':
        return None
    try:
        user_num = int(userdata)
        if user_num > 1:
            return user_num
        else:
            print("I need a number greater than 1 to continue.")
            return(get_int())
    except ValueError:
        print("I need an integer to continue.")
        return(get_int())

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
    
    num_matrix = get_int()
    
    if num_matrix != None:
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
