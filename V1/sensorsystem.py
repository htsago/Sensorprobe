import socket
import msvcrt
import pandas as pd
import csv
import time
 
UDP_IP = "" #IP-Addess of the Host Computer
UDP_PORT = 8889 #Remote-Port of the FBG Interrogator
 
UDP_Interrogator_IP = "192.168.0.10" #IP-Addess of the FBG Interrogator
UDP_Interrogator_PORT = 8888 #Local-Port of the FBG Interrogator
 
MESSAGE_AUTO_ON = b"auto,1>"
MESSAGE_AUTO_OFF = b"auto,0>"
MESSAGE_ZERO_DIR = b"zeroDIR>"
MESSAGE_ZERO_WL = b"zeroWL>"
 
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
sender_sock.sendto(MESSAGE_AUTO_ON, (UDP_Interrogator_IP, UDP_Interrogator_PORT)) #switch UDP stream on
print('abc')
receiver_sock.bind((UDP_IP, UDP_PORT))

# Initialize a counter for the number of lines received
line_count = 0

# Initialize a variable to store the concatenated data
concatenated_data = ""

with open("udp_data_timestamp.txt", "w") as file:
    while True:
        # data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data, addr = receiver_sock.recvfrom(1024) #receive the data from UDP
        data = "%s" % data
        # Increment the line count
        line_count += 1

        # Concatenate the data with the previous data
        concatenated_data += ',' + data  
        print(concatenated_data)

        # If the line count is 4, write the concatenated data and timestamp to the text file
        if line_count == 4:
            # Get the current timestamp
            timestamp = time.time()

            # Write the concatenated data and timestamp to the text file
            file.write(f"{timestamp} {concatenated_data}\n")

            # Reset the line count and concatenated data
            line_count = 0
            concatenated_data = ""

        # if msvcrt.kbhit(): #read keyboard input
        #     key = msvcrt.getch()
        #     if key == b's': #Zero edge sensors (straight sensor)
        #         print("straight sensor")
        #         sender_sock.sendto(MESSAGE_ZERO_WL, (UDP_Interrogator_IP, UDP_Interrogator_PORT))
        #     if key == b'd': #Zero edge sensors direction (coiled sensor)
        #         print("zero direction")
        #         sender_sock.sendto(MESSAGE_ZERO_DIR, (UDP_Interrogator_IP, UDP_Interrogator_PORT))
        #     if key == b'e': #switch UDP stream off
        #         print("UDP transfer off")
        #         sender_sock.sendto(MESSAGE_AUTO_OFF, (UDP_Interrogator_IP, UDP_Interrogator_PORT))
