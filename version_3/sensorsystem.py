import socket
import msvcrt
import pandas as pd
import csv
import time

# IP-Adresse des Host-Computers und Port des FBG-Interrogators
UDP_IP = "" # IP-Adresse des Host-Computers
UDP_PORT = 8889 # Remote-Port des FBG-Interrogators

# IP-Adresse und Port des FBG-Interrogators
UDP_Interrogator_IP = "192.168.0.10" # IP-Adresse des FBG-Interrogators
UDP_Interrogator_PORT = 8888 # Lokaler Port des FBG-Interrogators

# Nachrichten, um den Auto-Modus ein- und auszuschalten, sowie die Sensoren zu kalibrieren
MESSAGE_AUTO_ON = b"auto,1>"
MESSAGE_AUTO_OFF = b"auto,0>"
MESSAGE_ZERO_DIR = b"zeroDIR>"
MESSAGE_ZERO_WL = b"zeroWL>"

# Socket für den Versand und Empfang von Daten über UDP
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# UDP-Stream einschalten, indem eine Nachricht an den FBG-Interrogator gesendet wird
sender_sock.sendto(MESSAGE_AUTO_ON, (UDP_Interrogator_IP, UDP_Interrogator_PORT))
print('abc')

# Den Empfangs-Socket an die angegebene IP-Adresse und Port binden
receiver_sock.bind((UDP_IP, UDP_PORT))

# Initialisierung eines Zählers für die Anzahl der empfangenen Zeilen
line_count = 0

# Initialisierung einer Variable, um die zusammengefügten Daten zu speichern
concatenated_data = ""

# Eine Textdatei öffnen, um die Daten mit Zeitstempel zu speichern
with open("udp_data_timestamp.txt", "w") as file:
    while True:
        # Daten empfangen (Puffergröße beträgt 1024 Bytes)
        data, addr = receiver_sock.recvfrom(1024)

        # Daten in ein String-Format konvertieren
        data = "%s" % data

        # Den Zeilenzähler erhöhen
        line_count += 1

        # Die empfangenen Daten mit den vorherigen Daten zusammenfügen
        concatenated_data += ',' + data  
        print(concatenated_data)

        # Wenn der Zeilenzähler 4 erreicht, die zusammengefügten Daten und den Zeitstempel in die Textdatei schreiben
        if line_count == 4:
            # Den aktuellen Zeitstempel abrufen
            timestamp = time.time()

            # Die zusammengefügten Daten und den Zeitstempel in die Textdatei schreiben
            file.write(f"{timestamp} {concatenated_data}\n")

            # Den Zeilenzähler und die zusammengefügten Daten zurücksetzen
            line_count = 0
            concatenated_data = ""

        # Überprüfen, ob eine Taste auf der Tastatur gedrückt wurde
        if msvcrt.kbhit():
            key = msvcrt.getch()

            # Wenn 's' gedrückt wurde, die Sensoren auf Null setzen (gerader Sensor)
            if key == b's':
                print("gerader Sensor")
                sender_sock.sendto(MESSAGE_ZERO_WL, (UDP_Interrogator_IP, UDP_Interrogator_PORT))

            # Wenn 'd' gedrückt wurde, die Sensorenrichtung auf Null setzen (gewickelter Sensor)
            if key == b'd':
                print("Sensorenrichtung auf Null setzen")
                sender_sock.sendto(MESSAGE_ZERO_DIR, (UDP_Interrogator_IP, UDP_Interrogator_PORT))

            # Wenn 'e' gedrückt wurde, den UDP-Stream ausschalten
            if key == b'e':
                print("UDP-Übertragung ausgeschaltet")
                sender_sock.sendto(MESSAGE_AUTO_OFF, (UDP_Interrogator_IP, UDP_Interrogator_PORT))
