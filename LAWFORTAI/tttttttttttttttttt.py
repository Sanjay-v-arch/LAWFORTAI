import socket
try:
    ip = socket.gethostbyname("api.generativeai.google")
    print("Resolved IP:", ip)
except Exception as e:
    print("Error:", e)
