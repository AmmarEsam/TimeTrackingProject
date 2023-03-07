import re
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QSizePolicy
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from datetime import date
import datetime
import sys
import json
import os
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import vlc

def read_file():
    with open("data.json", 'r') as f:
        data = json.load(f)
    return data


def write_file(data):
    with open("data.json", 'w') as file:
        json.dump(data, file)


class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI, self).__init__()
        loadUi("./UI/login.ui", self)

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

            if self.login_email == "":
             self.errorTextLogin.setText("Email can not be empty!")

            elif self.login_email in self.user_emails:
             global user
             user = User(self.login_email)
             self.go_main_menu()
            else:
             self.errorTextLogin.setText("Account Not Found, please Sign Up")

    def signUp(self):
        email = self.emailInputSignUp.text()
        name = self.nameInputSignUp.text()
        try:
          data = read_file()
          if not data:
              data = dict()
        except:
            data = {}
        if email == "" or name == "":
            self.errorTextSignUp.setText("Email/name can not be empty")
        elif email not in data.keys():
            new_user = {email: {"name": name,
                                'recipients': [email],
                                "projects": {}, }}
            data.update(new_user)
            write_file(data)
            self.emailInputSignUp.setText("")
            self.nameInputSignUp.setText("")
            self.errorTextSignUp.setText(
                "Account created successfully!, please Login")
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


class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI, self).__init__()
        loadUi("./UI/mainMenu.ui", self)
        self.recipients_email = self.addRecipientInput
        self.error_recipient = self.errorTextRecipientsEmailLabel
        self.addRecipientButton.clicked.connect(self.add_recipients_email)
        self.selected_recipient_delete = self.deleteRecipientCombo
        self.deleteRecipientButton.clicked.connect(
            self.delete_recipients_email)
        self.selected_project_delete = self.projectDeleteCombo
        self.projectDeleteButton.clicked.connect(self.delete_project)
        self.selected_subject_delete = self.subjectDeleteCombo
        self.subjectDeleteButton.clicked.connect(self.delete_subject)
        self.project_add = self.addProjectInput
        self.error_project_input = self.errorTextProjectLabel
        self.addProjectButton.clicked.connect(self.add_project)
        self.subject_add = self.addSubjectInput
        self.selected_project_for_subject = self.addSubjectOnProjectCombo
        self.error_subject_input = self.errorTextSubjectLabel
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
        self.total_tracked_time.setText("00:00")
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
        self.selected_project_summary.currentTextChanged.connect(
            self.on_change_select_subject_summary)
        self.titleWorkspaceLabel.setText(user.name.capitalize()+"'s Workspace")
        

    def on_change_select_subject_to_delete(self, value):
        if value == 'Select Project':
            self.selected_subject_delete.clear()
        else:
         self.selected_subject_delete.clear()
         self.data = read_file()
         subject = self.data[user.email]['projects'][value].keys()
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

    def on_change_select_subject_summary(self, value):
        if value == 'All':
            self.selected_subject_summary.clear()
            self.selected_subject_summary.addItem('All')
        else:
         self.selected_subject_summary.clear()
         self.data = read_file()
         subject = self.data[user.email]['projects'][value].keys()
         for i in subject:
             self.selected_subject_summary.addItem(i)

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
        if project_name == "":
           self.error_project_input.setText("Project can't be empty")

        elif project_name in self.data[user.email]['projects']:
            self.error_project_input.setText("Project already exist")
        else:

            self.data[user.email]['projects'][project_name] = {}
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
          print("No project found")
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
        project = self.selected_project_for_subject.currentText()
        subject = self.subject_add.text()
        index = self.selected_project_for_subject.currentIndex()
        self.data = read_file()
        if index == 0:
            self.error_subject_input.setText("Select project First")
        elif subject == "":
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
        project_index = self.selected_project_delete.currentIndex()
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

    def start_pomodoro(self):
        project_name = self.selected_project_to_start.currentText()
        subject_name = self.selected_subject_to_start.currentText()
        if subject_name!="":
            #self.data = read_file()
            #self.data[user.email]['projects'][project_name][subject_name] = {
             #   'session1': {}, 'session2': {}, 'session3': {}, 'session4': {}}
            #self.data.update()
            #write_file(self.data)
            pomodoro = PomodoroUI(project_name, subject_name)
            widget.addWidget(pomodoro)
            widget.setCurrentIndex(widget.currentIndex()+1)
    

    def show_summary(self):
        global row
        row = {}
        self.project = self.selected_project_summary
        self.subject = self.selected_subject_summary
        self.period = self.selected_period_summary
        self.data = read_file()
        projects = self.data[user.email]['projects'].keys()
        for i in reversed(range(self.summaryTableValuesWidget.rowCount())):
         self.summaryTableValuesWidget.removeRow(i)

        if self.project.currentText() == "All":
            if self.subject.currentText() == "All":

              self.all_selected(projects, self.period.currentText())
            else:
               pass
                # self.specific_project_all_subject()
        else:
            if self.subject.currentText() != "All":
                self.specific_subject_project(self.project.currentText(
                ), self.subject.currentText(), self.period.currentText())
            else:
                pass


    def total_hrs(self,start,end):
       
        #self.data = read_file()
        if start ==0 and end ==0:
            calc_hr = 0
            calc_min = 0
        else:
          calc_start = start.split(':')
          calc_end = end.split(':')
          calc_hr =   int(calc_end[0]) - int(calc_start[0])
          calc_min = int(calc_end[1]) - int(calc_start[1])
        return calc_hr,calc_min
                 
        
    def specific_project_all_subject():
        pass
    def specific_subject_project(self,project,subject,period):
        c = 0
        total_hr=0
        total_min=0
        sessions = self.data[user.email]['projects'][project][subject].keys()
        for k in sessions:
            if period == 'All':
               start,end = self.all_days(project,subject,k,c)
            elif period == 'Today':
                start,end = self.today(project,subject,k,c)
            elif period == 'This week':
                start,end = self.this_week(project,subject,k,c)
            else:
                start,end = self.this_month(project,subject,k,c)
            if start!=0 and end != 0:
                c+=1
            calc_hr, calc_min = self.total_hrs(start,end)
            total_hr += calc_hr
            total_min += calc_min
        self.total_tracked_time.setText(str(total_hr)+':'+str(total_min))
    def all_selected (self,projects,period):
        c = 0
        total_hr=0
        total_min=0
        for i in projects:
            subjects = self.data[user.email]['projects'][i].keys()
            
            for j in subjects:
                sessions = self.data[user.email]['projects'][i][j].keys()
                for k in sessions:
                 if period == 'All':
                   start,end = self.all_days(i,j,k,c)
                 elif period == 'Today':
                    start,end = self.today(i,j,k,c)
                 elif period == 'This week':
                     start,end = self.this_week(i,j,k,c)
                 else:
                    start,end = self.this_month(i,j,k,c)
                 if start!=0 and end != 0:
                    c+=1
                 
                 calc_hr, calc_min = self.total_hrs(start,end)
                 total_hr += calc_hr
                 total_min += calc_min         
        self.total_tracked_time.setText(str(total_hr)+':'+str(total_min))
                 

                 
    def  all_days(self,project,subject,session,c):
        dates = self.data[user.email]['projects'][project][subject][session]['date']
        start,end = self.table_attributes(project,subject,session,c,dates)
        return start, end
    def today(self,project,subject,session,c):
        dates = self.data[user.email]['projects'][project][subject][session]['date']
         
        if dates == str(date.today()):
           start,end = self.table_attributes(project,subject,session,c,dates)
        else:  
            start = 0
            end = 0
        return start, end
        
            

    def this_week(self,project,subject,session,c):
        dates = self.data[user.email]['projects'][project][subject][session]['date'] 
        if str(date.today() - datetime.timedelta(days = 7))<= dates <= str(date.today()) :
           start,end = self.table_attributes(project,subject,session,c,dates)
        else:  
            start = 0
            end = 0
        return start, end
    def this_month(self,project,subject,session,c):
        dates = self.data[user.email]['projects'][project][subject][session]['date'] 
        if str(date.today() - datetime.timedelta(days =30))<= dates <= str(date.today()) :
           start,end = self.table_attributes(project,subject,session,c,dates)
        else:  
            start = 0
            end = 0
        return start, end
                 
    def table(self,dates,start,end,success,fail,c):
                 row.update(
                        {f'row'+str(c): [dates, start, end, success, fail]})
                 rowPosition = self.summaryTableValuesWidget.rowCount()
                 self.summaryTableValuesWidget.insertRow(c)
                 self.summaryTableValuesWidget.setItem(
                     rowPosition, 0, QTableWidgetItem(dates))
                 self.summaryTableValuesWidget.setItem(
                     rowPosition, 1, QTableWidgetItem(start))
                 self.summaryTableValuesWidget.setItem(
                     rowPosition, 2, QTableWidgetItem(end))
                 if success != "":
                  self.summaryTableValuesWidget.setItem(
                     rowPosition, 3, QTableWidgetItem(str(success)))
                 else:
                     self.summaryTableValuesWidget.setItem(
                         rowPosition, 3, QTableWidgetItem('None'))
                 if fail!="":
                  self.summaryTableValuesWidget.setItem(
                     rowPosition, 4, QTableWidgetItem(str(fail)))
                 else:
                     self.summaryTableValuesWidget.setItem(
                         rowPosition, 4, QTableWidgetItem('None'))
    def table_attributes(self,project,subject,session,c,dates):
           
        start = self.data[user.email]['projects'][project][subject][session]['start']
        end = self.data[user.email]['projects'][project][subject][session]['end']
        success_task = self.data[user.email]['projects'][project][subject][session]['tasks']['success']
        success_task = ','.join(success_task)
        fail_task = self.data[user.email]['projects'][project][subject][session]['tasks']['fail']
        fail_task = ','.join(fail_task)
        self.table(dates,start,end,success_task,fail_task,c)
        return start, end

    def send_email(self):
        global row
        recipient_email = self.deleteRecipientCombo.currentText()
        self.email_sender = 'fenyxclass8@gmail.com'
        self.email_password = 'ncdt hlwf pdkz couj'
        self.email_receiver = recipient_email

        self.connection = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.connection.login(self.email_sender, self.email_password)
        self.message = MIMEMultipart("alternatives")
        self.message['Subject'] = 'Summary Of Pomodoro'
        self.message['From'] = self.email_sender
        self.message['To'] = self.email_receiver

        
        self.html = """
         <!DOCTYPE html>
                <html>
                <head>
                <style>
                table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                }
                </style>
                </head>
                <body>
                <h2>Summary Of Pomodoro</h2>
                <p></p>
                <table style="width:100%">
                <tr>
                    <th>Date</th>
                    <th>Starting Time</th> 
                    <th>End Time</th>
                    <th>Success(Tasks)</th>
                    <th>Failure(Tasks)</th>
                </tr>
                    """ 
        for i in row.values():
            self.html += '<tr>'
            for j in i:
               self.html += '<td>'+j+'</td>'
            '</tr>'
        self.html+="""
                </table>
                </body>
                </html>"""

        self.htmlPart = MIMEText(self.html, 'html')
        self.message.attach(self.htmlPart)
        self.connection.sendmail(
            self.email_sender, self.email_receiver, self.message.as_string())
        self.connection.quit()



class PomodoroUI(QDialog):
    global session_number
    session_number = 1

    def __init__(self, project_name, subject_name):
        super(PomodoroUI, self).__init__()
        loadUi("./UI/pomodoro.ui", self)
        self.goToMainMenuButton.clicked.connect(self.go_main_menu)
        self.addTask.clicked.connect(self.add_task)
        self.remaining_time = 1501
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_counter)
        self.resetButton.clicked.connect(self.reset_timer) 
        self.startStopButton.clicked.connect(self.time_counter)
        self.startStopButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.update_time_counter()
        self.doneButton.clicked.connect(self.end_session)
        self.labelAsNotFinishedButton.clicked.connect(self.accomplished_task)
        self.project_name = project_name
        self.subject_name = subject_name
        self.numberOfSession.setText(str(session_number))
       
        self.today = date.today()
        now = datetime.datetime.now()
        self.current_time = now.strftime("%H:%M")
        self.data = read_file()
        self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                str(session_number)] = {'date': str(self.today), 'start': '00:00', 'end': '00:00', 'tasks': {'success':[],'fail':[]}}
        self.data.update()
        write_file(self.data)

    def go_main_menu(self):
        now = datetime.datetime.now()
        self.data = read_file()
        if self.timer.isActive():
         self.end_time = now.strftime("%H:%M")
         self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                str(session_number)]['end'] = self.end_time
        else:
            self.start_time = now.strftime("%H:%M")
            self.end_time = now.strftime("%H:%M")
            self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                str(session_number)]['start'] = self.start_time
            self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                str(session_number)]['end'] = self.end_time
        self.data.update()
        write_file(self.data)
        mainMenu = MainMenuUI()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def add_task(self):
        self.task = self.taskInput.text()
        if self.taskInput.text() == "" or self.taskInput.text() == "Enter a task please":
            self.taskInput.setText("Enter a task please")
        else:
            
            self.data = read_file()
            check_task =self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                    str(session_number)]['tasks']['success']
            if check_task =="":
                self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                        str(session_number)]['tasks']['success']=[self.task]
            else:
                self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                        str(session_number)]['tasks']['success'].append(self.task)
            self.data.update()
            write_file(self.data)
            self.tasksCombo.addItem(self.task)
            self.tasksCombo_2.addItem(self.task)
            

    def time_counter(self):
        now = datetime.datetime.now()
        self.current_time = now.strftime("%H:%M")
        if self.tasksCombo.currentText() == "" or self.taskInput.text() == "Enter a task please":
            self.taskInput.setText("Enter a task please")
        else:  
            
            self.timer.start(1000)  
            self.startStopButton.setStyleSheet("Qpushbutton{background-color:black")
            self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                    str(session_number)]['start'] = self.current_time
            self.data.update()
            write_file(self.data)
            self.startStopButton.setEnabled(False)
            
            
            

    def update_time_counter(self):
                self.remaining_time -= 1
                minutes = self.remaining_time // 60
                seconds = self.remaining_time % 60
                self.timeLabel.setText("{:02d}:{:02d}".format(minutes, seconds))
                
                if self.remaining_time <=0:
                    self.timer.stop()
                    
                    # self.done(0)
    def reset_timer(self):
        self.timer.stop()
        self.remaining_time = 1501
        self.time_counter()
        
    def end_session(self):
        if self.tasksCombo.currentText() == "" or self.taskInput.text() == "Enter a task please":
            self.taskInput.setText("Enter a task please")
        else:    
           if self.remaining_time <1500:
                now = datetime.datetime.now()
                self.end_time = now.strftime("%H:%M")
           else:
              self.end_time = "00:00"
           self.data = read_file()
           self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                str(session_number)]['end'] = self.end_time
           self.data.update()
           write_file(self.data)
           if self.end_time != "00:00":
             if session_number < 4:
                shortBreak = ShortBreakUI(self.project_name, self.subject_name)
                widget.addWidget(shortBreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
             else:
                longBreak = LongBreakUI()
                widget.addWidget(longBreak)
                widget.setCurrentIndex(widget.currentIndex()+1)

    def accomplished_task(self):
        self.unfinished_task = self.tasksCombo_2.currentText()
        self.data = read_file()
        check_task =self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                    str(session_number)]['tasks']['fail']
        if check_task =="":
                self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                        str(session_number)]['tasks']['fail'] = [self.unfinished_task]
        else:
                self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                        str(session_number)]['tasks']['fail'].append(self.unfinished_task)
        self.data[user.email]['projects'][self.project_name][self.subject_name]['session' +
                                                                                str(session_number)]['tasks']['success'].remove(self.unfinished_task)
        self.data.update()
        write_file(self.data)


class ShortBreakUI(QDialog):
    def __init__(self, project_name, subject_name):
        super(ShortBreakUI, self).__init__()
        loadUi('ui/shortBreak.ui', self)
        self.setWindowTitle('Short Break')

        self.remaining_time = 301 # 5 minutes in seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.startButton.clicked.connect(self.start_timer)
        self.skipButton.clicked.connect(self.skip_break)
        self.goToMainMenuButton.clicked.connect(self.go_to_main_menu)

        self.startButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.skipButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        instance = vlc.Instance()
        self.player = instance.media_player_new()
        self.working_time = instance.media_new("scott-buckley-moonlight.mp3")
        self.update_time()
        self.project_name = project_name
        self.subject_name = subject_name

    def update_time(self):
        global session_number
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timeLabel.setText("{:02d}:{:02d}".format(minutes, seconds))

        if self.remaining_time <= 0:
            self.timer.stop()
            self.player.stop() 
            session_number += 1
            skipBreak = PomodoroUI(self.project_name,
                                   self.subject_name)
            widget.addWidget(skipBreak)
            widget.setCurrentIndex(widget.currentIndex()+1)

            # self.done(0)

    def start_timer(self):
        self.player.set_media(self.working_time)
        self.player.play()
        self.timer.start(1000)

    def skip_break(self):
        global session_number
        session_number += 1
        self.player.stop() 
        self.timer.stop()
        skipBreak = PomodoroUI(self.project_name,
                               self.subject_name)
        widget.addWidget(skipBreak)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_main_menu(self):
        mainMenu = MainMenuUI()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI, self).__init__()
        loadUi('ui/longBreak.ui', self)
        self.setWindowTitle('Long Break')

        self.remaining_time = 1801  # 30 minutes in seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.startButton.clicked.connect(self.start_timer)
        self.skipButton.clicked.connect(self.skip_timer)
        self.goToMainMenuButton.clicked.connect(self.go_to_main_menu)

        self.startButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.skipButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update_time()

    def update_time(self):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timeLabel.setText("{:02d}:{:02d}".format(minutes, seconds))

        if self.remaining_time <= 0:
            global session_number
            session_number = 1
            self.timer.stop()
            # self.done(0)

    def start_timer(self):
        self.timer.start(1000)

    def skip_timer(self):
        global session_number
        session_number = 1
        self.go_to_main_menu()

    def go_to_main_menu(self):
        mainMenu = MainMenuUI()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)
UI = LoginUI()  # This line determines which screen you will load at first

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