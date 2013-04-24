
import socket
import threading

class FileServer(threading.Thread):
    def __init__(self,adress="", port=5001, maxClients=1):
        threading.Thread.__init__(self)
        self.adress = adress
        self.port = port
        self.file = None
        self.stayOpen = True
        self.start()
        
    def serveFile(self, file):
        self.file = file
        
    def run(self):
        while self.stayOpen:
            if self.file != None:
                self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.mySocket.bind((self.adress, self.port))
                self.mySocket.listen(1)
                f = open(self.file, "rb")
                data = f.read()
                f.close()
                self.notify("status", "Ready to serve file:" +self.file)
                self.myConnection, maddr = self.mySocket.accept()
                
                self.mySocket.close()
                self.myConnection.send(data)
                self.myConnection.close()
                self.notify("status", "File sent:" + self.file)
                self.file = None
            
            
    observers = []
    SUBJECT_NAME = "FileServer"
    def registerObserver(self, observer):
        self.observers.append(observer)
    def unRegisterObserver(self, observer): 
        if observer in self.observers:
            self.observers.remove(observer)
    def notify(self, eventType, event):
        for eachObserver in self.observers:
            eachObserver.notify(self.SUBJECT_NAME, eventType, event)

        
        
if __name__ == '__main__':
    myCommandServer = FileServer()
    myCommandServer.serveFile("testImage.jpeg")
