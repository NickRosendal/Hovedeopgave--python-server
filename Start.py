from CommandServer import CommandServer
from CameraStreamHttpServer import CameraCaptureServer
from MagtekUsbCardReader import MagtekUsbCardReader
import HealthInsuranceCardInterpreter
class ObserverbleTest():
    def __init__(self):
        self.myCommandServer = CommandServer()
        self.myCommandServer.registerObserver(self)
        self.myCommandServer.start()
        
        self.myMagtekUsbCardReader = MagtekUsbCardReader()
        self.myMagtekUsbCardReader.registerObserver(self)
        self.myMagtekUsbCardReader.start()
        
        self.myCameraCaptureServer = CameraCaptureServer()
        self.myCameraCaptureServer.start()
        print "All modules have been asked to start"

    def notify(self, subjectName,eventType, message):
        if eventType =="status":
            print subjectName, "status", message
        if subjectName == "CommandServer" and eventType =="message":
            self.handleTcpMessages(message)
           
        elif subjectName == "CardReader" and eventType =="swipe":
            cardString = HealthInsuranceCardInterpreter.Interpitate(message)
            self.myCommandServer.sendMessage(self.createCommandString(cardString))
       
    def handleTcpMessages(self, message):
        print "CommandServer have recived message:", message
        if message == "pending":
            self.myCommandServer.sendMessage("connection accepted")
        elif message == "start video server":
            self.myCameraCaptureServer.showVideo()
            self.myCommandServer.sendMessage("video server is ready")
        elif message == "take picture":
            self.myCameraCaptureServer.takePicture("path")
            self.myCommandServer.sendMessage("image is ready")   
        elif message == "pretendToSwipe":
            self.myCommandServer.sendMessage("guestInfo:name:SIGNE JOHANSEN# birthday:1986-12-23# zipcode:3500# sex:Female# status:welcomed# lastVisit:NA##")
            
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
    while True:
        command = raw_input('Write stop to exit\n')
        if command == "stop":
            myObserverbleTest.myCameraCaptureServer.stopCamera()
            myObserverbleTest.myCommandServer.stop()
            print "stopped"
            break;
        print command