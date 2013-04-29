
import socket
import threading

class FileServer(threading.Thread):
    def __init__(self,adress="", port=5001):
        threading.Thread.__init__(self)
        self.adress = adress
        self.port = port
        self.file = None
        self.fileQue = []
        self.stayOpen = True
        self.start()
        
    def serveFile(self, file):
        self.fileQue.append(file)
        
    def stop(self):
        try:
            self.mySocket.close()
            self.myConnection.close()
        except:
            pass
        
    def run(self):
        while self.stayOpen:
            if len(self.fileQue) > 0:
                self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.mySocket.bind((self.adress, self.port))
                self.mySocket.listen(1)
                filePath =  self.fileQue.pop()
                rawFile = open(filePath, "rb")
                data = filePath + "#"
                data += rawFile.read()
                rawFile.close()
                self.notify("status", "Ready to serve filePath:" + filePath)
                self.myConnection, maddr = self.mySocket.accept()
                self.mySocket.close()
                self.myConnection.send(data)
                self.myConnection.close()
                self.notify("status", "File sent:" + filePath)
            
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
