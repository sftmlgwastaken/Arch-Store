import PyQt6.QtWidgets as pq
import library.lpak as lpak
from PyQt6.QtGui import QIcon
import os
from show_allert import show_allert
import webbrowser
def show(language, name, repo, aur_method):
    global row
    global more_info_window
    more_info_window = pq.QWidget()
    more_info_window.setWindowTitle(f"{lpak.get("more info about", language)}: {name}")
    more_info_window.setGeometry(0,0,900,600)
    more_info_window.setWindowIcon(QIcon("icon.png"))
    layout=pq.QGridLayout(more_info_window)
    

    if repo == "aur":
        pass
    elif repo == "flatpak":
        pass
    else:
        name = name.split(" ")[0]
        data = os.popen(f"pacman -Si {name}").read()
        data_list = data.split("\n")
        n = 0
        line = ""
        clear_data =[]
        tot = len(data_list)
        while n < tot-1:
            if " :" in data_list[n+1] or data_list[n+1] == "":     
                try:   
                    line = data_list[n].split(" : ")[1]
                except:
                    line = line + data_list[n]
                clear_data.append(line)
                line = ""
            else:
                line = line + data_list[n]
            n = n + 1

        print(clear_data[10])

        repo = clear_data[0]
        name = clear_data[1]
        version = clear_data[2]
        description = clear_data[3]
        arch = clear_data[4]
        url = clear_data[5]
        license_type = clear_data[6]
        group = clear_data[7]
        provides = clear_data[8]
        dependencies = clear_data[9]
        optional_dependencies = clear_data[10]
        conflict = clear_data[11]
        replaces = clear_data[12]
        download_size = clear_data[13]
        required_space = clear_data[14]
        packager = clear_data[15]
        creation_date = clear_data[16]
        validated_by = clear_data[17]

        attribute_repo_label = pq.QLabel(lpak.get("repository", language))
        attribute_name_label = pq.QLabel(lpak.get("name", language))
        attribute_version_label = pq.QLabel(lpak.get("version", language))
        attribute_description_label = pq.QLabel(lpak.get("description", language))
        attribute_arch_label = pq.QLabel(lpak.get("architecture", language))
        attribute_url_label = pq.QLabel(lpak.get("url", language))
        attribute_license_label = pq.QLabel(lpak.get("license", language))
        attribute_group_label = pq.QLabel(lpak.get("group", language))
        attribute_provides_label = pq.QLabel(lpak.get("provides", language))
        attribute_dependencies_label = pq.QLabel(lpak.get("dependencies", language))
        attribute_optionalDependencies_label = pq.QLabel(lpak.get("optional dependencies", language))
        attribute_conflict_label = pq.QLabel(lpak.get("conflict", language))
        attribute_replaces_label = pq.QLabel(lpak.get("replaces", language))
        attribute_downloadSize_label = pq.QLabel(lpak.get("download size", language))
        attribute_requiredSpace_label = pq.QLabel(lpak.get("required space", language))
        attribute_packager_label = pq.QLabel(lpak.get("packager", language))
        attribute_creationDate_label = pq.QLabel(lpak.get("creation date", language))
        attribute_validatedBy_label = pq.QLabel(lpak.get("validated by", language))
        
        attribute_repo_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_name_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_version_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_description_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_arch_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_url_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_license_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_group_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_provides_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_dependencies_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_optionalDependencies_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_conflict_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_replaces_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_downloadSize_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_requiredSpace_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_packager_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_creationDate_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_validatedBy_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")

        repo_label = pq.QLabel(clear_data[0])
        name_label = pq.QLabel(clear_data[1])
        version_label = pq.QLabel(clear_data[2])
        description_label = pq.QLabel(clear_data[3])
        arch_label = pq.QLabel(clear_data[4])
        url_label = pq.QLabel(clear_data[5])
        licenseType_label = pq.QLabel(clear_data[6])
        group_label = pq.QLabel(clear_data[7])
        provides_label = pq.QLabel(clear_data[8])
        dependencies_label = pq.QLabel(clear_data[9])
        optionalDependencies_label = pq.QLabel(clear_data[10])
        conflict_label = pq.QLabel(clear_data[11])
        replaces_label = pq.QLabel(clear_data[12])
        downloadSize_label = pq.QLabel(clear_data[13])
        requiredSpace_label = pq.QLabel(clear_data[14])
        packager_label = pq.QLabel(clear_data[15])
        creationDate_label = pq.QLabel(clear_data[16])
        validatedBy_label = pq.QLabel(clear_data[17])    

        

        # Inserimento nel layout
        row = 0

        def add_row(attr_label, value_label):
            global row
            layout.addWidget(attr_label, row, 0)
            layout.addWidget(value_label, row, 1)
            row += 1
            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            layout.addWidget(line, row, 0, 1, 2)
            row += 1

        add_row(attribute_repo_label, repo_label)
        add_row(attribute_name_label, name_label)
        add_row(attribute_version_label, version_label)
        add_row(attribute_description_label, description_label)
        add_row(attribute_arch_label, arch_label)
        add_row(attribute_url_label, url_label)
        add_row(attribute_license_label, licenseType_label)
        add_row(attribute_group_label, group_label)
        add_row(attribute_provides_label, provides_label)
        add_row(attribute_dependencies_label, dependencies_label)
        add_row(attribute_optionalDependencies_label, optionalDependencies_label)
        add_row(attribute_conflict_label, conflict_label)
        add_row(attribute_replaces_label, replaces_label)
        add_row(attribute_downloadSize_label, downloadSize_label)
        add_row(attribute_requiredSpace_label, requiredSpace_label)
        add_row(attribute_packager_label, packager_label)
        add_row(attribute_creationDate_label, creationDate_label)
        add_row(attribute_validatedBy_label, validatedBy_label)




        

    layout.setRowStretch(layout.rowCount(), 1)
    more_info_window.show()
