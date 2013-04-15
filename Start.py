from CommandServer import CommandServer
from CameraStreamHttpServer import CameraCaptureServer
from MagtekUsbCardReader import MagtekUsbCardReader
import HealthInsuranceCardInterpreter
class ObserverbleTest():
    def __init__(self):
     #  self.myCommandServer = CommandServer()
     #   self.myCommandServer.registerObserver(self)
     #  self.myCommandServer.start()
        
     #   self.myMagtekUsbCardReader = MagtekUsbCardReader()
     #   self.myMagtekUsbCardReader.registerObserver(self)
     #   self.myMagtekUsbCardReader.start()
        
        print "we made it"
        self.myCameraCaptureServer = CameraCaptureServer()
        self.myCameraCaptureServer.start()
        

    def notify(self, subjectName, message):
        if subjectName == "CommandServer":
            self.handleTcpMessages(message)
           
        elif subjectName == "CardReader":
            if "M'%" in message:
                cardString = HealthInsuranceCardInterpreter.Interpitate(message)
                print self.createCommandString(cardString)
                self.myCommandServer.sendMessage(self.createCommandString(cardString))
        print subjectName + " says: " + message
    def handleTcpMessages(self, message):
        if message == "pending":
            self.myCommandServer.sendMessage("connection accepted")
        elif message == "start video server":
            self.myCommandServer.sendMessage("video server is ready")
        elif message == "take picture":
            
            self.myCommandServer.sendMessage("image is ready")   
        elif message == "pretendToSwipe":
            self.myCommandServer.sendMessage("guestInfo:name:SIGNE JOHANSEN# birthday:1986-12-23# zipcode:3500# sex:Female# status:welcomed# lastVisit:NA##")
        elif message == "die":
            self.myCommandServer.stop()
            
    def createCommandString(self, cardInfo):
        if cardInfo == None:
            return
        returnString  = "guestInfo:name:" + str(cardInfo[0]) + "#"
        returnString += " birthday:" + str(cardInfo[3]) + "#"
        returnString += " zipcode:" + str(cardInfo[2]) + "#"
        returnString += " sex:" + str(cardInfo[4]) + "#"
        returnString += " status:" + "welcomed#"
        returnString += " lastVisit:NA#"
        returnString += "#"
        return returnString 
if __name__ == '__main__':
    myObserverbleTest = ObserverbleTest()  # starts the class 
