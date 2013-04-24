import socket

ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ms.connect(("127.0.0.1", 5002))
f = open("output201.jepg","wb")
while 1:
    data = ms.recv(1024)
    if not data: break
    f.write(data)
f.close()
ms.close()

'''
Created on Apr 24, 2013
import sys, socket

ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ms.connect(("127.0.0.1", 5001))

f = open("testImage.jpeg", "rb")
data = f.read()
f.close()

ms.send(data)
ms.close()
if __name__ == '__main__':
    pass
@author: xxx


msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msock.bind(('', 5001))
msock.listen(1)
f = open("output.jepg","wb")
mconn, maddr = msock.accept()
while 1:
    data = mconn.recv(1024)
    if not data: break
    f.write(data)
f.close()
'''