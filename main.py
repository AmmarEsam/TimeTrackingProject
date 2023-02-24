import re
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys



class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)

        self.loginButton.clicked.connect(self.login)
        self.signUpButton.clicked.connect(self.signUp)


    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def login(self):
        login_email = self.emailInputLogin.text()
        self.errorTextLogin.setText("")
        #self.go_main_menu()
    
    def signUp(self):
        sign_up_email = self.emailInputSignUp.text()
        sign_up_name = self.nameInputSignUp.text()
        self.errorTextSignUp.setText("")
        #self.go_main_menu()




class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)
        self.recipients_email = self.addRecipientInput
        self.error_recipient = self.errorTextRecipientsEmailLabel
        self.addRecipientButton.clicked.connect(self.add_recipients_email)
        self.selected_recipient_delete = self.deleteRecipientCombo
        self.deleteRecipientButton.clicked.connect(self.delete_recipients_email)
        self.selected_project_delete = self.projectDeleteCombo
        self.projectDeleteButton.clicked.connect(self.delete_project)
        self.selected_subject_delete = self.subjectDeleteCombo
        self.subjectDeleteButton.clicked.connect(self.delete_subject)
        self.project_add = self.addProjectInput
        self.error_project_input = self.errorTextProjectLabel
        self.addProjectButton.clicked.connect(self.add_project)
        self.subject_add = self.addSubjectInput
        self.selected_project_for_subject = self.addSubjectOnProjectCombo
        self.error_project_input=self.errorTextSubjectLabel
        self.addSubjectButton.clicked.connect(self.add_subject)
        self.selected_project_to_start = self.selectProjectCombo
        self.selected_subject_to_start = self.selectSubjectCombo
        self.startPomodoroButton.clicked.connect(self.start_pomodoro)
        self.selected_project_summary = self.showSummaryProjectCombo
        self.selected_subject_summary = self.showSummarySubjectCombo
        self.selected_period_summary = self.showSummaryPeriodCombo
        self.showSummaryButton.clicked.connect(self.show_summary)
        self.sendEmailThisSummaryButton.clicked.connect(self.send_email)
        self.total_tracked_time = self.totalTrackedTimeDurationLabel

        
    def add_recipients_email(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if(re.fullmatch(regex, self.recipients_email.text())):
           self.error_recipient.setText("Recipient email is saved")
           with open ('recipient.txt', 'a') as f:
               f.write(self.recipients_email.text())
               f.write('\n')
               self.deleteRecipientCombo.addItem(self.recipients_email.text())
        else:
            self.error_recipient.setText("Invalid")
    def delete_recipients_email(self):
         with open ('recipient.txt') as f:
               emails=f.readlines()
         with open ('recipient.txt','w') as f:
               for email in emails:
                   if (self.selected_recipient_delete.currentText()!= email.strip()):
                       f.write(email)
                    
    def add_project(self):
        with open ('project.txt', 'a') as f:
               f.write(self.project_add.text())
               f.write('\n')
               self.projectDeleteCombo.addItem(self.project_add.text())
    def delete_project(self):
        with open ('project.txt') as f:
               projects=f.readlines()
        with open ('project.txt','w') as f:
               for project in projects:
                   if (self.projectDeleteCombo.currentText()!= project.strip()):
                       f.write(project)
    def add_subject(self):
        with open ('subject.txt', 'a') as f:
               f.write(self.subject_add.text())
               f.write('\n')
               self.subjectDeleteCombo.addItem(self.subject_add.text())
    def delete_subject(self):
        with open ('subject.txt') as f:
               subjects=f.readlines()
        with open ('subject.txt','w') as f:
               for subject in subjects:
                   if (self.subjectDeleteCombo.currentText()!= subject.strip()):
                       f.write(subject)
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
