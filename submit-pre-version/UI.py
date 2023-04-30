import PyQt5.QtCore
import PyQt5.QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit

import trans
# import transdemo3

def handleCalc():
    input_text_A = textEdit1.toPlainText()
    output = trans.convert_java_to_python(input_text_A)
    textEdit2.setPlainText(output)



def handleClear():
    textEdit1.clear()
    textEdit2.clear()


app = QApplication([])

window = QMainWindow()
window.resize(900, 500)
window.move(10, 10)
window.setWindowTitle('code translator')

textEdit1 = QPlainTextEdit(window)
textEdit1.setPlaceholderText("Please enter the JAVA code.")
textEdit1.move(10, 25)
textEdit1.resize(400, 400)

textEdit2 = QPlainTextEdit(window)
textEdit2.setPlaceholderText("output python code")
textEdit2.move(410, 25)
textEdit2.resize(400, 400)



button = QPushButton('START', window)
button.move(160, 440)
moudle_num_list = list()
fixed_list = list()
# when clicked,use handleCalc
button.clicked.connect(handleCalc)

button = QPushButton('RESET', window)
button.move(560, 440)
# clear
button.clicked.connect(handleClear)

window.show()

app.exec_()
