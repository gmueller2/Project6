from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from model.exceptions import DuplicateEmail
from model.league_database import LeagueDatabase
from model.team_member import TeamMember

Ui_MainWindow, QtBaseWindow = uic.loadUiType('team_editor_dialog.ui')


def no_item_selected_error():
    dialog = QMessageBox(QMessageBox.Icon.Warning,
                         "Error",
                         "You need to select an item from the list first!",
                         QMessageBox.StandardButton.Ok)
    dialog.exec()


def blank_text_error():
    dialog = QMessageBox(QMessageBox.Icon.Warning,
                         "Error",
                         "Please enter a value for the name or email!",
                         QMessageBox.StandardButton.Ok)
    dialog.exec()

def duplicate_email_error():
    dialog = QMessageBox(QMessageBox.Icon.Warning,
                         "Error",
                         "Please enter a unique value for the email!",
                         QMessageBox.StandardButton.Ok)
    dialog.exec()


class TeamEditDialog(QtBaseWindow, Ui_MainWindow):

    def __init__(self, team=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._team = team
        if team:
            self.update_ui()
        self.delete_player_button.clicked.connect(self.delete_button_clicked)
        self.edit_player_button.clicked.connect(self.edit_button_clicked)
        self.add_player_button.clicked.connect(self.add_button_clicked)
        self.player_list_widget.itemClicked.connect(self.player_select)
        self.setWindowTitle(f"Editing Team: {self._team.name}")

    def update_ui(self):
        self.player_list_widget.clear()
        for player in self._team.members:
            self.player_list_widget.addItem(f'{player.name}')

    def delete_button_clicked(self):
        if len(self.player_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        item_name = self.player_list_widget.currentItem().text()
        selected_player = self._team.member_named(item_name)
        self._team.remove_member(selected_player)
        self.update_ui()

    def edit_button_clicked(self):
        if len(self.player_list_widget.selectedItems()) == 0:
            no_item_selected_error()
            return None
        edit_line_name = self.line_edit_player_name.text()
        edit_line_email = self.line_edit_player_email.text()
        if len(edit_line_name) == 0 or len(edit_line_email) == 0:
            blank_text_error()
            return None
        item_name = self.player_list_widget.currentItem().text()
        selected_player = self._team.member_named(item_name)

        if selected_player.name != edit_line_name:
            selected_player.name = edit_line_name
        if selected_player.email != edit_line_email:
            selected_player.email = edit_line_email
        self.update_ui()

    def add_button_clicked(self):
        ldb = LeagueDatabase.instance()
        name_to_add = self.line_edit_player_name.text()
        email_to_add = self.line_edit_player_email.text()
        if len(name_to_add) == 0 or len(email_to_add) == 0:
            blank_text_error()
            return None
        new_player = TeamMember(ldb.next_oid(), name_to_add, email_to_add)
        try:
            self._team.add_member(new_player)
        except DuplicateEmail:
            duplicate_email_error()
        self.update_ui()

    def player_select(self):
        item_name = self.player_list_widget.currentItem().text()
        selected_player = self._team.member_named(item_name)
        self.line_edit_player_name.setText(selected_player.name)
        self.line_edit_player_email.setText(selected_player.email)



