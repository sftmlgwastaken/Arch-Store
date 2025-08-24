import shutil
from PyQt6.QtGui import QIcon
import PyQt6.QtWidgets as pq
import webbrowser
import library.lpak as lpak
from show_allert import show_allert
def show_window(language):
    global installation_methods_window


    def install_flatpak():
        show_allert(lpak.get("instructions", language), lpak.get("search for flatpak in the store and install it", language))

    def install_paru():
        webbrowser.open("https://github.com/Morganamilo/paru")

    def install_yay():
        webbrowser.open("https://github.com/Jguer/yay")



    installation_methods_window = pq.QWidget()
    installation_methods_window.setWindowTitle(lpak.get("manage installation methods", language))
    installation_methods_window.setGeometry(0, 0, 550, 200)
    layout = pq.QGridLayout(installation_methods_window)
    installation_methods_window.setWindowIcon(QIcon("icon.png"))

    def is_installed(cmd):
        return shutil.which(cmd) is not None

    method_label = pq.QLabel(lpak.get("installation method", language))
    status_label = pq.QLabel(lpak.get("status", language))
    method_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    status_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")

    flatpak_status = is_installed("flatpak")
    paru_status = is_installed("paru")
    yay_status = is_installed("yay")

    flatpak_label = pq.QLabel("Flatpak")
    if flatpak_status == True:
        flatpak_status_label = pq.QLabel(lpak.get("installed", language))
    else:
        flatpak_status_label = pq.QLabel(lpak.get("not installed", language))
        flatpak_install_button = pq.QPushButton(lpak.get("install", language))
        flatpak_install_button.pressed.connect(install_flatpak)
        layout.addWidget(flatpak_install_button, 2, 3)

    paru_label = pq.QLabel("Paru")
    if paru_status == True:
        paru_status_label = pq.QLabel(lpak.get("installed", language))
    else:
        paru_status_label = pq.QLabel(lpak.get("not installed", language))
        paru_install_button = pq.QPushButton(lpak.get("install", language))
        paru_install_button.pressed.connect(install_paru)
        layout.addWidget(paru_install_button, 4, 3)

    yay_label = pq.QLabel("Yay")
    if yay_status == True:
        yay_status_label = pq.QLabel(lpak.get("installed", language))
    else:
        yay_status_label = pq.QLabel(lpak.get("not installed", language))
        yay_install_button = pq.QPushButton(lpak.get("install", language))
        yay_install_button.pressed.connect(install_yay)
        layout.addWidget(yay_install_button, 6, 3)

    def make_separator():
        line = pq.QFrame()
        line.setFrameShape(pq.QFrame.Shape.HLine)
        line.setFrameShadow(pq.QFrame.Shadow.Sunken)
        return line

    layout.addWidget(method_label, 0, 0)
    layout.addWidget(status_label, 0, 1)
    layout.addWidget(make_separator(), 1, 0, 1, 4)

    layout.addWidget(flatpak_label, 2, 0)
    layout.addWidget(flatpak_status_label, 2, 1)
    layout.addWidget(make_separator(), 3, 0, 1, 4)

    layout.addWidget(paru_label, 4, 0)
    layout.addWidget(paru_status_label, 4, 1)
    layout.addWidget(make_separator(), 5, 0, 1, 4)

    layout.addWidget(yay_label, 6, 0)
    layout.addWidget(yay_status_label, 6, 1)
    layout.addWidget(make_separator(), 7, 0, 1, 4)


    layout.setRowStretch(layout.rowCount(), 1)

    installation_methods_window.show()

