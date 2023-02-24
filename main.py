from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys



class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)

        # This is example of changing screen
        self.loginButton.clicked.connect(self.go_main_menu)

    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def login():
        pass
    
    def signUp():
        pass




class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)
        recipients_email = self.addRecipientInput.text()
        error_recipient = self.errorTextRecipientsEmailLabel
        self.addRecipientButton.clicked.connect(self.add_recipients_email)
        selected_recipient_delete = self.deleteRecipientCombo.text()
        self.deleteRecipientButton.clicked.connect(self.delete_recipients_email)
        selected_project_delete = self.projectDeleteCombo.text()
        self.projectDeleteButton.clicked.connect(self.delete_project)
        selected_subject_delete = self.subjectDeleteCombo.text()
        self.subjectDeleteButton.clicked.connect(self.delete_subject)
        project_add = self.addProjectInput.text()
        error_project_input = self.errorTextProjectLabel
        self.addProjectButton.clicked.connect(self.add_project)
        subject_add = self.addSubjectInput.text()
        selected_project_for_subject = self.addSubjectOnProjectCombo.text()
        error_project_input=self.errorTextSubjectLabel
        self.addSubjectButton.clicked.connect(self.add_subject)
        selected_project_to_start = self.selectProjectCombo.text()
        selected_subject_to_start = self.selectSubjectCombo.text()
        self.startPomodoroButton.clicked.connect(self.start_pomodoro)
        selected_project_summary = self.showSummaryProjectCombo.text()
        selected_subject_summary = self.showSummarySubjectCombo.text()
        selected_period_summary = self.showSummaryPeriodCombo.text()
        self.showSummaryButton.clicked.connect(self.show_summary)
        self.sendEmailThisSummaryButton.clicked.connect(self.send_email)
        total_tracked_time = self.totalTrackedTimeDurationLabel

        
    def add_recipients_email():
        pass
    def delete_recipients_email():
        pass
    def add_project():
        pass
    def delete_project():
        pass
    def add_subject():
        pass
    def delete_subject():
        pass
    def select_project():
        pass
    def select_subject():
        pass
    def start_pomodoro():
        pass
    def show_summary():
        pass
    def send_email():
        pass
    def calculate_total_tracked_time():
        pass
    
    
    

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)
  
    def display_session_num():
        pass
    def add_task():
        pass
    def time_counter():
        pass
    def start_session():
        pass
    def end_session():
        pass
    def accomplished_task():
        pass
    


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)
    
    def time_counter():
        pass
    def start_timer():
        pass
    def pause_timer():
        pass
    def skip_break():
        pass
    
    

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)
        
    def time_counter():
        pass
    def start_timer():
        pass
    def pause_timer():
        pass
    def skip_break():
        pass

app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    # UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
