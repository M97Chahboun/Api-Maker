from PyQt5.QtWidgets import  QCheckBox,  QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from src.logic import Logic
class EditField(QDialog):
    def __init__(self, field, fld, name, path,flname):
        super().__init__()
        allArgField = {'CharField': {'args': [], 'defaults': []}, 'AutoField': {'args': [], 'defaults': []}, 'BigAutoField': {'args': [], 'defaults': []}, 'BigIntegerField': {'args': [], 'defaults': []}, 'BooleanField': {'args': [], 'defaults': []}, 'DateField': {'args': ['auto_now', 'auto_now_add'], 'defaults': [False, False]}, 'DateTimeField': {'args': ['auto_now', 'auto_now_add'], 'defaults': [False, False]}, 'DecimalField': {'args': ['max_digits', 'decimal_places'], 'defaults': [None, None]}, 'DurationField': {'args': [], 'defaults': []}, 'EmailField': {'args': [], 'defaults': []}, 'FilePathField': {'args': ['path', 'match', 'recursive', 'allow_files', 'allow_folders'], 'defaults': ['', None, False, True, False]}, 'FloatField': {'args': [], 'defaults': []}, 'IntegerField': {'args': [], 'defaults': []}, 'NullBooleanField': {'args': [], 'defaults': []}, 'PositiveIntegerField': {'args': [], 'defaults': []},'SlugField': {'args': [], 'defaults': []}, 'SmallIntegerField': {'args': [], 'defaults': []}, 'TextField': {'args': [], 'defaults': []}, 'TimeField': {'args': ['auto_now', 'auto_now_add'], 'defaults': [False, False]}, 'URLField': {'args': [], 'defaults': []}, 'UUIDField': {'args': [], 'defaults': []}, 'FileField': {'args': ['upload_to', 'storage'], 'defaults': ['', None]}}
        fieldArg = {'args': ['verbose_name', 'name', 'primary_key', 'max_length', 'unique', 'blank', 'null', 'db_index', 'rel', 'default', 'editable', 'serialize', 'unique_for_date', 'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace', 'auto_created', 'validators', 'error_messages'], 'defaults': [None, None, False, None, False, False, False, False, None, "<class 'django.db.models.fields.NOT_PROVIDED'>", True, True, None, None, None, None, '', None, None, False, (), None]}
        self.flname = flname
        self.allArg = ""
        self.field = field
        self.logic = Logic(path)
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