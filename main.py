from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QSizePolicy
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
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
UI = LongBreakUI() # This line determines which screen you will load at first

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
