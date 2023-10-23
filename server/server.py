import socketserver
import threading 
from datetime import datetime
import json 
import Crypto.Hash # Used to generate keys and for encryption and decryption
import secrets
import string
import oc_database
import re
from tabulate import tabulate
import time

# Versioning 
# Major.Minor.Revision (bug fixes, small updates).build number


# Known bugs: 't or anything with ' will break the input and the server. 

# Encryption: 
"""
    - Client generates an asymmetric keypair. 
    - Client sends public key with initial authentication request to server 
    - Server uses the key to encrypt the response and sends back the response to the client
    - If the client is authenticated the server generates a symmetric key and includes that key in the response to the client.  

    * Both the clients asymmetric key and servers symmetric key are "randomly" generated for each connection. 


    
"""
class Client:
    def __init__(self, client_version, profile_hash): # Profile hash can be anything until I develop a hashing method  
        self.client_version = client_version # The client version 
        self.phash = profile_hash # Just going to be a name or something 
        self.connected = datetime.now()
        self.messages = {}
        self.token = None # Need to implement a token 
        self.client_key = None # Clients public key 
        self.private_key = None # The servers private key (or key for this session)
        self.symmetric_key = None # Once encryption is established the server generates a symmetric key
        self.data = None
        self.id = None
        self.last_message = None

    
    def readMessage(self, message):
        message = json.loads(message)
        t = message.pop('token')
        n = message.pop('n')
         
        self.messages[n] = message
        client = Client("0.0.0.1", self.data)
        return message['content']
    
    



class Server:
    def __init__(self):
        self.connections = []
        self.active_connections = []
        self.server_version = "0.0.0.1"
        self.server_hash = None # Need to implement unique server hashes (easy way for server identification)
        self.verification_hash = None # Need to implement unique verification hashes for the server 
        self.database = oc_database.Database()
    
    
    # Authorize access to the server 
    def authorize(self, user):
        message = {} # holds the auth message
        message["version"] = self.server_version
        message["token"]  = None # Need to implement a token system or session system 

        return message 
 

    def saveMessages(self, sent, user):
        if user in self.messages.keys():
            self.messages[user] = {**self.messages[user], **sent}
        
        else: 
            self.messages[user] = sent
    
    def loadMessages(self, user):
        if user not in self.messages.keys():
            return 1

        long_string = ">>>  " # Combine all messages into 1 long string (for now )
        user_messages = self.messages[user]
        for message in user_messages.keys():
            long_string += user_messages[message]['content'] + "\n" + ">>>  "
        
        return long_string
    
    
     
    
                
    
opencord_server = Server()
        
def update(timeout=2):
    time.sleep(timeout)
    # message = bytes("Testing update", 'utf-8')
    while True: 
        # print(f"active connections: {len(opencord_server.active_connections)}")
        for i in opencord_server.active_connections:
            for client, connection in i.items():
                master_string = ""
                # print(f"Client: {client.phash}")
                # print(f"Connection: {connection}")
                room = opencord_server.database.query(f"SELECT room FROM user WHERE name = '{client.phash}'")
                room = room.fetchone()[0]
                if room != None:
                    # print(f"Room: {room}")
                    messages = opencord_server.database.query(f"SELECT * FROM message WHERE room_id = {room} ORDER BY id DESC LIMIT 10")
                    messages = messages.fetchall()
                    # print(f"Last message: {messages[0][0]}")
                    if client.last_message == None:
                        try:
                            client.last_message = messages[0][0]
                        except Exception as e:
                            # Error with index being out of range for messages[0][0] meaning no messages in the room. 
                            client.last_message = None
                        for m in messages: 
                            try:
                                name = opencord_server.database.query(f"SELECT name FROM user WHERE id = {m[5]}")
                                name = name.fetchone()[0]
                                # print(f"message_id: {m[0]}")

                                # print(f"Name: {name}")
                                        
                                # print(f"Message: {m[2]}")
                                master_string = f"{name}: {m[2]}\n" + master_string
                                # print(master_string)
                            except Exception as e:
                                print(f"Last message Error: {e}")
                                print(f"Last meassage: {client.last_message}\n Room: {room}")
                        message = bytes(master_string, 'utf-8')
                        connection.sendall(message)
                    elif client.last_message < messages[0][0]:
                        for x in range(0, messages[0][0] - client.last_message):
                            # print(f"index: {x}")
                            message_text = messages[x][2]
                            # print(f"Message id: {message_id}")
                            try:
                                name = opencord_server.database.query(f"SELECT name FROM user WHERE id = {messages[x][5]}")
                                name = name.fetchone()[0]
                                master_string = f"{name}: {message_text}\n" + master_string

                                client.last_message = messages[0][0] 
                            except Exception as e:
                                print(f"Update Error: {e}")
                                print(f"Last meassage: {client.last_message}\n Room: {room}")
                        message = bytes(master_string, 'utf-8')
                        connection.sendall(message)

        time.sleep(timeout)


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
            print(f"Message: {message}")
            message = message.decode('utf-8')
            new_message = "Server says: " + message.upper() + '\n'
            new_message = bytes(new_message, 'utf-8')
         
            print(f"{self.client_address[0]} wrote: {message}")
            self.request.sendall(new_message)
        

class ThreadedTCPHandler(socketserver.BaseRequestHandler):

    # Parse the message
    def parseMessage(self, message):
        parsed_message = string.split('')
        return 
 
    def handle(self): 
        self.data = self.request.recv(1024).strip()
        message = self.data.strip()
        message = self.data.decode('utf-8')
        msg_object = json.loads(message)
        print(f"{self.client_address[0]} wrote: {self.data}")
        
        client = Client("0.0.0.1", msg_object['profile'])
        opencord_server.connections.append(client) # Add client to the list of current connections
        # query = "SELECT 1 FROM user where name = " + msg_object['profile']
        # check_user = opencord_server.database.query(query) # Check if user exists in the database



        



        # IF the user is not in the database add them into the database
        if(opencord_server.database.checkUser(msg_object['profile'])[0] == 0): 
            opencord_server.database.insertUser(msg_object['profile']) # Add user to the database
            welcome = f"""
                Welcome {client.phash}!
                Join a room using the /join roomname (replacing roomname with the room you want to join) command.
                For more commands enter /help or /? to view the full list of commands.
            """
            new_message = bytes(welcome, 'utf-8') 
            self.request.sendall(new_message)
        else:
            try:
                user_id = opencord_server.database.query(f"SELECT id FROM user WHERE name = '{client.phash}'") 
                user_id = user_id.fetchone()[0]
                client.id = user_id

                room_id = opencord_server.database.query(f"SELECT room FROM user WHERE id = {client.id}")
                room_id = room_id.fetchone()[0]
                room_name = opencord_server.database.query(f"SELECT name from room where id = {room_id}")
                room_name = room_name.fetchone()[0]

                welcome = f"""
                You have joined {room_name}
                """ + "\n"
            except Exception as e:
                print(f"Welcome Error: {e}")
                welcome = f"""
                    Welcome {client.phash}!
                    Join a room using the /join roomname (replacing roomname with the room you want to join) command.
                    For more commands enter /help or /? to view the full list of commands.
                    """

            new_message = bytes(welcome, 'utf-8') 
            self.request.sendall(new_message)
            

        print(f"Client address: {self.client_address}")
        print(f"Request: {self.request}")

        
        object_identifier = {client:self.request}
        opencord_server.active_connections.append(object_identifier)
        # self.data = self.request.recv(1024).strip()
        cur_thread = threading.current_thread()
        print(f"Thread: {cur_thread}")
        # print(f"{self.client_address[0]} wrote: {self.data}")
        # self.request.sendall(self.data.upper())
        # loaded_messages = opencord_server.loadMessages(client.phash)
        # if loaded_messages != 1:
        #     self.request.sendall(bytes(loaded_messages, 'utf-8'))
            
        while True: 
            try:
                # print(f"Socket: {server.socket._closed}")
                # self.data = self.request.recv(1024).strip()
                self.data = self.request.recv(1024)
                if not self.data:
                    print("Client Disconnected")
                    # opencord_server.saveMessages(client.messages, client.phash)
                    break
                
                # print(f"Stripped data: {self.data.strip()}")
                message = self.data.strip()
                message = message.decode('utf-8')
                # print(f"Message: {message}")
                m = client.readMessage(message)
                # x = re.search('^\S+', m)
                # x = re.search("^\?>", m)
                # print(f"X: {x}")
                if re.search("^\/", m):
                    
                    # Parse the command it will remove the ?> and the spaces until it hits the actual command
                    parsed_command = re.sub(r'^\/', '', m)
                    parsed_command = re.sub(r"^\s+", '', parsed_command)
                    parsed_command = re.split("\s", parsed_command)
                    
                    print(f"parsed command: {parsed_command}")

                    # Python switch statement 
                    new_message = None
                    match parsed_command[0]:
                        case "users":
                            table = []
                            current_connections = opencord_server.connections # This will list current connections to the server
                            # new_message = "Server says: " + m.upper() + '\n'
                            # new_message = bytes(m, 'utf-8')
                            headers = ["Connected Users"]
                            
                            connected_clients = ""
                            for u in current_connections:
                                print(f"u.phash: {u.phash}") 
                                table.append([u.phash])
                                # connected_clients += u.phash + "\n"
                            
                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"                        
                            new_message = bytes(pretty_format, 'utf-8') 
                            self.request.sendall(new_message)
                        
                        case "rooms":
                            result = opencord_server.database.query("SELECT name FROM room")
                            result = result.fetchall()
                            table = []
                            headers = ["Rooms"]
                            for room in result:
                                table.append([room[0]])
                                
                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"                        
                            # print(f"Result from query: {result}")
                            new_message = bytes(pretty_format, 'utf-8') 
                            self.request.sendall(new_message)
                        
                        case "join":
                            print("Implement the ability to join rooms")
                            room_id = opencord_server.database.query(f"SELECT id FROM room WHERE name = '{parsed_command[1]}'")
                            room_id = room_id.fetchone()[0]
                            # print(f"Room ID: {room_id}")
                            
                            opencord_server.database.query(f"UPDATE user SET room = {room_id} WHERE name = '{client.phash}'")
                            client.last_message = None
                            
                            new_message = bytes(f"You have joined {parsed_command[1]}\n", 'utf-8') 
                            self.request.sendall(new_message)
                        
                        case "createroom":
                            opencord_server.database.query(f"INSERT INTO room (name) VALUES ('{parsed_command[1]}')")
                            new_message = bytes(f"Room {parsed_command[1]} created.\n", 'utf-8') 
                            self.request.sendall(new_message)
                            
                        case "help":
                            headers = ["Command", "Description"]
                            table = [
                                ["/users", "List the servers users."], 
                                ["/rooms", "List the rooms in the server."], 
                                ["/join RoomName", "Join a room in the server (no spaces allowed in room name for now)."], 
                                ["/createroom RoomName", "Create a new room in the server (no spaces allowed in room name for now)."], 
                                ["/help or /?", "Lists the commands available in the server."],
                                ["/exit", "Exit the server (terminates the connection with the server)."]
                            ]

                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"                        
                            new_message = bytes(pretty_format, 'utf-8') 
                            self.request.sendall(new_message)
                        case "?":
                            headers = ["Command", "Description"]
                            table = [
                                ["/users", "List the currently connected users."], 
                                ["/rooms", "List the rooms in the server."], 
                                ["/join RoomName", "Join a room in the server (no spaces allowed in room name for now)."], 
                                ["/createroom RoomName", "Create a new room in the server (no spaces allowed in room name for now)."], 
                                ["/help or /?", "Lists the commands available in the server."],
                                ["/exit", "Exit the server (terminates the connection with the server)."]
                            ]
                              
                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"                        
                            new_message = bytes(pretty_format, 'utf-8') 
                            self.request.sendall(new_message)

                        case _: 
                            # new_message = "Server says: " + m.upper() + '\n'
                            new_message = "Default case \n"
                            new_message = bytes(new_message, 'utf-8')
                            self.request.sendall(new_message)
         
                            # print(f"{self.client_address[0]}: {message}")
                else:
                    new_message = f"{client.phash}: {m}"
                    room = opencord_server.database.query(f"SELECT room FROM user WHERE id = '{client.id}'")
                    room = room.fetchone()[0]
                    
                    if room != None:
                        opencord_server.database.query(f"INSERT INTO message (text, room_id, user_id) VALUES ('{m}', {room}, {client.id})")
                                        
                    # new_message = bytes(m, 'utf-8')
                    # self.request.sendall(new_message)

            except Exception as e:
                print(f"Error: {e}")
                opencord_server.active_connections.remove(object_identifier)
                # opencord_server.saveMessages(client.messages, client.phash)
                break
                
                
                
                
                


# The class should already be defined but we can override functions inside the class
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    print("Called threadedTCPServer")
    pass


if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 9090

    # Non threaded server 
    # with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
    #     print("Server Started")
    #     # print(f"Data: {server.fileno()}")
    #     server.serve_forever()


    # Most of this code is from the docs with edits made to it 
    # https://docs.python.org/3/library/socketserver.html
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)
 
    with server:
        ip, port = server.server_address
        
        # Start a thread with the server -- that thread will then start
        # one more thread for each request 
        server_thread = threading.Thread(target=server.serve_forever)  # This is the serving thread

        # Exit the server thread when the main thread terminates 

        # update_thread = threading.Thread(target=server

        # The entire Python program exits when only daemon threads are left.
        # So they are abruptly stopped at shutdown meaning resources may not be released properly. 
        # For threads to stop gracefully, they should be non-daemonic and use a signalling mechanism
        # such as an Event.
        server_thread.daemon = True 
        
        server_thread.start()

        
        # If we want the server to control the updating we use this 
        update_thread = threading.Thread(target=update, daemon=True)  # This is the update Thread
        update_thread.start()
        
        print(f"Server loop running in thread {server_thread.name}")
        print(f"Server running on port {PORT}")
        while True: 
            try:
                t = input("\"Exit\" to stop the server: ")
                if t == "exit":
                    break
        
                print("Shutting Down")
                server.shutdown()
            except Exception as e:
                print(f"Error Here: {e}")
                break
        
        server.shutdown() 
            

    