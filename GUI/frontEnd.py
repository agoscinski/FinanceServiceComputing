import os
import sys
import htmlPy
#from PyQt4 import QtGui
sys.path.append('../Kernel')

class FrontEndHandler():
    def __init__(self):
        # Initial confiurations
        self.BASE_DIR = os.path.abspath(os.path.dirname(__file__))

        # GUI initializations
        self.htmlPy_app = htmlPy.AppGUI(title=u"Application", width=1200, height=750, plugins=True)

        # GUI configurations
        self.htmlPy_app.static_path = os.path.join(self.BASE_DIR, "static/")
        self.htmlPy_app.template_path = os.path.join(self.BASE_DIR, "templates/")

        self.htmlPy_app.web_app.setMinimumWidth(1200)
        self.htmlPy_app.web_app.setMinimumHeight(750)
