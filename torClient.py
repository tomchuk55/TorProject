import socket, webbrowser, os
mainIp = '10.70.235.114'
PORT = 5000


def tEncode(data, key):
    return chr(ord(data)+key)


def tDecode(data, key):
    return chr(ord(data)-key)


def mConstruct(data, req):
    for x in data:
        req = tEncode(req, x[2])
        req = x[1] + ";" + req
    i = req.find(';')
    req = req[:i]
    return req


def mDeConstruct(data, ans):
    for x in data:
        ans = tDecode(ans, x[2])
    return ans


def request(req):
    s = socket.socket()
    s.connect((mainIp, PORT))
    s.send("I am a client".encode())
    data = s.recv(1024).decode().split(";")
    message = mConstruct(data, req)
    s.close()
    s.connect((data[2][1], PORT))
    s.send(message.encode())
    message = s.recv().decode()
    message = mDeConstruct(data, message)
    f = open('datafile.html', 'w')
    f.write(message)
    webbrowser.open_new_tab('datafile.html')
    f.close()
    os.remove('datafile.html')



def main():
    while True:
        req = input("insert ip")
        request(req)






if __name__ == '__main__':
    main()
