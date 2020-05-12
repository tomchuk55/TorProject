import socket, threading
mainIp = '10.70.235.114'
HOST = '0.0.0.0'
PORT = 5000


def main():
    s = socket.socket()
    s.connect((mainIp, PORT))
    s.send("I am a server".encode())
    key = s.recv(3)
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        try:
            s, addr = server.accept()
            data = s.recv().decode()
            threading.Thread(target=nodeHandler, args=(s, data, key)).start()
        except:
            continue

if __name__ == '__main__':
    main()

