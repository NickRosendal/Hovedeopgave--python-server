
import socket
import threading

class CommandServer(threading.Thread):
    def __init__(self,adress="", port=5001, maxClients=1):
        threading.Thread.__init__(self)
        self.adress = adress
        self.port = port
    
    def serveFile(self, file):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((self.adress, self.port))
        self.mySocket.listen(1)
        f = open(file, "rb")
        data = f.read()
        f.close()
        self.myConnection, maddr = self.mySocket.accept()
        
        self.mySocket.close()
        self.myConnection.send(data)
        self.myConnection.close()
        print "done"
if __name__ == '__main__':
    myCommandServer = CommandServer()
    myCommandServer.serveFile("testImage.jpeg")