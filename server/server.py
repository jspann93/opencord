import socketserver
import time 

class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"Client address: {self.client_address}")
        print(f"Request: {self.request}")
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self.data}")
        self.request.sendall(self.data.upper())
        while True: 
            print(f"Socket: {server.socket._closed}")
            # self.data = self.request.recv(1024).strip()
            self.data = self.request.recv(1024)
            if not self.data:
                print("Client Disconnected")
                break
            # print(f"Stripped data: {self.data.strip()}")
            message = self.data.strip()
            message = message.decode('utf-8')
            new_message = "Server says: " + message.upper() + '\n'
            new_message = bytes(new_message, 'utf-8')
         
            print(f"{self.client_address[0]} wrote: {message}")
            self.request.sendall(new_message)
        



if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 9090
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        print("Server Started")
        # print(f"Data: {server.fileno()}")
        server.serve_forever()
    