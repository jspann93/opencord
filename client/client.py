import socket 
import sys



if __name__ == "__main__":
    HOST, PORT = "", 9090
    # data = " ".join(sys.argv[1:])

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: 
        # Connect to server and send data
        data = None
        sock.connect((HOST, PORT))
        while data != "exit":
            data = input("Input:  ")
            sock.sendall(bytes(data + "\n", 'utf-8'))
            received = str(sock.recv(1024), 'utf-8')
            print(received)


            # Receive data from the server and shut down 
    
    print(f"Sent: {data}")
    print(f"Received: {received}")