import PyQt6.QtWidgets as pq
import library.lpak as lpak
from PyQt6.QtGui import QIcon
import os
from show_allert import show_allert
def open_appimages_settings(language, working_dir):
        global appimages_window
        def update_appimage_window(name, program_user_base):
            appimage_path, _ = pq.QFileDialog.getOpenFileName(
                 
                caption=lpak.get("select an appimage", language),
                filter=("AppImage (*.AppImage)")
            )
            if appimage_path:  
                button.setText(str(appimage_path))
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.AppImage")
            os.system(f"mv '{appimage_path}' '{AppImagesDir}/{name}-{program_user_base}.AppImage'")
            show_allert(lpak.get("update completed", language), lpak.get("update completed", language))            

        def remove_appimage(name, program_user_base):            
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.AppImage")
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.png")
            if program_user_base == "-":
                cmd = f"rm '/usr/share/applications/{name}-archstore.desktop'"
                subprocess.run(["pkexec", "bash", "-c", cmd])                
            else:
                desktop_path = os.path.expanduser(f"~/.local/share/applications/{name}-archstore.desktop")
                os.remove(desktop_path)
            with open(f"{working_dir}/appimages.data.conf", "r") as f:
                appimage_data = f.readlines()
            with open(f"{working_dir}/appimages.data", "w") as f:
                for line in appimage_data:
                    if line != f"{name}|{program_user_base}":
                        f.write(line)
            show_allert(lpak.get("remove completed", language), lpak.get("remove completed", language))   
        

        appimages_window = pq.QWidget()
        appimages_window.setWindowTitle(lpak.get("manage appimages", language))
        appimages_window.setWindowIcon(QIcon(f"{working_dir}/icon.png"))       
        appimages_window.setGeometry(0, 0, 600, 500)    
        layout = pq.QVBoxLayout(appimages_window)
        # Scroll Area
        scroll = pq.QScrollArea()
        scroll.setWidgetResizable(True)

        container = pq.QWidget()
        container_layout = pq.QGridLayout(container)
        container.setLayout(container_layout)

        if not os.path.isfile(f"{working_dir}/appimages.data"):
            with open(f"{working_dir}/appimages.data", "w") as f:
                pass

        with open(f"{working_dir}/appimages.data", "r") as f:
            appimages_data = f.readlines()

        
        row = 0
        if appimages_data == []:
            no_appimage_apps_label = pq.QLabel(lpak.get("no appimages app", language))
            container_layout.addWidget(no_appimage_apps_label)
        else:            
            actions_label_title= pq.QLabel(lpak.get("actions", language))
            name_label_title=pq.QLabel(lpak.get("name",language))
            user_label_title=pq.QLabel(lpak.get("user", language))

            container_layout.addWidget(actions_label_title, 0, 0)
            container_layout.addWidget(name_label_title, 0, 2)
            container_layout.addWidget(user_label_title, 0, 3)
            


            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            container_layout.addWidget(line, 1, 0, 1, 4)

            row = 2
            for app in appimages_data:
                try:
                    name, user = app.strip().split("|")
                    if user == "-" or user == user_name:                       

                        remove_button = pq.QPushButton(lpak.get("remove", language))
                        remove_button.clicked.connect(lambda _, n=name, u=user: remove_appimage(n, u))

                        update_button = pq.QPushButton(lpak.get("update", language))
                        update_button.clicked.connect(lambda _, n=name, u=user: update_appimage_window(n, u))

                        container_layout.addWidget(remove_button, row, 0)
                        container_layout.addWidget(update_button, row, 1)                       
                        container_layout.addWidget(pq.QLabel(name), row, 2)                      
                        container_layout.addWidget(pq.QLabel(user), row, 3)
                    
                        line = pq.QFrame()
                        line.setFrameShape(pq.QFrame.Shape.HLine)
                        container_layout.addWidget(line, row + 1, 0, 1, 4)
                        row = row +2
                except Exception as e:
                    print("Errore caricando appimages:", e)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        container_layout.setRowStretch(container_layout.rowCount(), 1)

        appimages_window.show()

def start_add_appimage(language, working_dir):
            def select_file_appimage(button, parent_window):
                appimage_path, _ = pq.QFileDialog.getOpenFileName(
                    parent=parent_window,  
                    caption=lpak.get("select an appimage", language),
                    filter=("AppImage (*.AppImage)")
                )
                if appimage_path:  
                    button.setText(str(appimage_path))
            def select_file_icon(button, parent_window):
                icon_path, _ = pq.QFileDialog.getOpenFileName(
                    parent=add_appimage_window,
                    caption=lpak.get("select an icon", language),
                    filter= "PNG (*.png)"
                )
                if icon_path:
                    button.setText(str(icon_path))
            
            def confirm_appimage_install(name_text, path_but, icon_but, category_selection):
                name = name_text.text()
                path = path_but.text()
                icon = icon_but.text()
                category = category_selection.currentText()
                if "|" in name or name == None or name == "":
                    show_allert(lpak.get("illegal caracter", language), lpak.get("you can't use the following caracther", language)+": |")
                    return
                if not os.path.isfile(path):
                    show_allert(lpak.get("invalid appimage location", language), lpak.get("the appimage you selected was not found", language))
                    return
                if not os.path.isfile(icon):
                    show_allert(lpak.get("invalid icon location", language), lpak.get("the icon you selected was not found", language))
                    return    

                response = pq.QMessageBox.question(add_appimage_window,
                    lpak.get("confirm installation", language),
                    lpak.get("do you want to install it for all users", language),
                    pq.QMessageBox.StandardButton.Yes | pq.QMessageBox.StandardButton.No,
                    pq.QMessageBox.StandardButton.No
                ) 
                
                if response == pq.QMessageBox.StandardButton.Yes:
                    program_user = "-"
                else:
                    program_user = user_name
                os.system(f"mv '{icon}' '{AppImagesDir}/{name}-{program_user}.png'")
                os.system(f"mv '{path}' '{AppImagesDir}/{name}-{program_user}.AppImage'")
                desktop_entry_data = f"[Desktop Entry]\nType=Application\nName={name}\nExec='{AppImagesDir}/{name}-{program_user}.AppImage'\nIcon={AppImagesDir}/{name}-{program_user}.png\nCategories={category};"
                if program_user == "-":
                    with open("desktop_temp", "w") as f:
                        f.write(desktop_entry_data)
                    subprocess.run([
                            "pkexec", "cp", f"{working_dir}/desktop_temp", f"/usr/share/applications/{name}-archstore.desktop"
                        ])
                    os.remove("desktop_temp")
                else:
                    desktop_path = os.path.expanduser(f"~/.local/share/applications/{name}-archstore.desktop")
                    with open(desktop_path, "w") as f:
                        f.write(desktop_entry_data)
                with open(f"{working_dir}/appimages.data", "r") as f:
                    appimage_file_data = f.readlines()
                with open (f"{working_dir}/appimages.data", "w") as f:
                    for line in appimage_file_data:
                        f.write(line)                        
                    f.write(f"\n{name}|{program_user}")
                show_allert(lpak.get("installation completed", language), lpak.get("installation completed", language))
            
            add_appimage_window = pq.QWidget()
            add_appimage_window.setGeometry(0, 0, 900, 500)
            add_appimage_window.setWindowIcon(QIcon(f"{working_dir}/icon.png"))
            add_appimage_window.setWindowTitle(lpak.get("add appimage", language))
            appimage_name_label = pq.QLabel(lpak.get("name", language))
            appimage_name_textbox = pq.QLineEdit("")
            appimage_path_label = pq.QLabel(lpak.get("path", language))
            appimage_path_button = pq.QPushButton(lpak.get("select an appimage", language))
            appimage_path_button.pressed.connect(lambda path_button=appimage_path_button, back_top=add_appimage_window: select_file_appimage(path_button, back_top))
            appimage_ico_label = pq.QLabel(lpak.get("icon", language))
            appimage_ico_button = pq.QPushButton(lpak.get("select an icon", language))
            appimage_ico_button.pressed.connect(lambda ico_button = appimage_ico_button, back_top=add_appimage_window: select_file_icon(ico_button, back_top))      
            avaible_appimage_types = ["Utility", "Game", "Graphics", "Network", "AudioVideo", "Development", "Office", "Presentation"]
            menu_select_type = pq.QComboBox()
            menu_select_type.addItems(avaible_appimage_types)
            label_type=pq.QLabel(lpak.get("app type", language))
            appimage_confirm_button = pq.QPushButton(lpak.get("install appimage",language))
            appimage_confirm_button.pressed.connect(lambda name=appimage_name_textbox, path=appimage_path_button, icon=appimage_ico_button, tipe=menu_select_type: confirm_appimage_install(name, path, icon, tipe))
            
            #
            layout = pq.QGridLayout(add_appimage_window)

            layout.addWidget(appimage_name_label, 0, 0)
            layout.addWidget(appimage_name_textbox, 0, 1)
            layout.addWidget(appimage_path_label, 1,0)
            layout.addWidget(appimage_path_button,1,1)
            layout.addWidget(appimage_ico_label, 2, 0)
            layout.addWidget(appimage_ico_button, 2, 1)
            layout.addWidget(label_type, 3, 0)
            layout.addWidget(menu_select_type, 3, 1)
            layout.addWidget(appimage_confirm_button, 4, 2)
            add_appimage_window.show()       