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
        name = name.split(" ")[0]
        data = os.popen(f"{aur_method} -Si {name}").read()
        data_list = []
        data_list = data.split("\n")
        clear_data = []
        for data in data_list:
            if data != "" and data != " " and data != "\n":
                clear_data.append(data.split(" : ")[1])       


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
        make_dependencies = clear_data[10]
        dependencies_control = clear_data[11]
        conflict = clear_data[12]
        replaces = clear_data[13]
        aur_url = clear_data[14]
        first_submit = clear_data[15]
        keywords = clear_data[16]
        last_modified = clear_data[17]
        packager = clear_data[18]
        popularity = clear_data[19]
        votes = clear_data[20]
        outdated = clear_data[21]

        # Etichette localizzate
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
        attribute_makeDependencies_label = pq.QLabel(lpak.get("make dependencies", language))
        attribute_dependenciesControl_label = pq.QLabel(lpak.get("dependencies control", language))
        attribute_conflict_label = pq.QLabel(lpak.get("conflict", language))
        attribute_replaces_label = pq.QLabel(lpak.get("replaces", language))
        attribute_aurUrl_label = pq.QLabel(lpak.get("aur url", language))
        attribute_firstSubmit_label = pq.QLabel(lpak.get("first submit", language))
        attribute_keywords_label = pq.QLabel(lpak.get("keywords", language))
        attribute_lastModified_label = pq.QLabel(lpak.get("last modified", language))
        attribute_packager_label = pq.QLabel(lpak.get("packager", language))
        attribute_popularity_label = pq.QLabel(lpak.get("popularity", language))
        attribute_votes_label = pq.QLabel(lpak.get("votes", language))
        attribute_outdated_label = pq.QLabel(lpak.get("outdated", language))
        
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
        attribute_makeDependencies_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_dependenciesControl_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_conflict_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_replaces_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_aurUrl_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_firstSubmit_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_keywords_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_lastModified_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_packager_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_popularity_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_votes_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")
        attribute_outdated_label.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")

        # Valori
        repo_label = pq.QLabel(repo)
        name_label = pq.QLabel(name)
        version_label = pq.QLabel(version)
        description_label = pq.QLabel(description)
        arch_label = pq.QLabel(arch)
        url_label = pq.QLabel(url)
        licenseType_label = pq.QLabel(license_type)
        group_label = pq.QLabel(group)
        provides_label = pq.QLabel(provides)
        dependencies_label = pq.QLabel(dependencies)
        makeDependencies_label = pq.QLabel(make_dependencies)
        dependenciesControl_label = pq.QLabel(dependencies_control)
        conflict_label = pq.QLabel(conflict)
        replaces_label = pq.QLabel(replaces)
        aurUrl_label = pq.QLabel(aur_url)
        firstSubmit_label = pq.QLabel(first_submit)
        keywords_label = pq.QLabel(keywords)
        lastModified_label = pq.QLabel(last_modified)
        packager_label = pq.QLabel(packager)
        popularity_label = pq.QLabel(popularity)
        votes_label = pq.QLabel(votes)
        outdated_label = pq.QLabel(outdated)

        # Funzione helper
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

        # Inserimento nel layout
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
        add_row(attribute_makeDependencies_label, makeDependencies_label)
        add_row(attribute_dependenciesControl_label, dependenciesControl_label)
        add_row(attribute_conflict_label, conflict_label)
        add_row(attribute_replaces_label, replaces_label)
        add_row(attribute_aurUrl_label, aurUrl_label)
        add_row(attribute_firstSubmit_label, firstSubmit_label)
        add_row(attribute_keywords_label, keywords_label)
        add_row(attribute_lastModified_label, lastModified_label)
        add_row(attribute_packager_label, packager_label)
        add_row(attribute_popularity_label, popularity_label)
        add_row(attribute_votes_label, votes_label)
        add_row(attribute_outdated_label, outdated_label)

        
    elif repo == "flathub":
        data = os.popen(f"flatpak remote-info flathub {name}").read()
        data_list = data.split("\n")
        clear_data = []
        for data in data_list:
            if ": " in data:       
                clear_data.append(data.split(": ")[1])
            elif "- " in data:    
                clear_data.append(data.split("- ")[0])
                clear_data.append(data.split("- ")[1])
        title = clear_data[0]  
        flatpak_id = clear_data[1]
        ref = clear_data[2]
        arch = clear_data[3]
        branch = clear_data[4]
        version = clear_data[5]
        license_type = clear_data[6]
        origin = clear_data[7]
        collection = clear_data[8]
        installation = clear_data[9]
        installed_size = clear_data[10]
        runtime = clear_data[11]
        sdk = clear_data[12]
        commit = clear_data[13]
        parent = clear_data[14]
        subject = clear_data[15]
        date = clear_data[16]

        attribute_title_label = pq.QLabel(lpak.get("name", language))
        attribute_id_label = pq.QLabel(lpak.get("id", language))
        attribute_ref_label = pq.QLabel(lpak.get("ref", language))
        attribute_arch_label = pq.QLabel(lpak.get("architecture", language))
        attribute_branch_label = pq.QLabel(lpak.get("branch", language))
        attribute_version_label = pq.QLabel(lpak.get("version", language))
        attribute_license_label = pq.QLabel(lpak.get("license", language))
        attribute_origin_label = pq.QLabel(lpak.get("origin", language))
        attribute_collection_label = pq.QLabel(lpak.get("collection", language))
        attribute_installation_label = pq.QLabel(lpak.get("download size", language))
        attribute_installedSize_label = pq.QLabel(lpak.get("installed size", language))
        attribute_runtime_label = pq.QLabel(lpak.get("runtime", language))
        attribute_sdk_label = pq.QLabel(lpak.get("sdk", language))
        attribute_commit_label = pq.QLabel(lpak.get("commit", language))
        attribute_parent_label = pq.QLabel(lpak.get("parent", language))
        attribute_subject_label = pq.QLabel(lpak.get("subject", language))
        attribute_date_label = pq.QLabel(lpak.get("date", language))

        for lbl in [
            attribute_title_label, attribute_id_label, attribute_ref_label,
            attribute_arch_label, attribute_branch_label, attribute_version_label,
            attribute_license_label, attribute_origin_label, attribute_collection_label,
            attribute_installation_label, attribute_installedSize_label, attribute_runtime_label,
            attribute_sdk_label, attribute_commit_label, attribute_parent_label,
            attribute_subject_label, attribute_date_label
        ]:
            lbl.setStyleSheet("color: #004080; font: bold 12pt 'Arial'")

        title_label = pq.QLabel(title)
        id_label = pq.QLabel(flatpak_id)
        ref_label = pq.QLabel(ref)
        arch_label = pq.QLabel(arch)
        branch_label = pq.QLabel(branch)
        version_label = pq.QLabel(version)
        license_label = pq.QLabel(license_type)
        origin_label = pq.QLabel(origin)
        collection_label = pq.QLabel(collection)
        installation_label = pq.QLabel(installation)
        installedSize_label = pq.QLabel(installed_size)
        runtime_label = pq.QLabel(runtime)
        sdk_label = pq.QLabel(sdk)
        commit_label = pq.QLabel(commit)
        parent_label = pq.QLabel(parent)
        subject_label = pq.QLabel(subject)
        date_label = pq.QLabel(date)

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

        add_row(attribute_title_label, title_label)
        add_row(attribute_id_label, id_label)
        add_row(attribute_ref_label, ref_label)
        add_row(attribute_arch_label, arch_label)
        add_row(attribute_branch_label, branch_label)
        add_row(attribute_version_label, version_label)
        add_row(attribute_license_label, license_label)
        add_row(attribute_origin_label, origin_label)
        add_row(attribute_collection_label, collection_label)
        add_row(attribute_installation_label, installation_label)
        add_row(attribute_installedSize_label, installedSize_label)
        add_row(attribute_runtime_label, runtime_label)
        add_row(attribute_sdk_label, sdk_label)
        add_row(attribute_commit_label, commit_label)
        add_row(attribute_parent_label, parent_label)
        add_row(attribute_subject_label, subject_label)
        add_row(attribute_date_label, date_label)

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

    print(clear_data)


        

    layout.setRowStretch(layout.rowCount(), 1)
    more_info_window.show()
