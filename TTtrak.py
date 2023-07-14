import RPi.GPIO as GPIO
import time
import requests
from datetime import datetime
import mysql.connector
import socket

# Nastavitev načina pinov (uporabljamo oznake BCM)
GPIO.setmode(GPIO.BCM)

# Nastavitev pinov
button_pin = 4
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Parametri za debouncing
debounce_time = 0.05  # 50 ms
last_state = GPIO.HIGH
last_time = time.time()



# URL za pošiljanje podatkov


udp_host = "172.100.100.235"
udp_port = 5002
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Glavna zanka programa
try:
    while True:
        # Preveri stanje pina
        button_state = GPIO.input(button_pin)

        # Preveri, ali je prišlo do spremembe stanja
        if button_state != last_state:
            current_time = time.time()
            # Preveri, ali je minilo dovolj časa od prejšnjega preklopa
            if current_time - last_time >= debounce_time:
                last_state = button_state
                last_time = current_time

                # Preveri, ali je gumb pritisnjen (nizka vrednost pina)
                if button_state == GPIO.LOW:
                    # Gumb je bil pritisnjen, pridobi trenuten čas
                    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    print("Pritisnjen gumb ob:", current_time_str)
                    
                    #UDP
                    
                    message = current_time_str.encode()
                    udp_socket.sendto(message,(udp_host,udp_port))
                    

                    # Pošiljanje časa preko Ethernet kabla
                    print("Podatki poslani preko Ethernet kabla.")

        # Počakaj malo, da se ne izvaja preverjanje stanja prevečkrat v sekundi
        time.sleep(0.01)

except KeyboardInterrupt:
    # Ob prekinitvi programa s tipko Ctrl+C počistimo GPIO nastavitve in zapremo povezavo z bazo
    GPIO.cleanup()
    udp_socket.close()
