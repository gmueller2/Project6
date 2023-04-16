from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from model.league_database import LeagueDatabase
from model.league import League
import sys

from ui.league_editor_dialog import LeagueEditDialog

Ui_LeagueWindow, QtBaseWindow = uic.loadUiType("league_db_window.ui")


def no_item_selected_error():
    dialog = QMessageBox(QMessageBox.Icon.Warning,
                         "Error",
                         "You need to select an item from the list first!",
                         QMessageBox.StandardButton.Ok)
    dialog.exec()


def blank_text_error():
    dialog = QMessageBox(QMessageBox.Icon.Warning,
                         "Error",
                         "Please enter a value for the name!",
                         QMessageBox.StandardButton.Ok)
    dialog.exec()


def unique_name_error():
    dialog = QMessageBox(QMessageBox.Icon.Warning,
                         "Error",
                         "Name must be unique!",
                         QMessageBox.StandardButton.Ok)
    dialog.exec()


class LeagueWindow(QtBaseWindow, Ui_LeagueWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.edit_league_button.clicked.connect(self.edit_button_clicked)
        self.delete_league_button.clicked.connect(self.delete_button_clicked)
        self.add_league_button.clicked.connect(self.add_button_clicked)
        self.import_league_button.clicked.connect(self.import_button_clicked)
        self.export_league_button.clicked.connect(self.export_button_clicked)
        self.action_save.triggered.connect(self.save_button_clicked)
        self.action_load.triggered.connect(self.load_button_clicked)
        self.setWindowTitle("League Database Manager")

    def update_ui(self):
        ldb = LeagueDatabase.instance()
        self.league_list_widget.clear()
        for league in ldb.leagues:
            self.league_list_widget.addItem(f'{league.name}')

    def edit_button_clicked(self):
        ldb = LeagueDatabase.instance()
        if len(self.league_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        item_name = self.league_list_widget.currentItem().text()
        selected_league = ldb.league_named(item_name)
        dialog = LeagueEditDialog(league=selected_league)
        dialog.exec()

    def delete_button_clicked(self):
        ldb = LeagueDatabase.instance()
        if len(self.league_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        item_name = self.league_list_widget.currentItem().text()
        print(f'Removing {item_name}')
        selected_league = ldb.league_named(item_name)
        ldb.remove_league(selected_league)
        self.update_ui()

    def add_button_clicked(self):
        name_to_add = self.line_edit_league_name.text()
        if len(name_to_add) == 0:
            blank_text_error()
            return None
        ldb = LeagueDatabase.instance()
        items_in_list = [league.name for league in ldb.leagues]
        if name_to_add in items_in_list:
            unique_name_error()
            return None
        print(f'Adding League: {name_to_add}')
        new_league = League(ldb.next_oid(), name_to_add)
        ldb.add_league(new_league)
        self.update_ui()

    def import_button_clicked(self):
        # get the league instance and league name
        ldb = LeagueDatabase.instance()
        if len(self.league_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        name_to_import = self.league_list_widget.currentItem().text()
        # get the league object
        league_to_import = ldb.league_named(name_to_import)
        # get the file path
        filename = QFileDialog.getOpenFileName(self, 'Import League Teams', 'c:\\', "CSV Files (*.csv)")
        # import the teams (filename is tuple!)
        if filename[0] == '':
            return None
        else:
            ldb.import_league_teams(league_to_import, filename[0])

    def export_button_clicked(self):
        # get the league instance and league name
        ldb = LeagueDatabase.instance()
        if len(self.league_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        name_to_export = self.league_list_widget.currentItem().text()
        # get the league object
        league_to_export = ldb.league_named(name_to_export)
        # get the save file path
        filename = QFileDialog.getSaveFileName(self, 'Export League Teams', 'c:\\', "CSV Files (*.csv)")
        # export the teams (filename is tuple!)
        if filename[0] == '':
            return None
        else:
            ldb.export_league_teams(league_to_export, filename[0])

    def save_button_clicked(self):
        # get the league instance
        ldb = LeagueDatabase.instance()
        # get the save file path
        filename = QFileDialog.getSaveFileName(self, 'Save League Database', 'c:\\', "League Files (*.league "
                                                                                     "*league.backup)")
        if filename[0] == '':  # just in case they cancel
            return None
        else:
            ldb.save(filename[0])

    def load_button_clicked(self):
        # get the league instance
        ldb = LeagueDatabase.instance()
        # get the load file path
        filename = QFileDialog.getOpenFileName(self, 'Load League Database', 'c:\\', "League Files (*.league "
                                                                                     "*league.backup)")
        if filename[0] == '':  # just in case they cancel
            return None
        else:
            ldb.load(filename[0])
        self.update_ui()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueWindow()
    window.show()
    sys.exit(app.exec())
