import PyQt6.QtWidgets as pq
def show_allert(title, message):
    msg = pq.QMessageBox()
    msg.setIcon(pq.QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setStandardButtons(pq.QMessageBox.StandardButton.Ok | pq.QMessageBox.StandardButton.Cancel)
    retval = msg.exec()