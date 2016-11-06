import os
import sys
import htmlPy
#from PyQt4 import QtGui
sys.path.append('../Kernel')


# Initial confiurations
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# GUI initializations
htmlPy_app = htmlPy.AppGUI(title=u"Application", width=1200, height=750, plugins=True)


# GUI configurations
htmlPy_app.static_path = os.path.join(BASE_DIR, "static/")
htmlPy_app.template_path = os.path.join(BASE_DIR, "templates/")

htmlPy_app.web_app.setMinimumWidth(1200)
htmlPy_app.web_app.setMinimumHeight(750)
#htmlPy_app.window.setWindowIcon(QtGui.QIcon(BASE_DIR + "/static/img/icon.png"))

# Binding of back-end functionalities with GUI

# Import back-end functionalities
#from backEnd import python_app

# Register back-end functionalities
#htmlPy_app.bind(python_app())


# Instructions for running application
if __name__ == "__main__":
    # The driver file will have to be imported everywhere in back-end.
    # So, always keep app.start() in if __name__ == "__main__" conditional
    htmlPy_app.start()