import socket, threading, urllib.request
mainIp = '10.70.235.114'
HOST = '0.0.0.0'
PORT = 5000


def portFinder(ip):
    global PORT
    n = socket.socket()
    PORT += 1
    if PORT == 10000:
        PORT = 5000
    try:
        n.connect((ip, PORT))
        return n
    except:
        portFinder(ip)


def tEncode(data, key):
    return chr(ord(data)+key)


def tDecode(data, key):
    return chr(ord(data)-key)


def nodeHandler(s, data, key):
    global PORT
    message = tDecode(data, key)
    i = message.find(';')
    if i == -1:
        ip = message
        fp = urllib.request.urlopen(ip)
        message = fp.read().decode("utf8")
        fp.close()
    else:
        ip = message[:i]
        message = message[i+1:]
        n = portFinder(ip)
        n.send(message.encode())
        message = n.recv().decode()
        message = tEncode(message, key)
    print(message)
    s.send(message.encode())



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
            c, addr = server.accept()
            s.recv(0).decode()
            data = s.recv(9).decode()
            if data == "confirmed":
                data = c.recv().decode()
                threading.Thread(target=nodeHandler, args=(s, data, key)).start()
        except:
            continue
            

if __name__ == '__main__':
    main()

