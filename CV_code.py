import cv2
import socket
from cvzone.HandTrackingModule import HandDetector

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ESP module's IP address and port
esp_ip = "192.168.251.129"  # Replace with the actual IP address of your ESP
esp_port = 1234  # Replace with   the port number you set in your ESP code

# Connect to the ESP module
client_socket.connect((esp_ip, esp_port))

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.5, maxHands=2)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    hands, frame = detector.findHands(frame)

    if not hands:
        print("No hands found")
    else:
        hands1 = hands[0]
        fingers = detector.fingersUp(hands1)
        fingers_count = fingers.count(1)
        print(fingers_count)

        # Send the number of fingers detected to the ESP as a string
        data_to_send = str(fingers_count)
        client_socket.send(data_to_send.encode())
        client_socket.send('\n'.encode())

    cv2.imshow("Controller", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Close the socket when done
client_socket.close()
cap.release()
cv2.destroyAllWindows()