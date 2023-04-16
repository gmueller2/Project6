from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from model.league_database import LeagueDatabase
from model.team import Team
from ui.team_editor_dialog import TeamEditDialog

Ui_MainWindow, QtBaseWindow = uic.loadUiType('league_editor_dialog.ui')


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


class LeagueEditDialog(QtBaseWindow, Ui_MainWindow):

    def __init__(self, league=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._league = league
        if league:
            self.update_ui()
        self.edit_team_button.clicked.connect(self.edit_button_clicked)
        self.delete_team_button.clicked.connect(self.delete_button_clicked)
        self.add_team_button.clicked.connect(self.add_button_clicked)
        self.import_teams_button.clicked.connect(self.import_button_clicked)
        self.export_teams_button.clicked.connect(self.export_button_clicked)
        self.setWindowTitle(f"Editing League: {self._league.name}")

    def update_ui(self):
        self.team_list_widget.clear()
        for team in self._league.teams:
            self.team_list_widget.addItem(f'{team.name}')

    def edit_button_clicked(self):
        if len(self.team_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        item_name = self.team_list_widget.currentItem().text()
        selected_team = self._league.team_named(item_name)
        dialog = TeamEditDialog(team=selected_team)
        dialog.exec()

    def delete_button_clicked(self):
        if len(self.team_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        item_name = self.team_list_widget.currentItem().text()
        selected_team = self._league.team_named(item_name)
        self._league.remove_team(selected_team)
        self.update_ui()

    def add_button_clicked(self):
        name_to_add = self.line_edit_team_name.text()
        if len(name_to_add) == 0:
            blank_text_error()
            return None
        items_in_list = [team.name for team in self._league.teams]
        if name_to_add in items_in_list:
            unique_name_error()
            return None
        ldb = LeagueDatabase.instance()  # for the oid generator
        print(f'Adding Team: {name_to_add}')
        new_team = Team(ldb.next_oid(), name_to_add)
        self._league.add_team(new_team)
        self.update_ui()

    def import_button_clicked(self):
        # get league database instance
        ldb = LeagueDatabase.instance()
        # get the league object
        league_to_import = self._league
        # get the file path
        filename = QFileDialog.getOpenFileName(self, 'Import League Teams', 'c:\\', "CSV Files (*.csv)")
        # import the teams (filename is tuple!)
        if filename[0] == '':
            pass
        else:
            ldb.import_league_teams(league_to_import, filename[0])
        self.update_ui()

    def export_button_clicked(self):
        # get the league database instance
        ldb = LeagueDatabase.instance()
        # get the league object
        league_to_export = self._league
        # get the save file path
        filename = QFileDialog.getSaveFileName(self, 'Export League Teams', 'c:\\', "CSV Files (*.csv)")
        # export the teams (filename is tuple!)
        if filename[0] == '':
            pass
        else:
            ldb.export_league_teams(league_to_export, filename[0])




