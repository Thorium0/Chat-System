from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet
import sys, socket, select
from threading import Thread
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Port = 2478


class ChatInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.font = QtGui.QFont("Arial", 12)
        self.setFont(self.font)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)

        # connectWidgetsLayout
        self.connectWidgetsLayout = QHBoxLayout(self)
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter Username")
        self.ip = QLineEdit(self)
        self.ip.setPlaceholderText("Enter IP-Address")
        self.connect = QPushButton(self)
        self.connect.clicked.connect(self.connectToServer)
        self.connect.setText("Connect")
        self.ip.returnPressed.connect(self.connect.click)
        self.connectWidgetsLayout.addWidget(self.username)
        self.connectWidgetsLayout.addWidget(self.ip)
        self.connectWidgetsLayout.addWidget(self.connect)

        # chatLayout
        self.chatLayout = QVBoxLayout(self)
        self.chat = QTextEdit(self)
        self.chat.setReadOnly(True)
        self.chatLayout.addWidget(self.chat)

        # chatWidgetsLayout
        self.chatWidgetsLayout = QHBoxLayout(self)
        self.message = QLineEdit(self)
        self.send = QPushButton(self)
        self.send.setText("Send")
        self.send.clicked.connect(self.sendMessage)
        self.message.returnPressed.connect(self.send.click)
        self.chatWidgetsLayout.addWidget(self.message)
        self.chatWidgetsLayout.addWidget(self.send)

        # add to main layout
        self.mainLayout.addLayout(self.connectWidgetsLayout)
        self.mainLayout.addLayout(self.chatLayout)
        self.mainLayout.addLayout(self.chatWidgetsLayout)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.mainLayout)


    def handleConnection(self):
        while True:
            pass
            message = server.recv(2048)
            if message:
                self.chat.insertPlainText(message.decode("utf-8"))
            sleep(1)
        server.close()


    @QtCore.Slot()
    def connectToServer(self):
        IP_address = self.ip.text()
        if IP_address:
            try:
                server.connect((IP_address, Port))
            except OSError as ex:
                if ex.errno == 106: # Already connected error code
                    self.chat.append("\n<You are already connected to this server>")
                else:
                    self.chat.append("\n<Unable to connect to server>")
            else:
                Thread(target=self.handleConnection).start()
        else:
            self.chat.append("\n<Please type an ip-address before trying to connect>")


    @QtCore.Slot()
    def sendMessage(self):
        username = self.username.text().strip()
        if not username:
            self.chat.append("\n<Please type a username before trying to send a message>")
        else:
            message = self.message.text().replace(";","").strip()
            messageforServer = username + ";" + message
            if message and messageforServer:
                try:
                    server.send(messageforServer.encode("utf-8"))
                except:
                    self.chat.append("\n<Please connect before trying to send a message>\n")
                else:
                    self.chat.append("[{}]: {}".format(self.username.text(), message))
                    self.message.setText("")



if __name__ == '__main__':
    app = QApplication([ ])
    apply_stylesheet(app, theme='dark_teal.xml')
    window = ChatInterface()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
