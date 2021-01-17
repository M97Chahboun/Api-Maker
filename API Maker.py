
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QInputDialog, QLabel, QLayout, QLineEdit, QMessageBox, QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget,QDesktopWidget
import sys
from PyQt5.QtCore import QCoreApplication, QMetaObject, QProcess, QRect, QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import shutil
import os
import subprocess
from subprocess import Popen
import time
from functools import partial
from threading import Thread
import signal
from PyQt5.QtGui import QFont, QIcon
import socket
import webbrowser
import sqlite3
class logic:
    def __init__(self, path):
        self.path = path
        self.project = '/'.join(path.split('\\')[:-1])
        self.pth = self.project
        self.app = self.path.split("\\")[-1]
        self.project = self.project + "/" + self.project.split('/')[-1]
        self.process = QProcess()
        self.prc = {"run":self.process,"make":self.process,"mig":self.process,"browser":self.process}
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)

    def initState(self):
        try:
            a = open(f"{self.path}/serializers.py", "r")
        except:
            a = open(f"{self.path}/serializers.py", "w+").write(
                'from rest_framework import serializers,compat\nfrom .models import *\n\n')
        if "from rest_framework import viewsets\nfrom .serializers import *\nfrom .models import *\n" not in open(f"{self.path}/views.py", "r").read():
            a = open(f"{self.path}/views.py", "w").write(
                'from rest_framework import viewsets\nfrom .serializers import *\nfrom .models import *\n')
        if "from .models import *" not in open(f"{self.path}/admin.py", "r").read():
            a = open(f"{self.path}/admin.py",'a')
            a.write(f"\nfrom .models import *\n\n")
            a.close()

        self.addToUrls()

    def listToStr(self, mylist):
        result = ""
        for i in mylist:
            result += i+'\n'
        return result

    def delItem(self, cl):
        self.delModel(cl, f"{self.path}/models.py")
        self.delModel(cl, f"{self.path}/views.py")
        self.delModel(cl, f"{self.path}/serializers.py")
        self.delRouter(cl)
        self.delAdmin(cl)

    def renameAll(self,cl,ncl):
        self.renameItem(f"{self.path}/models.py",cl,ncl)
        self.renameItem(f"{self.path}/views.py",cl,ncl)
        self.renameItem(f"{self.path}/serializers.py",cl,ncl)
        self.renameItem(f"{self.path}/admin.py",cl,ncl)
        self.renameItem(f'{self.project}/urls.py',cl,ncl)
        


    def renameItem(self,file,cl,ncl):
        dire = {f"{self.path}/models.py":[f'class {cl}(models.Model):',f'class {ncl}(models.Model):'],
        f"{self.path}/views.py":[f'class {cl}ViewSet(viewsets.ModelViewSet):\n    queryset = {cl}.objects.all()\n    serializer_class = {cl}Serializer',f'class {ncl}ViewSet(viewsets.ModelViewSet):\n    queryset = {ncl}.objects.all()\n    serializer_class = {ncl}Serializer'],
        f"{self.path}/serializers.py":[f"class {cl}Serializer(serializers.HyperlinkedModelSerializer):\n    class Meta:\n        model = {cl}",f"class {ncl}Serializer(serializers.HyperlinkedModelSerializer):\n    class Meta:\n        model = {ncl}"],
        f"{self.path}/admin.py":[f"admin.site.register({cl})",f"admin.site.register({ncl})"],
        f'{self.project}/urls.py':[f"router.register(r'{cl}', {cl}ViewSet)",f"router.register(r'{ncl}', {ncl}ViewSet)"]
        }

        fl = open(file,'r').read()
        new = fl.replace(dire[file][0],dire[file][1])
        open(file,'w').write(new)
    def delAdmin(self, cl):
        ad = open(f"{self.path}/admin.py", 'r').readlines()
        for u in ad:
            if u == '\n':
                ad.remove(u)
        for i in ad:
            if f"admin.site.register({cl})" in i:
                ad.remove(i)

        ad = open(f"{self.path}/admin.py",
                  'w').write(self.listToStr(ad).strip())

    def delModel(self, cl, file):
        tl = cl
        t = ""
        mdl = open(file, 'r').read()
        if file == f"{self.path}/models.py":
            cl = " "+cl+"(models.Model):"
            spl = f'class'
            t = " "
        elif file == f"{self.path}/views.py":
            cl = "ViewSet(viewsets.ModelViewSet):"
            spl = f'class {tl}'
        else:
            cl = "Serializer(serializers.HyperlinkedModelSerializer):"
            spl = f'class {tl}'

        imp = mdl.split(spl)[0]
        mdls = mdl.split(spl)[1:]
        mdlsv = mdl.split(spl)[1:]
        for i in mdls:
            mdlsv[mdlsv.index(i)] = spl + t + i.strip()+"\n"
            if cl == i.split('\n')[0][:i.find(':')+1]:
                mdlsv.remove(spl+t+i.strip()+"\n")
        mdlsv.insert(0, imp.strip())
        mdl = open(file, 'w').write(self.listToStr(mdlsv).strip())

    def addRouter(self, cl):
        with open(f'{self.project}/urls.py', 'r') as router:
            router = router.read()
            new = router.replace(router[router.find("router = "):router.rfind("DefaultRouter()")+len("DefaultRouter()")], router[router.find(
                "router = "):router.rfind("DefaultRouter()")+len("DefaultRouter()")]+f"\nrouter.register(r'{cl}', {cl}ViewSet)")
            open(f'{self.project}/urls.py', 'w').write(new)

    def delRouter(self, cl):
        with open(f'{self.project}/urls.py', 'r') as router:
            a = router.read().split('\n')
            for i in a:
                if cl in i:
                    a.remove(i)
            open(f'{self.project}/urls.py',
                 'w').write(self.listToStr(a).strip())

    def addToUrls(self):
        model = open(f'{self.project}/urls.py', 'r').read()
        if "register" not in model:
            find = model.find('[')
            a = model[find:model.find(']', find+1)].split('),')
            a[0] = a[0]+"),"
            a.append("path('', include(router.urls)),")
            a.append("]")
            h = model[find:model.find(']', find+1)].split('),')
            h[0] = h[0]+"),\n"+"]"
            h = self.listToStr(h)
            t = model.replace(h.strip(), self.listToStr(a).strip())
            pth = self.path.split('\\')[-1]
            new = t.replace("from django.urls import path",
                            f"from rest_framework import routers\nfrom django.urls import include, path\nfrom {pth}.views import *\nrouter = routers.DefaultRouter()\n")
            model = open(f'{self.project}/urls.py', 'w').write(new)

    def newModel(self, cl):
        self.addRouter(cl)
        model = open(f"{self.path}/models.py", 'a')
        serializer = open(f"{self.path}/serializers.py", "a").write(f"""\nclass {cl}Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = {cl}
        fields = []""")
        open(f"{self.path}/views.py", "a").write(f"""\nclass {cl}ViewSet(viewsets.ModelViewSet):
    queryset = {cl}.objects.all()
    serializer_class = {cl}Serializer""")
        template = f"\nclass {cl}(models.Model):\n"
        model.write(template)
        model.close()
        open(f"{self.path}/admin.py",
             'a').write(f"\nadmin.site.register({cl})\n")

    def addField(self, model, field):
        mdl = open(f"{self.path}/models.py", 'r').read()
        srz = open(f"{self.path}/serializers.py", 'r').read()
        index = srz.find(f'class {model}Serializer')
        mdls = srz[index:srz.find(']', index+1)+1]
        ofld = mdls[mdls.find('fields = ')+len('fields = '):mdls.find("]")+1]
        nfld = eval(ofld)
        nfld.extend(field)
        nmdl = mdls.replace(ofld, str(nfld))
        open(f"{self.path}/serializers.py",'w').write(srz.replace(mdls, str(nmdl)))
        for itm in mdl.split("class"):
            if " "+ model+"(models.Model):" == itm[:itm.find(':')+1]:
                a = " "+itm.strip() + f"\n    {list(field.keys())[0]} = {list(field.values())[0]}"  
                w = mdl.replace(" "+itm.strip(), a).strip()
        file = open(f"{self.path}/models.py", 'w').write(w)

    def deleteField(self, model, field,delete=True,nw=""):
        # Ser
        srz = open(f"{self.path}/serializers.py", 'r').read()
        index = srz.find(f'class {model}Serializer')
        mdl = srz[index:srz.find(']', index+1)+1]
        ofld = mdl[mdl.find('fields = ')+len('fields = '):mdl.find("]")+1]
        nfld = eval(ofld)
        if delete:
            nfld.remove(field)
        else:
            nfld[nfld.index(field)] = nw
        open(f"{self.path}/serializers.py",
             'w').write(srz.replace(ofld, str(nfld)))
        # models
        mdl = open(f"{self.path}/models.py", 'r').read()
        for itm in mdl.split("class"):
            if model in itm:
                a = itm.split('\n')
                for u in a:
                    if field + " = " in u:
                        if delete:
                            try:
                                a.remove(u)
                            except:
                                pass
                        else:
                            nwd = u.replace(field,nw)
                            a[a.index(u)] = a[a.index(u)].replace(u,nwd)
                w = mdl.replace(itm.strip(), self.listToStr(a).strip()).strip()
                file = open(f"{self.path}/models.py", 'w').write(w)

    def getArg(self, mdl, field):
        model = open(f"{self.path}/models.py", 'r').read()
        result = {}
        for i in model.split("class "):
            if mdl in i:
                mldc = i
                for u in i.split('\n'):
                    if field+" = " in u:
                        tp = u[u.find("(")+1:-1].strip()[:-1]
                        for t in tp.split(','):
                            spl = t.split('=')
                            result[spl[0]] = spl[1].replace('"', '')

        return result

    def editField(self, field, newData, mdl, checkF):
        model = open(f"{self.path}/models.py", 'r').read()
        #new = model.readlines()
        current = ""
        mldc = ""
        fldc = ""
        rpl = ""
        for i in model.split("class "):
            if mdl in i:
                mldc = i
                for u in i.split('\n'):
                    if field + " = " in u:
                        current = u
                        if checkF:
                            fldc = u[u.find(".")+1:u.find("(")].strip()
                        else:
                            fldc = u[u.find("("):].strip()
                        rpl = newData
        nfld = current.replace(fldc, rpl)
        new = mldc.replace(current, nfld)
        open(f"{self.path}/models.py", 'w').write(model.replace(mldc, new))

    def getModels(self):
        result = {}
        mdl = open(f"{self.path}/models.py", 'r').read().strip()
        for itm in mdl.split("class"):
            if 'import' not in itm:
                result[itm.split('\n')[0][:itm.split(
                    '\n')[0].find('(')].strip()] = []
                for u in itm.split('\n')[1:]:
                    if u[:u.find('=')].strip() != '':
                        result[itm.split('\n')[0][:itm.split('\n')[0].find(
                            '(')].strip()].append([u[:u.find('=')].strip()])
                        fl = u[u.find('=')+2:].strip()
                        result[itm.split('\n')[0][:itm.split('\n')[0].find(
                            '(')].strip()][-1].append(fl[fl.find(".")+1:fl.find("(")])

        return result

    def settingApp(self):
        model = open(f'{self.project}\settings.py', 'r').read()
        ip = model.find("ALLOWED_HOSTS")
        ipt = model[ip+len("ALLOWED_HOSTS")+2:model.find(']', ip)+1]
        nipt = eval(ipt)
        nipt.insert(0,f"{self.ip_address}")
        b = model.find("INSTALLED_APPS")
        t = model[b+len("INSTALLED_APPS")+2:model.find(']', b)+1]
        dt = eval(model[b+len("INSTALLED_APPS")+2:model.find(']', b)+1])
        if dt.count(self.path.split('\\')[-1]) == 0:
            dt.append(self.path.split('\\')[-1])
        if dt.count('rest_framework') == 0:
            dt.append('rest_framework')
        old = model.replace("ALLOWED_HOSTS ="+ipt,"ALLOWED_HOSTS = "+str(nipt))
        model = open(f'{self.project}\settings.py', 'w')
        model.write(old.replace(t, str(dt)))
        model.close()

    def ttsg(self,c):
        # try:
        #     shutil.rmtree(f'{self.path}\migrations')
        # except:
        #     pass
        # commands = [f"python {self.pth}\manage.py makemigrations",
        #             f"python {self.pth}\manage.py migrate"]
        # for com in commands:
        #     process = Popen(com, shell=False,
        #                     stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        #     l, m = process.communicate(bytes(c,"utf-8"))
        #     print(l, m)
        #     time.sleep(0.5)
        pass

    def killAll(self):
        for i in self.prc.keys():
            if i != 'run':
                self.prc[i].kill()
                self.prc[i].terminate()

    def killRun(self):
        self.prc['run'].kill()
        self.prc['run'].terminate()
        del self.prc['run']
    def delMig(self):
        connection = sqlite3.connect(f"{self.pth}\db.sqlite3")
        cursor = connection.cursor()
        deleteSQLStatememnt = f'DELETE from django_migrations where app="{self.app}"'
        cursor.execute(deleteSQLStatememnt)
        connection.close()
    def make(self):
        self.killAll()
        print(self.project)
        com = f'python "{self.pth}\manage.py" makemigrations {self.app}'
        process = Popen(com, shell=False,
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        l, m = process.communicate(bytes("y","utf-8"))
        print(l, m)
        # self.process = QProcess()
        # com = f'python "{self.pth}\manage.py" makemigrations mini'
        # self.process.start(com)
        # self.process.waitForStarted()
        # self.process.write(u'y'.encode('utf-8'))
        # self.process.waitForReadyRead()
        # print(str(self.process.readAll(), 'utf-8'))
        # self.prc['make'] = self.process

    def migrate(self):
        self.killAll()
        self.process = QProcess()
        com = f'python "{self.pth}\manage.py" migrate'
        self.process.start(com)
        self.process.waitForReadyRead()
        print(str(self.process.readAll(), 'utf-8'))
        self.prc['mig'] = self.process
        
    def RunServer(self,wb):
        self.killAll()
        self.process = QProcess()
        com = f'python "{self.pth}\manage.py" runserver 0.0.0.0:8000'
        self.process.start(com)
        self.process.waitForReadyRead()
        print(str(self.process.readAll(), 'utf-8'))
        self.prc['run'] = self.process
        wb.setUrl(QUrl(f'http://{self.ip_address}:8000'))
        #webbrowser.open('http://{}:8000'.format(self.ip_address))


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
        print(self.project)
        self.logic = logic(self.path)
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
        self.logic = logic(path)
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
        
    
class EditField(QDialog):
    def __init__(self, field, fld, name, path,flname):
        super().__init__()
        allArgField = {'CharField': {'args': [], 'defaults': []}, 'AutoField': {'args': [], 'defaults': []}, 'BigAutoField': {'args': [], 'defaults': []}, 'BigIntegerField': {'args': [], 'defaults': []}, 'BooleanField': {'args': [], 'defaults': []}, 'DateField': {'args': ['auto_now', 'auto_now_add'], 'defaults': [False, False]}, 'DateTimeField': {'args': ['auto_now', 'auto_now_add'], 'defaults': [False, False]}, 'DecimalField': {'args': ['max_digits', 'decimal_places'], 'defaults': [None, None]}, 'DurationField': {'args': [], 'defaults': []}, 'EmailField': {'args': [], 'defaults': []}, 'FilePathField': {'args': ['path', 'match', 'recursive', 'allow_files', 'allow_folders'], 'defaults': ['', None, False, True, False]}, 'FloatField': {'args': [], 'defaults': []}, 'IntegerField': {'args': [], 'defaults': []}, 'NullBooleanField': {'args': [], 'defaults': []}, 'PositiveIntegerField': {'args': [], 'defaults': []},'SlugField': {'args': [], 'defaults': []}, 'SmallIntegerField': {'args': [], 'defaults': []}, 'TextField': {'args': [], 'defaults': []}, 'TimeField': {'args': ['auto_now', 'auto_now_add'], 'defaults': [False, False]}, 'URLField': {'args': [], 'defaults': []}, 'UUIDField': {'args': [], 'defaults': []}, 'FileField': {'args': ['upload_to', 'storage'], 'defaults': ['', None]}}
        fieldArg = {'args': ['verbose_name', 'name', 'primary_key', 'max_length', 'unique', 'blank', 'null', 'db_index', 'rel', 'default', 'editable', 'serialize', 'unique_for_date', 'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace', 'auto_created', 'validators', 'error_messages'], 'defaults': [None, None, False, None, False, False, False, False, None, "<class 'django.db.models.fields.NOT_PROVIDED'>", True, True, None, None, None, None, '', None, None, False, (), None]}
        self.flname = flname
        self.allArg = ""
        self.field = field
        self.logic = logic(path)
        self.fld = fld
        self.name = name
        self.path = path
        self.args = fieldArg['args']
        self.default = fieldArg['defaults']
        currentArg = self.logic.getArg(self.name, self.field)
        chcld = allArgField[self.fld]
        for u, i in enumerate(chcld['args']):
            if i not in self.args:
                self.args.append(i)
                self.default.append(chcld["defaults"][u])
        self.VC = QVBoxLayout(self)
        self.args.insert(0,"Field name :")
        self.default.insert(0,self.field)
        for i in range(len(self.args)):
            self.HC = QHBoxLayout()
            self.VC.addLayout(self.HC)
            lbl = QLabel(str(self.args[i]))
            if bool == type(self.default[i]):
                if self.args[i] in list(currentArg.keys()):
                    txt = QCheckBox()
                    txt.setChecked(bool(currentArg[self.args[i]]))
                else:
                    txt = QCheckBox()
                    txt.setChecked(self.default[i])
            else:
                if self.args[i] in list(currentArg.keys()):
                    txt = QLineEdit(str(currentArg[self.args[i]]))
                else:
                    txt = QLineEdit(str(self.default[i]))

            self.HC.addWidget(lbl)
            self.HC.addWidget(txt)
        self.HC = QHBoxLayout()
        self.VC.addLayout(self.HC)
        ok = QPushButton()
        ok.setText("OK")
        cnl = QPushButton()
        cnl.setText("Cancel")
        self.HC.addWidget(ok)
        self.HC.addWidget(cnl)
        cnl.clicked.connect(self.cancel)
        ok.clicked.connect(self.save)
        self.show()

    def save(self):
        child = self.children()[1:-2]
        self.allArg += "("
        a = 0
        for vc in range(int(len(child)/2)):
            if QCheckBox == type(child[vc+a+1]):
                wdt = child[vc+a+1].isChecked()
            else:
                wdt = child[vc+a+1].text()
            if child[vc].text() == "Field name :":
                self.field = self.flname.text()
                self.flname.setText(wdt)
                self.logic.deleteField(self.name, self.field,False,wdt)  
            elif str(self.default[vc]) != str(wdt):
                self.allArg += f"{child[vc+a].text()}="
                if wdt == "" or wdt == None:
                    self.allArg += f'"",'
                else:
                    if type(wdt) == bool:
                        self.allArg += f"{wdt},"
                    else:
                        if wdt.isalpha():
                            self.allArg += f'"{wdt}",'
                        else:
                            self.allArg += f"{wdt},"

            a += 1
        self.allArg += ")"
        self.logic.editField(self.field, self.allArg, self.name, False)
        self.hide()

    def cancel(self):
        self.hide()
def main():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Ui_Form()
    ex.showMaximized()
    sys.exit(app.exec_())
main()
# result = {}
# args = eval(f"inspect.getfullargspec(models.Field)")
# result = {"args":[],"defaults":[]}
# for i,t in enumerate(args.args[1:]):
#     result['args'].append(t)
#     result['defaults'].append(args.defaults[i])

