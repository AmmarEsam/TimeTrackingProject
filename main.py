import re
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QSizePolicy
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
import sys 
import json

session_number = 1

def read_file():
    with open("data.json", 'r') as f:
         data = json.load(f)
    return data

def write_file(data):
    with open("data.json", 'w') as file:
        json.dump(data, file)
    

class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)

        self.loginButton.clicked.connect(self.login)
        self.signUpButton.clicked.connect(self.signUp)
        self.errorTextLogin.setText("")
        self.errorTextSignUp.setText("")
        
    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def login(self): 
        try:
           data = read_file()
        except:
         self.errorTextLogin.setText("Account Not Found, please Sign Up")
        else:    
            self.user_emails = data.keys()
            self.login_email = self.emailInputLogin.text()
            
            if self.login_email =="" :
             self.errorTextLogin.setText("Email can not be empty!")
        
            elif self.login_email in self.user_emails:
             global user
             user = User(self.login_email)
             self.go_main_menu()
            else:
             self.errorTextLogin.setText("Account Not Found, please Sign Up")
        
    
    
    def  signUp(self):
        email = self.emailInputSignUp.text()
        name = self.nameInputSignUp.text()
        try:
          data = read_file()
          if not data:
              data = dict()
        except:
            data = {}
        if email =="" or name =="":
            self.errorTextSignUp.setText("Email/name can not be empty")
        elif email not in data.keys():
            new_user = {email: {"name": name,
                                     'recipients': [email],
                                     "projects": {}, }}
            data.update(new_user)
            write_file(data)
            self.emailInputSignUp.setText("")
            self.nameInputSignUp.setText("")
            self.errorTextSignUp.setText("Account created successfully!, please Login")
        else:
            self.errorTextSignUp.setText("Account already exist, please Login")



class User:
    def __init__(self, email):  
        data = read_file()
        self.data = data.get(email)
        self.email = email
        self.name = self.data.get('name')
        self.projects = self.data.get('projects')
        self.recipients = self.data.get('recipients')
        self.pomodoro = self.data.get('pomodoro')
        #self.tasks = self.data.get('task')
        
        
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
        self.error_subject_input=self.errorTextSubjectLabel
        self.addSubjectButton.clicked.connect(self.add_subject)
        self.selected_project_to_start = self.selectProjectCombo
        self.selected_subject_to_start = self.selectSubjectCombo
        self.startPomodoroButton.clicked.connect(self.go_to_pomodoro)
        self.selected_project_summary = self.showSummaryProjectCombo
        self.selected_subject_summary = self.showSummarySubjectCombo
        self.selected_period_summary = self.showSummaryPeriodCombo
        self.showSummaryButton.clicked.connect(self.show_summary)
        self.sendEmailThisSummaryButton.clicked.connect(self.send_email)
        self.total_tracked_time = self.totalTrackedTimeDurationLabel
        self.errorTextRecipientsEmailLabel.setText("")
        self.error_subject_input.setText("")
        self.error_project_input.setText("")
        for i in user.recipients:
            self.deleteRecipientCombo.addItem(i)
        for i in user.projects:
            self.selected_project_delete.addItem(i)
            self.selected_project_to_start.addItem(i)
            self.selected_project_summary.addItem(i)
            self.selected_project_for_subject.addItem(i)
            
        self.selected_project_delete.currentTextChanged.connect(
            self.on_change_select_subject_to_delete)
        self.selected_project_to_start.currentTextChanged.connect(
            self.on_change_select_subject_pomodoro)

    def on_change_select_subject_to_delete(self, value):
        if value == 'Select Project':
            self.selected_subject_delete.clear()
        else:
         self.selected_subject_delete.clear()
         self.data = read_file()
         subject=self.data[user.email]['projects'][value].keys()
         for i in subject:
             self.selected_subject_delete.addItem(i)

    def on_change_select_subject_pomodoro(self, value):
        if value == 'Select Project':
            self.selected_subject_to_start.clear()
        else:
         self.selected_subject_to_start.clear()
         self.data = read_file()
         subject = self.data[user.email]['projects'][value].keys()
         for i in subject:
             self.selected_subject_to_start.addItem(i)
         
    def add_recipients_email(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        recipient_email = self.recipients_email.text()
        if (re.fullmatch(regex, recipient_email)):

              self.data = read_file()
              
              if recipient_email in self.data[user.email]['recipients']:
                 self.error_recipient.setText("Email already exist")
              else:
                self.data[user.email]['recipients'].append(recipient_email)
                self.data.update()
                write_file(self.data)
                self.error_recipient.setText("Recipient email is saved")
                self.deleteRecipientCombo.addItem(recipient_email)
                self.recipients_email.setText("")
        else:
            self.error_recipient.setText("Invalid Email Format") 
        
     
          
    def delete_recipients_email(self):
            recipient_email = self.deleteRecipientCombo.currentText()
            self.data = read_file()
            self.data[user.email]['recipients'].remove(recipient_email)
            self.data.update()
            write_file(self.data)
            self.error_recipient.setText("Recipient email is deleted")
            self.deleteRecipientCombo.removeItem(
                 self.deleteRecipientCombo.currentIndex())
            
            
    def add_project(self):
        project_name = self.project_add.text()
        self.data = read_file()
        if project_name =="":
           self.error_project_input.setText("Project can't be empty")
        
        elif project_name in self.data[user.email]['projects']:
            self.error_project_input.setText("Project already exist")
        else:
           
            self.data[user.email]['projects'][project_name]={}
            self.data.update()
            write_file(self.data)
            self.error_project_input.setText("Project is added")
            self.project_add.setText("")
            self.selected_project_delete.addItem(project_name)
            self.selected_project_to_start.addItem(project_name)
            self.selected_project_summary.addItem(project_name)
            self.selected_project_for_subject.addItem(project_name)
        
    def delete_project(self):
       project_name = self.selected_project_delete.currentText()
       project_index = self.selected_project_delete.currentIndex()
       if project_index == 0:
          print ("No project found")
       else:
        self.data = read_file()
        self.data[user.email]['projects'].pop(project_name)
        self.data.update()
        write_file(self.data)
        self.selected_project_delete.removeItem(
            self.selected_project_delete.currentIndex())
        self.selected_project_to_start.removeItem(project_index)
        self.selected_project_summary.removeItem(project_index)   
        self.selected_project_for_subject.removeItem(project_index)
       
    def add_subject(self):
        project=self.selected_project_for_subject.currentText()
        subject = self.subject_add.text()
        index = self.selected_project_for_subject.currentIndex()
        self.data = read_file()
        if index == 0:
            self.error_subject_input.setText("Select project First")
        elif subject =="":
            self.error_subject_input.setText("Subject can't be empty")
        else:
            self.data[user.email]['projects'][project][subject] = {}
            self.data.update()
            write_file(self.data)
            self.error_subject_input.setText("Subject is added")
            self.subject_add.setText("")
            self.selected_project_delete.setCurrentIndex(0)
            self.selected_project_to_start.setCurrentIndex(0)
           
            
            
    def delete_subject(self):
        project_name = self.selected_project_delete.currentText()
        project_index =self.selected_project_delete.currentIndex()
        subject = self.selected_subject_delete.currentText()
        if subject == '' or project_index == 0:
            print("No subject found")
        else:
            self.data = read_file()
            self.data[user.email]['projects'][project_name].pop(subject)
            self.data.update()
            write_file(self.data)
            self.selected_subject_delete.removeItem(
                self.selected_subject_delete.currentIndex())
  
  
    def go_to_pomodoro(self):
        pomodoro_screen = PomodoroUI(self.selectProjectCombo.currentText(),self.selectSubjectCombo.currentText())
        widget.addWidget(pomodoro_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def show_summary():
        pass
    def send_email():
        pass
    def calculate_total_tracked_time():
        pass
    
    


class PomodoroUI(QDialog):
    global session_number
    session_number =1
    
    def __init__(self,*args):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)
        self.selected_project = args[0]
        self.selected_subject = args[1]
        self.task_name = self.taskInput
        self.remaining_time = 1501
        self.timer = QTimer(self)
        
        self.goToMainMenuButton.clicked.connect(self.go_main_menu)
        self.addTask.clicked.connect(self.add_task)
        self.timer.timeout.connect(self.update_time_counter)
        self.startStopButton.clicked.connect(self.time_counter) 
        self.doneButton.clicked.connect(self.end_session) 
        self.labelAsNotFinishedButton.clicked.connect(self.accomplished_task)
        
        self.data = read_file()
        self.display_session_num()
        # for i in user.tasks:
        #  self.tasksCombo.addItem(i)
    def display_session_num(self):
       
        self.numberOfSession.setText(str(session_number))
        
    def add_task(self):
        if self.task_name.text() == " " or self.task_name.text() =="Task can't be empty":
           self.task_name.setText("Task can't be empty")
        
        else:
          try:
           self.data[user.email]['projects'][ self.selected_project][self.selected_subject]['pomodoro']
           
          except:
              self.data[user.email]['projects'][ self.selected_project][self.selected_subject]['pomodoro']={}
              self.data[user.email]['projects'][ self.selected_project][self.selected_subject]['pomodoro'][f'session{session_number}'] = {'task':{}}

          else:    
              try:
                  self.data[user.email]['projects'][ self.selected_project][self.selected_subject]['pomodoro'][f'session{session_number}']['task']
              except:
                     self.data[user.email]['projects'][ self.selected_project][self.selected_subject]['pomodoro'][f'session{session_number}'] = {'task':{}}
        
          finally:
              
              self.data[user.email]['projects'][ self.selected_project][self.selected_subject]['pomodoro'][f'session{session_number}']['task'][self.task_name.text()]=''
              self.data.update()
              write_file(self.data)
              self.tasksCombo.addItem(self.task_name.text())
              self.task_name.setText(" ")
         
       
    def time_counter(self):
        if self.tasksCombo.currentText()!=" " or self.tasksCombo.currentText()!= "choose task first":
           self.timer.start(self.remaining_time)
        else:
            self.tasksCombo.setText('choose task first')


    def update_time_counter(self):
        self.remaining_time -= 1
        minutes, seconds = divmod(self.remaining_time,60)
        self.timeLabel.setText("{:02d}:{:02d}".format(minutes, seconds))
        
        if self.remaining_time <= 0:
            self.timer.stop()
            self.end_session()


    def start_session():
        pass
    def end_session(self):
        global session_number 
        if session_number !=4 or self.doneButton.clicked:
                session_number+=1           
                shortBreak = ShortBreakUI()
                widget.addWidget(shortBreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
                                                                  

    def accomplished_task(self):
        pass
    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

#class ShortBreakUI(QDialog):
    #def __init__(self):
     #   super(ShortBreakUI,self).__init__()
     #  loadUi("./UI/shortBreak.ui",self)
    
   # def time_counter():
   #     pass
   # def start_timer():
   #     pass
   # def pause_timer():
   #     pass
  #  def skip_break():
    #    pass

class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI, self).__init__()
        loadUi('ui/shortBreak.ui', self)
        self.setWindowTitle('Short Break')
        
        self.remaining_time = 300  # 5 minutes in seconds   
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
        self.startButton.clicked.connect(self.start_timer)
        self.skipButton.clicked.connect(self.skip_break)
        self.goToMainMenuButton.clicked.connect(self.go_to_main_menu)
        
        self.startButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.skipButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.update_time()
        
    def update_time(self):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timeLabel.setText("{:02d}:{:02d}".format(minutes, seconds))
        
        if self.remaining_time <= 0:
            self.timer.stop()
            # pmodoro = PomodoroUI()
            # widget.addWidget(pmodoro)
            # widget.setCurrentIndex(widget.currentIndex()+1)
            self.done(0)
            
    def start_timer(self):
        self.timer.start(1000)
        
    def skip_break(self):
        self.done(1)
        
    def go_to_main_menu(self):
        self.done(2)

#class LongBreakUI(QDialog):
   # def __init__(self):
     #   super(LongBreakUI,self).__init__()
     #   loadUi("./UI/longBreak.ui",self)
        
  #  def time_counter():
   #     pass
  #  def start_timer():
   #     pass
  #  def pause_timer():
   #     pass
  #  def skip_break():
   #     pass

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI, self).__init__()
        loadUi('ui/longBreak.ui', self)
        self.setWindowTitle('Long Break')

        self.remaining_time = 900  # 15 minutes in seconds   
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
        self.startButton.clicked.connect(self.start_timer)
        self.skipButton.clicked.connect(self.skip_timer)
        self.goToMainMenuButton.clicked.connect(self.go_to_main_menu)
        
        self.startButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.skipButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.update_time()
        
    def update_time(self):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timeLabel.setText("{:02d}:{:02d}".format(minutes, seconds))
        
        if self.remaining_time <= 0:
            self.timer.stop()
            self.done(0)
            
    def start_timer(self):
        self.timer.start(1000)
        
    def skip_timer(self):
        self.done(1)
        
    def go_to_main_menu(self):
        self.done(2)

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
