#!/usr/bin/env python

from platform import system

from PyQt5.QtWidgets import (QApplication, QGridLayout, QPushButton, QDialogButtonBox, QLabel, QLineEdit,
        QTabWidget, QVBoxLayout, QHBoxLayout, QStyleFactory, QAction, QMainWindow, QMessageBox, QWidget)
from PyQt5.QtGui import  QFont, QDoubleValidator
from PyQt5.QtCore import  Qt, QSize

import math

def myfloat(txt):
    try:
        x = float(txt)
    except:
        x = 0
    return x

class CalcWindow(QMainWindow):
    def __init__(self):
        super(CalcWindow, self).__init__()
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        QApplication.setPalette(QApplication.style().standardPalette())

        ssfont = QFont("")
        ssfont.setStyleHint(QFont.SansSerif)
        ssfont.setStyleStrategy(QFont.PreferOutline)
        ssfont.setFamily("Arial")
        if system() == "Darwin":
            ssfont.setPointSize(16)
        else:
            ssfont.setPointSize(12)
        self.setFont(ssfont)
        self.setAcceptDrops(False)

        self.tabWidget = QTabWidget()
        self.makeTitreTab()
        self.makeVNTTab()

        self.tabWidget.addTab(self.titreTab, "Titre Calc")
        self.tabWidget.addTab(self.VNTTab, "VNT Calc")

#        buttonBox = QDialogButtonBox()
#        quitButton = buttonBox.addButton("Quit",QDialogButtonBox.DestructiveRole)
        quitButton =QPushButton("Quit")
        quitButton.setAutoDefault(False)
        quitButton.setDefault(False)
        quitButton.clicked.connect(self.close)

#        calcButton = buttonBox.addButton("Calculate",QDialogButtonBox.ActionRole)
        calcButton = QPushButton("Calculate")
        calcButton.setDefault(True)

#        calcButton.setAutoDefault(True)
        calcButton.clicked.connect(self.Calc)

        buttonBox=QHBoxLayout()
        buttonBox.addWidget(calcButton)
        buttonBox.addWidget(quitButton)

#        buttonBox.setCenterButtons(True)

        mainview=QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addLayout(buttonBox)
        mainview.setLayout(mainLayout)
        self.setCentralWidget(mainview)

        self.setWindowTitle("Titre Calculations")

        self.createActions()
        self.createMenus()

    def about(self):
        ab = QMessageBox(self)
        ab.setTextFormat(Qt.RichText)
        ab.setText("<p style='font-size: 18pt'>About TitreUtil</p>"
                   "<p style='font-size: 14pt; font-weight: normal'> <b>TitreUtil</b> is a simple tool to calculate "
                   "virus titres (TCID50) or virus neutralising titres (also known as "
                   "serum neutralising titres) using the method of Spearman & Kärber </p>")
        ab.exec()

    def createActions(self):
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",triggered=self.close)
        self.aboutAct = QAction("&About", self, triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutAct)

    def Calc(self):
        frontTab = self.tabWidget.currentIndex()
        if frontTab == 0:
            grid = self.titreTab.findChild(QGridLayout)
            plate_dil = myfloat(grid.itemAtPosition(0,1).widget().text())
            if plate_dil == 0:
                plate_dil = 10
            logdil = math.log10(plate_dil)

            virusPerWell = myfloat(grid.itemAtPosition(1,1).widget().text())
            if virusPerWell <= 0:
                virusPerWell = 50
            logvirus = math.log10(1000/virusPerWell)

            baseline = myfloat(grid.itemAtPosition(2,1).widget().text())
            if baseline <= 0:
                baseline = 1
            logbase = math.log10(1/baseline)

            sumP = myfloat(grid.itemAtPosition(3,1).widget().text())
            if sumP < 1:
                sumP = 1
            titre = 0.01*float(int(0.5+100*(logvirus + (-1*(logbase-(logdil * (sumP - 0.5)))))))
            ans = '%.2f' % titre
        else:
            grid = self.VNTTab.findChild(QGridLayout)
            plate_dil = myfloat(grid.itemAtPosition(0, 1).widget().text())
            if plate_dil == 0:
                plate_dil = 2
            logdil = math.log10(plate_dil)

            baseline = myfloat(grid.itemAtPosition(2, 1).widget().text())
            if baseline <= 0:
                baseline = 5
            logbase = math.log10(1 / baseline)

            sumP = myfloat(grid.itemAtPosition(3, 1).widget().text())
            if sumP < 1:
                sumP = 1
            titre =  (-1 * (logbase - (logdil * (sumP - 0.5))))
            ans = '%.0f' % 10**titre

        grid.itemAtPosition(5, 1).widget().setText(ans)


    def exit(self):
        print("Quit button clicked")


    def makeTitreTab(self):
        self.titreTab = QWidget()
        TCLayout = QGridLayout()
        dilLabel = QLabel("Plate Dilution Factor =")
        dilLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        dilBox = myLineEdit("10")
        dilBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(dilLabel, 0, 0)
        TCLayout.addWidget(dilBox, 0, 1)
        virLabel = QLabel("Microlitres of virus per well =")
        virLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        virBox = myLineEdit("50")
        virBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(virLabel, 1, 0)
        TCLayout.addWidget(virBox, 1, 1)
        baseLabel = QLabel("Baseline dilution =")
        baseLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        baseBox = myLineEdit()
        baseBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(baseLabel, 2, 0)
        TCLayout.addWidget(baseBox, 2, 1)
        sumpLabel = QLabel("Sum of proportions =")
        sumpLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        sumpBox = myLineEdit("1")
        sumpBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(sumpLabel, 3, 0)
        TCLayout.addWidget(sumpBox, 3, 1)
        TCLayout.setRowMinimumHeight(4,10)
        ansLabel = QLabel("Log titre (TCID50/ml) =")
        ansLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        ansBox = myLineEdit()
        ansBox.setReadOnly(True)
        ansBox.setFocusPolicy(Qt.NoFocus)
        ansBox.setFrame(False)
        TCLayout.addWidget(ansLabel, 5, 0)
        TCLayout.addWidget(ansBox, 5, 1)
        self.titreTab.setLayout(TCLayout)


    def makeVNTTab(self):
        self.VNTTab = QWidget()
        TCLayout = QGridLayout()
        dilLabel = QLabel("Plate Dilution Factor =")
        dilLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        dilBox = myLineEdit("2")
        dilBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(dilLabel, 0, 0)
        TCLayout.addWidget(dilBox, 0, 1)
#        virLabel = QLabel("Microlitres of virus per well =")
#        virLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#        virBox = myLineEdit("1000")
#        virBox.returnPressed.connect(self.Calc)
#        TCLayout.addWidget(virLabel, 1, 0)
#        TCLayout.addWidget(virBox, 1, 1)
        baseLabel = QLabel("Baseline dilution =")
        baseLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        baseBox = myLineEdit("5")
        baseBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(baseLabel, 2, 0)
        TCLayout.addWidget(baseBox, 2, 1)
        sumpLabel = QLabel("Sum of proportions =")
        sumpLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sumpBox = myLineEdit("1")
        sumpBox.returnPressed.connect(self.Calc)
        TCLayout.addWidget(sumpLabel, 3, 0)
        TCLayout.addWidget(sumpBox, 3, 1)
        TCLayout.setRowMinimumHeight(4, 10)
        ansLabel = QLabel("Neutralising antibody titre = 1/")
        ansLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ansBox = myLineEdit()
        ansBox.setReadOnly(True)
        ansBox.setFocusPolicy(Qt.NoFocus)
        ansBox.setFrame(False)
        TCLayout.addWidget(ansLabel, 5, 0)
        TCLayout.addWidget(ansBox, 5, 1)
        self.VNTTab.setLayout(TCLayout)


class myLineEdit(QLineEdit):
    def __init__(self, defaultText=""):
        super(myLineEdit, self).__init__()
        self.setMaximumSize(QSize(80, 22))
        self.setText(defaultText)
        x = QDoubleValidator()
        x.setNotation(QDoubleValidator.StandardNotation)
        self.setValidator(x)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    mainWin = CalcWindow()
    mainWin.show()
    sys.exit(app.exec_())