import socket 
import sys
from datetime import datetime 
import json 
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import threading
import time
import os
import re
import pyaudio 
import wave
from audio import AudioFile # custom function 



if __name__ == "__main__":
    # print(audio_stream.readframes(1024))

    HOST, PORT = "localhost", 9090
    # data = " ".join(sys.argv[1:])


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = None
    received = None
    i = 0 
    
    packet_object = {
        # "c": False, # Critical data/message
        "n": None, # Packet Number
        "d": None,   # Packet Data      
    }

    while data != "/exit":
        data = input(">>> ")
        if data == "/audio":
            a = AudioFile("sample.wav")
            p = a.getObject()
            reader = a.getReader()
            audio_stream = a.getStream()
            print(f"Format: {p.get_format_from_width(audio_stream.getsampwidth())}")
            print(f"Channel Count: {audio_stream.getnchannels()}")
            print(f"Rate: {audio_stream.getframerate()}")
            audio_data = audio_stream.readframes(1024)
            # a.play()
            # a = AudioFile("sample.wav")
            # audio_stream = a.getStream()
            # audio_data = audio_stream.readframes(1024)
            # time.sleep(3)
            # print(audio_data)

            # audio_data = audio_stream.readframes(1024)
            while audio_data != b'':
                received = None
                counter = 0
                sock.sendto(audio_data, (HOST, PORT))
                # reader.write(audio_data)
                received = str(sock.recv(1024), "utf-8").strip()
                while received != "Recieved":
                    # print(f"Error not received: {received}")
                    time.sleep(1)
                    counter += 1
                    if counter == 5:
                        sock.sendto(audio_data, (HOST, PORT)) # Resend the data
                        counter = 0
                # print("Received")
                audio_data = audio_stream.readframes(1024)

            # sock.sendto(buffer, (HOST, PORT))
        
        else:
            # SOCK_DGRAM is the socket type to user for UDP sockets 
    
            # No connec() call; UDP has no connections. 
            # Data is directly sent to the recipient via sendto(). 
            sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
            received = str(sock.recv(1024), "utf-8")

        print(f"Sent: {data}")
        print(f"Received: {received}")