from PyQt5.QtWidgets import QComboBox, QFileDialog, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLayout, QMessageBox, QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget,QDesktopWidget
from src.logic import Logic
from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from functools import partial
import os
from PyQt5.QtGui import QFont, QIcon
from src.edit_field import EditField
class Ui_Form(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.setObjectName("self")
        self.resize(944, 654)
        
        self.setWindowIcon(QIcon('icon.ico'))
        self.setStyleSheet("QWidget{background-color: rgb(65, 65, 65);}\nQTabWidget::tab-bar {\n"
                           "     background-color: #fff;\n"
                           "}\n"
                           " QTabBar::tab {\n"
                           "    background-color:#323232;\n"
                           "    border-color: rgb(50, 50, 50);\n"
                           "    font: bold 12px \'Reboto\';\n"
                           "    color: white;\n"
                           "    height:40px;\n"
                           "    width:170px;\n"
                           "\n"
                           " } \n"
                           "QTabBar::tab:!selected {\n"
                           "    background-color:rgb(50, 50, 50);\n"
                           "    color: white;\n"
                           " }\n"
                           "\n"
                           "QTabBar::tab:hover {\n"
                           "    background-color: rgb(60, 60, 60);\n"
                           "    color: white;\n"
                           " }\n"
                           "\n"
                           "\n"
                           " QTabWidget::pane { \n"
                           "     position: absolute;\n"
                           " }\n"
                           "\n"
                           "QTabBar::tab:selected {\n"
                           "    background-color:rgb(35, 35, 35);\n"
                           "    color: white;\n"
                           "}\n"
                           "QTabBar::close-button {\n"
                           "     image: url(icons/close.png)\n"
                           " }")

        styleBtn = """QPushButton{\n
                               border:1px solid #323232;\n
                               background-color:#323232;\n
                               font: bold 12px \'Reboto\';\n
                               color: white;\n
                               height:40px;\n
                               width:170px;\n
                           \n
                            } \n
                           QPushButton:hover {\n
                                border:1px solid rgb(60, 60, 60);\n
                               background-color: rgb(60, 60, 60);\n
                               color: white;\n
                            }\n
                            QPushButton:pressed {\n
                                border:1px solid rgb(35, 35, 35);\n
                               background-color:rgb(35, 35, 35);\n
                               color: white;\n
                            }\n
                            """
        self.path = self.GetDir()
        self.project = '/'.join(self.path.split("\\")[:-1])
        self.project = self.project + "/" + self.project.split('/')[-1]
        self.logic = Logic(self.path)
        self.logic.initState()
        self.logic.settingApp()
        self.Models = []
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.Add = QPushButton(self)
        self.Add.setObjectName("Add")
        self.Add.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.Add, 0, 0, 1, 1)
        self.Save = QPushButton(self)
        self.Save.setObjectName("Save")
        self.Save.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.Save, 3, 1, 1, 1)
        self.run = QPushButton(self)
        self.run.setObjectName("run")
        self.run.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.run, 3, 0, 1, 1)
        self.Edit = QPushButton(self)
        self.Edit.setObjectName("Edit")
        self.Edit.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.Edit, 0, 1, 1, 1)
        self.Apply = QPushButton(self)
        self.Apply.setObjectName("Apply")
        self.Apply.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.Apply, 3, 2, 1, 1)
        self.Delete = QPushButton(self)
        self.Delete.setObjectName("Delete")
        self.Delete.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.Delete, 0, 2, 1, 1)
        self.AddF = QPushButton(self)
        self.AddF.setObjectName("AddF")
        self.AddF.setStyleSheet(styleBtn)
        self.gridLayout.addWidget(self.AddF, 1, 1, 1, 1)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 3)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.AddF.clicked.connect(self.showField)
        self.Add.clicked.connect(self.showModel)
        self.Delete.clicked.connect(self.delModel)
        self.Apply.clicked.connect(self.logic.migrate)
        self.view = QWebEngineView(self)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        print(" Screen size : "  + str(sizeObject.height()) + "x"  + str(sizeObject.width()))  
        #self.view.setGeometry(QRect(240,150,sizeObject.width(),sizeObject.height()))
        #self.gridLayout.addWidget(self.view, 2, 1, 1, 3)
        self.view.setGeometry(QRect(240,150,sizeObject.width()*0.85,sizeObject.height()*0.65))
        self.run.clicked.connect(partial(self.logic.RunServer,self.view))
        self.Edit.clicked.connect(self.EditModel)
        self.Save.clicked.connect(self.logic.make)
        self.tabs = 0
        self.initState()
        
        
    def initState(self):
        self.Edit.setEnabled(False)
        self.Delete.setEnabled(False)
        self.AddF.setEnabled(False)
        itms = self.logic.getModels()
        index = 0
        for i in itms.keys():
            self.addModel(i)
            item = self.Models[self.tabWidget.currentIndex()]
            for u in itms[i]:
                self.addField(u)
            index += 1

    def delModel(self):
        self.logic.delItem(self.tabWidget.currentWidget().objectName())
        self.tabWidget.removeTab(self.tabWidget.currentIndex())
        self.tabs -= 1
        if self.tabs == 0:
            self.Delete.setEnabled(False)
            self.AddF.setEnabled(False)
            self.Edit.setEnabled(False)
        

    def showModel(self):
        text, ok = QInputDialog.getText(self, 'New Model', 'Enter Model name:')
        if ok:
            self.addModel(str(text))
            self.logic.newModel(text)

    def EditModel(self):
        text, ok = QInputDialog.getText(self, 'Rename Model', 'Enter new name:',text=self.tabWidget.currentWidget().objectName())
        if ok:
            self.logic.renameAll(self.tabWidget.currentWidget().objectName(),str((text)))
            self.tabWidget.setTabText(self.tabWidget.currentIndex(),str(text))

    def showField(self):
        text, ok = QInputDialog.getText(self, 'New Field', 'Enter Field name:')
        if ok:
            self.addField([str(text).replace(" ","_"), ""])
            self.logic.addField(self.tabWidget.currentWidget().objectName(), {
                                str(text).replace(" ","_"): 'models.CharField(max_length=50,default="hjhj")'})

    def addModel(self, name):
        self.tab_2 = QWidget(self)
        self.tab_2.setObjectName(name)
        self.tabWidget.addTab(self.tab_2, name)
        self.layoutWidget = QWidget(self.tab_2)
        #self.layoutWidget.setGeometry(QRect(25, 0, 911, 511))
        self.scrollarea = QScrollArea(self.tab_2)
        self.scrollarea.setFixedWidth(230)
        self.scrollarea.setFixedHeight(540)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.layoutWidget)
        self.gridLayout_4 = QGridLayout(self.layoutWidget)
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.gridLayout_4.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(3)
        self.gridLayout_4.setVerticalSpacing(3)
        self.Models.append({'item': self.gridLayout_4, 'col': 0, 'row': 0,'ccol':1})
        self.tabWidget.setCurrentWidget(self.tab_2)
        self.tabs += 1
        self.Delete.setEnabled(True)
        self.Edit.setEnabled(True)
        self.AddF.setEnabled(True)

        return self.tab_2

    def closeEvent(self, event):
        close = QMessageBox(self)
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            self.logic.killRun()
            event.accept()
        else:
            event.ignore()
    def GetDir(self):
        options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
        fileName = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        if fileName:
            if os.sep == '\\':
                fileName = fileName.replace('/', '\\')

            return fileName

        else:
            exit()

    def addField(self, name):
        item = self.Models[self.tabWidget.currentIndex()]
        fld = Field(name[0], self.Models, self.tabWidget, name[1], self.path)
        item['item'].addWidget(fld)
        
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("self", "API Maker by <CHAHBOUN Mohammed>"))
        self.Add.setText(_translate("self", "New Model"))
        self.Save.setText(_translate("self", "Save"))
        self.run.setText(_translate("self", "Run"))
        self.Edit.setText(_translate("self", "Edit"))
        self.Apply.setText(_translate("self", "Apply"))
        self.Delete.setText(_translate("self", "Delete"))
        self.AddF.setText(_translate("self", "New Field"))

class Field(QWidget):
    def __init__(self,name, Models, tabwid, cType, path):
        super().__init__(parent=tabwid.currentWidget())
        fields = ['CharField', 'AutoField', 'BigAutoField', 'BigIntegerField', 'BooleanField',
                  'DateField', 'DateTimeField', 'DecimalField', 'DurationField',
                  'EmailField', 'FilePathField', 'FloatField', 'IntegerField', 'NullBooleanField', 'PositiveIntegerField',
                   'SlugField', 'SmallIntegerField', 'TextField',
                  'TimeField', 'URLField', 'UUIDField', 'FileField']


        btnStyle = """QPushButton:hover{background-color:rgb(241, 90, 36);border:1px solid rgb(255, 255, 255);}\n
        QPushButton{color:white;background-color: rgb(50, 50, 50);height:50px;width:10px;border:1px solid rgb(255, 255, 255);}\n
        QPushButton:pressed{color:white;background-color: rgb(50, 50, 50);border:1px solid rgb(255, 255, 255);}\n"""
        self.logic = Logic(path)
        self.path = path
        self.Models = Models
        self.name = name
        self.tabWidget = tabwid
        self.verticalLayout = QVBoxLayout(self)
        self.Model = QLabel(self)
        self.Model.setText(name)
        self.Model.setFont(QFont('Reboto', 20, QFont.Bold))
        self.Model.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.verticalLayout.addWidget(self.Model)
        font = QFont('Reboto',12, QFont.Bold)
        self.Types = QComboBox(self)
        self.Types.setFont(font)
        self.Types.setObjectName("Types")
        self.Types.addItems(fields)
        self.verticalLayout.addWidget(self.Types)
        self.Types.setCurrentText(cType)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.EditF = QPushButton()
        self.EditF.setText("E")
        self.EditF.setStyleSheet(btnStyle)
        self.horizontalLayout.addWidget(self.EditF)
        self.DeleteF = QPushButton(self)
        self.DeleteF.setText("D")
        self.DeleteF.setStyleSheet(btnStyle)
        self.horizontalLayout.addWidget(self.DeleteF)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.DeleteF.clicked.connect(self.DelField)
        self.Types.currentTextChanged.connect(self.changeType)
        self.EditF.clicked.connect(self.editField)

    def editField(self):
        self.argField = EditField(self.name, self.Types.currentText(
        ), self.tabWidget.currentWidget().objectName(), self.path,self.Model)
        self.argField.exec_()

    def changeType(self, item):
        self.logic.editField(self.name, item, self.tabWidget.currentWidget().objectName(), True)

    def DelField(self): 
        item = self.Models[self.tabWidget.currentIndex()]
        self.logic.deleteField(self.tabWidget.currentWidget().objectName(), self.name)
        item['item'].removeWidget(self)
        del self 
        #item['col']-=1
        