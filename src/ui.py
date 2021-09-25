from PyQt5.QtWidgets import QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLayout, QMessageBox, QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget,QDesktopWidget,QLineEdit
from src.logic import Logic
from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from functools import partial
import os
from PyQt5.QtGui import QFont, QIcon,QPixmap
from src.edit_field import EditField

class ApiMakerUi(QWidget):
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

        self.styleBtn = """QPushButton{\n
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
        self.startApp()
        self.Models = []
        
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.Add = QPushButton(self)
        self.Add.setObjectName("Add")
        self.Add.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.Add, 0, 0, 1, 1)
        self.Save = QPushButton(self)
        self.Save.setObjectName("Save")
        self.Save.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.Save, 3, 1, 1, 1)
        self.run = QPushButton(self)
        self.run.setObjectName("run")
        self.run.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.run, 3, 0, 1, 1)
        self.Edit = QPushButton(self)
        self.Edit.setObjectName("Edit")
        self.Edit.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.Edit, 0, 1, 1, 1)
        self.Apply = QPushButton(self)
        self.Apply.setObjectName("Apply")
        self.Apply.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.Apply, 3, 2, 1, 1)
        self.Delete = QPushButton(self)
        self.Delete.setObjectName("Delete")
        self.Delete.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.Delete, 0, 2, 1, 1)
        self.AddF = QPushButton(self)
        self.AddF.setObjectName("AddF")
        self.AddF.setStyleSheet(self.styleBtn)
        self.gridLayout.addWidget(self.AddF, 1, 1, 1, 1)       
        self.tabWidget = QTabWidget(self)
        self.view = QWebEngineView(self)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 3)
        self.gridLayout.addWidget(self.view, 2, 1, 1, 3)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.AddF.clicked.connect(self.showField)
        self.Add.clicked.connect(self.showModel)
        self.Delete.clicked.connect(self.delModel)
        self.Apply.clicked.connect(self.logic.migrate)
       
        self.sizeScreen = QDesktopWidget().screenGeometry(-1)
        #print(" Screen size : "  + str(sizeObject.height()) + "x"  + str(sizeObject.width())) 768,1366
        #self.view.resize(self.sizeScreen.height()*0.31,self.sizeScreen.width()*0.10)
        ##self.gridLayout.addWidget(self.view)
        #self.view.setGeometry(QRect(240,150,sizeObject.width()*0.85,sizeObject.height()*0.65))
        #self.gridLayout.addWidget(self.view, 2, 1, 1, 3)
        self.run.clicked.connect(partial(self.logic.runServer,self.view))
        self.Edit.clicked.connect(self.EditModel)
        self.Save.clicked.connect(self.logic.make)
        self.tabs = 0
        

        
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

    def resizeEvent(self, event):
        self.sizeScreen= QDesktopWidget().screenGeometry(-1)
        return super(ApiMakerUi, self).resizeEvent(event)
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
                                str(text).replace(" ","_"): 'models.CharField(max_length=50,default="")'})

    def addModel(self, name):
        self.tab_2 = QWidget(self)       
        self.tab_2.setObjectName(name)
        self.tabWidget.addTab(self.tab_2, name)       
        self.layoutWidget = QWidget(self.tab_2)    
        self.scrollarea = QScrollArea(self.tab_2)
        self.scrollarea.setFixedWidth(self.sizeScreen.width()*0.18)
        self.scrollarea.setFixedHeight(self.sizeScreen.height()*0.8)
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
        #self.gridLayout.addLayout(self.gridLayout_4, 2, 1, 1, 2)
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
    def startApp(self):
        self.dlg = QDialog()
        self.dlg.setStyleSheet("QWidget{background-color: rgb(65, 65, 65);}\nQTabWidget::tab-bar {\n"
                           "     background-color: #fff;\n"
                           "}\n")
        pixmap = QPixmap("./icon.ico")
        self.verticalLayoutWidget = QWidget(self.dlg)
        self.verticalLayoutWidget.setGeometry(QRect(30, 20, 341, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.icon = QLabel(self.verticalLayoutWidget)
        self.icon.setObjectName("icon")
        self.icon.resize(200,200)
        self.icon.move(10,100)
        self.icon.setPixmap(pixmap.scaled(self.icon.size()))
        self.verticalLayout.addWidget(self.icon,alignment=Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.new = QPushButton(self.verticalLayoutWidget)
        self.new.setObjectName("new")
        self.horizontalLayout.addWidget(self.new)
        self.open = QPushButton(self.verticalLayoutWidget)
        self.open.setObjectName("open")
        self.horizontalLayout.addWidget(self.open)
        self.exit = QPushButton(self.verticalLayoutWidget)
        self.exit.setObjectName("exit")
        self.horizontalLayout.addWidget(self.exit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.new.setText("New")
        self.open.setText("open")
        self.exit.setText("exit")
        self.new.clicked.connect(self.createNewProject)
        self.open.clicked.connect(self.openProject)
        self.exit.clicked.connect(self.dlg.close)
        self.new.setStyleSheet(self.styleBtn)
        self.open.setStyleSheet(self.styleBtn)
        self.exit.setStyleSheet(self.styleBtn)
        self.dlg.setWindowTitle("API Maker")
        self.dlg.setWindowModality(Qt.ApplicationModal)
        self.dlg.exec_()

    def createNewProject(self):
        self.newDialog = QDialog()
        self.verticalLayoutWidget = QWidget(self.newDialog)
        self.newDialog.setStyleSheet("QWidget{background-color: rgb(65, 65, 65);}\nQTabWidget::tab-bar {\n"
                           "     background-color: #fff;\n"
                           "}\n")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 361, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.newProject = QLabel(self.verticalLayoutWidget)
        self.newProject.setAlignment(Qt.AlignCenter)
        self.newProject.setObjectName("label")
        self.verticalLayout.addWidget(self.newProject)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.projectName = QLabel(self.verticalLayoutWidget)
        self.projectName.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.projectName)
        self.appName = QLabel(self.verticalLayoutWidget)
        self.appName.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.appName)
        self.saveIn = QLabel(self.verticalLayoutWidget)
        self.saveIn.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.saveIn)
        self.pyVersion = QLabel(self.verticalLayoutWidget)
        self.pyVersion.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.pyVersion)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.prjName = QLineEdit(self.verticalLayoutWidget)
        self.prjName.setObjectName("lineEdit_2")
        self.verticalLayout_4.addWidget(self.prjName)
        self.apName = QLineEdit(self.verticalLayoutWidget)
        self.apName.setObjectName("lineEdit_3")
        self.verticalLayout_4.addWidget(self.apName)
        self.saveI = QLineEdit(self.verticalLayoutWidget)
        self.saveI.setObjectName("lineEdit")
        self.verticalLayout_4.addWidget(self.saveI)
        self.comboBox = QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["python 3.8","python 3.9"])
        self.verticalLayout_4.addWidget(self.comboBox)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.newProject.setText("New Project:")
        self.projectName.setText("Project name:")
        self.appName.setText("App name:")
        self.saveIn.setText("Save in:")
        self.pyVersion.setText("Python version:")
        self.create = QPushButton(self.verticalLayoutWidget)
        self.create.setText("Create")
        self.verticalLayout.addWidget(self.create)
        self.create.clicked.connect(self.callCreateNewProject)
        self.create.setStyleSheet(self.styleBtn)
        self.comboBox.setStyleSheet(self.styleBtn)
        self.newDialog.setWindowTitle("New Project | API Maker")
        self.newDialog.setWindowModality(Qt.ApplicationModal)
        self.newDialog.exec_()
        
    def callCreateNewProject(self):
        if self.prjName.text() and self.apName.text() and self.saveI.text() and self.comboBox.currentText():
            self.newDialog.close()
            self.dlg.close()
            print(self.prjName.text())
            print(self.apName.text())
            print(self.saveI.text())
            print(self.comboBox.currentText())            
            self.path = f"/mnt/42E23A0EE23A0727/{self.prjName.text()}/{self.apName.text()}"
            self.logic = Logic(self.path)
            self.project = '/'.join(self.path.split("\\")[:-1])
            self.project = self.project + "/" + self.project.split('/')[-1]
            self.logic.createNewProject(self.prjName.text(),self.apName.text(),"/mnt/42E23A0EE23A0727")
            self.logic.initState()
            self.logic.settingApp()
            self.initState()

    def openProject(self):
        self.dlg.close()
        self.path = self.GetDir()
        self.project = '/'.join(self.path.split("\\")[:-1])
        self.project = self.project + "/" + self.project.split('/')[-1]
        self.logic = Logic(self.path)
        self.logic.initState()
        self.logic.settingApp()
        self.initState()

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
        