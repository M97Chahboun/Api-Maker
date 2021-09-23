from PyQt5.QtCore import QProcess, QUrl
import socket
import subprocess
import sqlite3
from subprocess import Popen

class Logic:
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
