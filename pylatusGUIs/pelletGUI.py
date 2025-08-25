from PyQt6 import QtWidgets, QtCore, QtGui
import logging
import pathlib
import os
from functools import partial

logdir = 'pylatusGUIlog'
homedir = pathlib.Path.home()
fulllogdir = f'{homedir}/{logdir}'
#os.makedirs(fulllogdir,exist_ok=True)
logger = logging.getLogger()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        '''
        eventlogfile = f'{homedir}/{logdir}/mfcgui.log'
        logging.basicConfig(filename=eventlogfile, level = logging.INFO, format = '%(asctime)s %(levelname)-8s %(message)s',
                            datefmt = '%Y/%m/%d_%H:%M:%S')
        logger.info('mfcgui opened')
        '''
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        
        self.MainWindow.setWindowTitle('Pellet grid GUI')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout()
        self.group = QtWidgets.QGroupBox()

        self.pelletLabels = {}
        self.sampleNames = {}
        self.buttons = {}
        self.elementList = {}
        self.repLists = {}
        self.values = {}

        ncols = 8
        nrows = 5
        nsubrows = 4

        self.namesLabels = {}
        self.elementsLabels = {}
        self.repLabels = {}
        for i in range(nrows):
            self.namesLabels[i] = QtWidgets.QLabel()
            self.namesLabels[i].setObjectName(f'namesLabels{i}')
            self.namesLabels[i].setText('sample name')
            self.namesLabels[i].adjustSize()
            self.gridLayout.addWidget(self.namesLabels[i], i*nsubrows+1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

            self.elementsLabels[i] = QtWidgets.QLabel()
            self.elementsLabels[i].setObjectName(f'namesLabels{i}')
            self.elementsLabels[i].setText('element list')
            self.elementsLabels[i].adjustSize()
            self.gridLayout.addWidget(self.elementsLabels[i], i*nsubrows+2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

            self.repLabels[i] = QtWidgets.QLabel()
            self.repLabels[i].setObjectName(f'namesLabels{i}')
            self.repLabels[i].setText('repetition list')
            self.repLabels[i].adjustSize()
            self.gridLayout.addWidget(self.repLabels[i], i*nsubrows+3, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        icondirec = f'{os.path.dirname(os.path.abspath(__file__))}/icons/'
        self.greenpic = QtGui.QPixmap(f'{icondirec}/green.png')
        self.greypic = QtGui.QPixmap(f'{icondirec}/grey.png')
        
        
        for n in range(ncols):
            for i in range(nrows):
                index = n+1+i*8
                self.values[index] = False
                self.pelletLabels[index] = QtWidgets.QLabel()
                self.pelletLabels[index].setObjectName(f'pellet{index}')
                self.pelletLabels[index].setScaledContents(True)
                #self.pelletLabels[index].setText(str(index))
                self.pelletLabels[index].setPixmap(self.greypic)
                self.pelletLabels[index].setMaximumWidth(70)
                self.pelletLabels[index].setMaximumHeight(70)
                self.gridLayout.addWidget(self.pelletLabels[index], i*nsubrows,n+1,alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

                self.buttons[index] = QtWidgets.QPushButton()
                self.buttons[index].setObjectName(f'buttons{index}')
                self.buttons[index].setText(str(index))
                self.buttons[index].setMaximumWidth(60)
                self.buttons[index].setMinimumHeight(60)
                self.buttons[index].setStyleSheet('background-color:rgba(255,255,255,0)')
                #self.buttons[index].setStyleSheet('border:none')
                #self.buttons[index].setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.buttons[index].clicked.connect(partial(self.changeLabelColor, index))
                self.gridLayout.addWidget(self.buttons[index], i*nsubrows,n+1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
                
                self.sampleNames[index] = QtWidgets.QLineEdit()
                self.sampleNames[index].setObjectName(f'sampleNames{index}')
                self.gridLayout.addWidget(self.sampleNames[index], i*nsubrows+1,n+1)

                self.elementList[index] = QtWidgets.QLineEdit()
                self.elementList[index].setObjectName(f'elementList{index}')
                self.gridLayout.addWidget(self.elementList[index], i*nsubrows+2,n+1)

                self.repLists[index] = QtWidgets.QLineEdit()
                self.repLists[index].setObjectName(f'repLists{index}')
                self.gridLayout.addWidget(self.repLists[index], i*nsubrows+3,n+1)
                
        self.runButton = QtWidgets.QPushButton()
        self.runButton.setObjectName('runButton')
        self.runButton.setText('generate code')
        #self.runButton.setStyleSheet('font-size:20;')
        self.runButton.setMinimumWidth(100)
        self.runButton.setMinimumHeight(50)
        self.runButton.adjustSize()
        self.runButton.clicked.connect(self.generateCode)
        self.gridLayout.addWidget(self.runButton,nrows*nsubrows, 0)

        self.group.setLayout(self.gridLayout)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.group)
        
        self.centralwidget.setLayout(self.gridLayout)

        self.MainWindow.resize(800, 500)

        self.MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def changeLabelColor(self, index):
        value = not self.values[index]
        valuedct = {True: self.greenpic,
                    False:self.greypic}
        self.pelletLabels[index].setPixmap(valuedct[value])
        self.values[index] = value

    def generateLists(self):
        positionList = []
        sampleList = []
        elementList2 = []
        repetitionList = []
        for index in self.values:
            if not self.values[index]:
                continue
            positionList.append(index)
            sampleList.append(self.sampleNames[index].text())
            elSublist = self.elementList[index].text().replace(' ','').split(',')
            elementList2.append(elSublist)
            repSublist = [int(i) for i in self.repLists[index].text().split(',')]
            if len(repSublist) == 1:
                repSublist = repSublist[0]
            elif not repSublist:
                repSublist = 3
            elif len(repSublist) != len(elSublist):
                #print('mismatch in repetition and element lists')
                raise ValueError('mismatch in repetition and element lists')
            repetitionList.append(repSublist)
        return positionList,sampleList,elementList2, repetitionList
    
    def generateCode(self):
        try:
            positionList,sampleList, elementList2, repetitionList = self.generateLists()
        except ValueError as e:
            print(e)
            return
        string = f'\npositionList = {positionList}\n'
        string += f'sampleList = {sampleList}\n'
        string += f'elementList = {elementList2}\n'
        string += f'repList = {repetitionList}\n'
        string += (f'ef.pelletGrid(pos1y, pos1z, sampleList = sampleList, subdir = "pellets", positionList = positionList,\n'
                   f'elementList = elementList, repList = repList, stage = , zmotorName = , autoGains = True, bigGrid = True, skip = 0)')
        print(string)


    
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()