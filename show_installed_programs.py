import PyQt6.QtWidgets as pq
import library.lpak as lpak
from PyQt6.QtGui import QIcon
import os
from show_allert import show_allert
from PyQt6.QtCore import QProcess
def update(name, method, aur_method, working_dir, language):
    if method=="aur":        
        command = f"{aur_method} -S {name} --noconfirm"
    elif method=="pacman":
        command = f"pacman -S {name} --noconfirm"
    elif method == "flatpak":
        command = f"flatpak update {name} -y"

    with open(f"{working_dir}/actions.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(command)

    def start_update():
        global install_status        
        install_status = True
        button.setDisabled(True)
        label.setText(lpak.get("update in progress", language))
        progress_bar.setRange(0, 0) 
        update_window.repaint()  

        proc = QProcess(update_window)       
        def on_finished(exitCode, exitStatus):
            global install_status, installed_packages_window
            install_status = False
            progress_bar.setRange(0, 1)
            button.setText(lpak.get("finished", language))
            label.setText(lpak.get("finished", language))
            try:
                button.pressed.disconnect()
            except TypeError:
                pass
            button.setDisabled(False)
            button.clicked.connect(update_window.close)
            update_window.update()
            installed_packages_window.close()

        def on_error(err):
            global install_status
            install_status = False
            progress_bar.setRange(0, 1)
            label.setText(f"{lpak.get('error', language)}: {err}")
            button.setDisabled(False)
            update_window.update()
         
        proc.finished.connect(on_finished)
        proc.errorOccurred.connect(on_error)

        proc.start("pkexec", ["bash", os.path.join(working_dir, "actions.sh")])

    update_window = pq.QWidget()
    update_window.setGeometry(100, 100, 400, 200)
    update_window.setWindowIcon(QIcon(f"icon.png"))
    update_window.setWindowTitle(lpak.get("update", language))
    layout = pq.QVBoxLayout(update_window)
    label = pq.QLabel(lpak.get("click to start update", language))
    layout.addWidget(label)
    progress_bar = pq.QProgressBar()      
    layout.addWidget(progress_bar)  
    button = pq.QPushButton(lpak.get("start update", language))    
    layout.addWidget(button)
    button.pressed.connect(start_update)

    update_window.show()



    
def remove(name, method, aur_method, working_dir, language):
    global installed_packages_window
    if method=="aur":        
        command = f"{aur_method} -R {name} --noconfirm"
    elif method=="pacman":
        command = f"pacman -R {name} --noconfirm"
    elif method == "flatpak":
        command = f"flatpak uninstall {name} -y"      

    with open(f"{working_dir}/actions.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(command)

    def start_remove():
        global install_status, installed_packages_window    
        install_status = True
        button.setDisabled(True)
        label.setText(lpak.get("removal in progress", language))
        progress_bar.setRange(0, 0) 
        remove_window.repaint()  

        proc = QProcess(remove_window)       
        def on_finished(exitCode, exitStatus):
            global install_status, installed_packages_window   
            install_status = False
            progress_bar.setRange(0, 1)
            button.setText(lpak.get("finished", language))
            label.setText(lpak.get("finished", language))
            try:
                button.pressed.disconnect()
            except TypeError:
                pass
            button.setDisabled(False)
            button.clicked.connect(remove_window.close)
            remove_window.update()
            installed_packages_window.close()
            

        def on_error(err):
            global install_status
            install_status = False
            progress_bar.setRange(0, 1)
            label.setText(f"{lpak.get('error', language)}: {err}")
            button.setDisabled(False)
            remove_window.update()
         
        proc.finished.connect(on_finished)
        proc.errorOccurred.connect(on_error)

        proc.start("pkexec", ["bash", os.path.join(working_dir, "actions.sh")])

    remove_window = pq.QWidget()
    remove_window.setGeometry(100, 100, 400, 200)
    remove_window.setWindowIcon(QIcon(f"icon.png"))
    remove_window.setWindowTitle(lpak.get("removal", language))
    layout = pq.QVBoxLayout(remove_window)
    label = pq.QLabel(lpak.get("click to start removal", language))
    layout.addWidget(label)
    progress_bar = pq.QProgressBar()      
    layout.addWidget(progress_bar)  
    button = pq.QPushButton(lpak.get("start removal", language))    
    layout.addWidget(button)
    button.pressed.connect(start_remove)

    remove_window.show()

def show(language, working_dir, aur_method, pacman, aur, flatpak):
    global installed_packages_window
    installed_packages_window = pq.QWidget()
    installed_packages_window.setWindowTitle("Installed packages")
    installed_packages_window.setWindowIcon(QIcon("icon.png"))  
    installed_packages_window.setGeometry(0, 0, 600, 500)
    main_layout = pq.QVBoxLayout(installed_packages_window)

    # Scroll area
    scroll = pq.QScrollArea()
    scroll.setWidgetResizable(True)
    main_layout.addWidget(scroll)    
    container = pq.QWidget()
    layout = pq.QGridLayout(container)
    #

    #INTERFACE
    name_header = pq.QLabel(lpak.get("name", language))
    actions_header = pq.QLabel(lpak.get("actions", language))
    version_header = pq.QLabel(lpak.get("version", language))
    repo_header = pq.QLabel("Repo")

    name_header.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    actions_header.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    version_header.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    repo_header.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")

    layout.addWidget(actions_header, 0, 0)
    layout.addWidget(name_header, 0, 2)
    layout.addWidget(version_header, 0, 4)
    layout.addWidget(repo_header, 0, 3)
    row = 1
    
    if aur == "enable":
        aur_programs = os.popen(f"{aur_method} -Qm").read()
        aur_list = []
        aur_list = aur_programs.split("\n")
        for package in aur_list:
            repo = pq.QLabel("AUR")
            remove_button = pq.QPushButton(lpak.get("remove", language))
            update_button = pq.QPushButton(lpak.get("update", language))
            try:
                name, version = package.split(" ")
            except:
                continue
            name_label = pq.QLabel(name)
            version_label = pq.QLabel(version)    
            remove_button.pressed.connect(lambda pkg=name: remove(pkg, "aur", aur_method, working_dir, language))
            update_button.pressed.connect(lambda pkg=name: update(pkg, "aur", aur_method, working_dir, language))
            #
            layout.addWidget(remove_button, row, 0)
            layout.addWidget(update_button, row, 1)
            layout.addWidget(name_label, row, 2)
            layout.addWidget(repo, row, 3)
            layout.addWidget(version_label, row, 4)
            #line
            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            layout.addWidget(line, row + 1, 0, 1, 5)

            row = row + 2
            
            
    first_line = True
    if flatpak == "enable":
        flatpak_programs = os.popen("flatpak list --columns=name,application,version").read()
        flatpak_list = []
        flatpak_list = flatpak_programs.strip().split("\n")
        for package in flatpak_list:            
            if first_line == True:
                first_line = False
                continue            
            remove_button = pq.QPushButton(lpak.get("remove", language))
            update_button = pq.QPushButton(lpak.get("update", language))


            parts = package.split("\t")
            if len(parts) >= 3:
                name, program_id, version = parts[:3]                

            name_label = pq.QLabel(name)
            version_label = pq.QLabel(version)   
            repo = pq.QLabel("flatpak") 
            remove_button.pressed.connect(lambda pkg=name: remove(pkg, "flatpak", aur_method, working_dir, language))
            update_button.pressed.connect(lambda pkg=name: update(pkg, "flatpak", aur_method, working_dir, language))
            #
            layout.addWidget(remove_button, row, 0)
            layout.addWidget(update_button, row, 1)
            layout.addWidget(name_label, row, 2)
            layout.addWidget(repo, row, 3)
            layout.addWidget(version_label, row, 4)
            #line
            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            layout.addWidget(line, row + 1, 0, 1, 5)

            row = row + 2
    if pacman == "enable":
        pacman_list = []    
        pacman_programs = os.popen("pacman -Q").read()
        pacman_list = pacman_programs.split("\n")
        for package in pacman_list:
            remove_button = pq.QPushButton(lpak.get("remove", language))
            update_button = pq.QPushButton(lpak.get("update", language))
            try:
                name, version = package.split(" ")
            except:
                continue
            name_label = pq.QLabel(name)
            version_label = pq.QLabel(version)    
            remove_button.pressed.connect(lambda pkg=name: remove(pkg, "pacman", aur_method, working_dir, language))
            update_button.pressed.connect(lambda pkg=name: update(pkg, "pacman", aur_method, working_dir, language))
            repo = pq.QLabel("pacman") 
            #
            layout.addWidget(remove_button, row, 0)
            layout.addWidget(update_button, row, 1)
            layout.addWidget(name_label, row, 2)
            layout.addWidget(repo, row, 3)
            layout.addWidget(version_label, row, 4)
            #line
            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            layout.addWidget(line, row + 1, 0, 1, 5)

            row = row + 2

    container.setLayout(layout)
    scroll.setWidget(container)

    installed_packages_window.show()