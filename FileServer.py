import select
import socket
import threading
import sys
class FileServer(threading.Thread):
    def __init__(self,adress="", port=5001):
        threading.Thread.__init__(self)
        self.adress = adress
        self.port = port
        #self.file = None
        self.fileQue = []
        self.shouldRun = True
        self.stayOpen = True
        self.start()
        
    def serveFile(self, inFile):
        
        self.stayOpen = True
        self.fileQue.append(inFile)
        
    def closeConnection(self):
        self.stayOpen = False
    def stop(self):
        self.stayOpen = False
        self.shouldRun = False
        
    def run(self): # SEMI TESTED
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((self.adress, self.port))
        self.mySocket.listen(1)
        
        while self.shouldRun:   
            while self.stayOpen:
                if len(self.fileQue) > 0:
                    self.notify("status", "Ready to serve file:" + "filePath")
                    readable, writable, exceptional = select.select([self.mySocket], [], [], 3)
                    for s in readable:
                        if s is self.mySocket:
                            self.myConnection, address = self.mySocket.accept()
                            #print "Connection from", address
                            filePath =  self.fileQue.pop()
                            rawFile = open(filePath, "rb")
                            data = filePath + "#"
                            data += rawFile.read()
                            rawFile.close()
                            self.myConnection.send(data)
                            self.myConnection.close()
                            self.notify("status", "File sent:" + filePath)
                #print "I am open and waiting"
            #print "I closed"
            self.fileQue = []
            
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
   # mysrt = "Ready to serve file:/home/xxx/Eclipse Workspace/PyBarEntrySystemServer/testImage.jpeg"
   # print mysrt[20:]
    myCommandServer = FileServer()
    myCommandServer.serveFile("/home/xxx/Eclipse Workspace/PyBarEntrySystemServer/testImage.jpeg")
