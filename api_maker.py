
from PyQt5.QtWidgets import QApplication
import sys

from src.ui import ApiMakerUi

def main():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = ApiMakerUi()
    ex.showMaximized()
    sys.exit(app.exec_())
main()
# result = {}
# args = eval(f"inspect.getfullargspec(models.Field)")
# result = {"args":[],"defaults":[]}
# for i,t in enumerate(args.args[1:]):
#     result['args'].append(t)
#     result['defaults'].append(args.defaults[i])

