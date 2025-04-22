from threading import Event, Thread
import tkinter.messagebox
from helium import *
from helium._impl import sleep
import tkinter

def autoclick(id_number, password, shouldStopFlag):
    ID_NUMBER = id_number
    PASSWORD = password
    PATIENCE = 5400 # time in seconds to wait when site loads before timing out

    TIMEOUT = 0.5 # time in seconds to wait after enlistment attempt

    gone_wrong = False

    try:
        for i in range(1):
            url = "https://animo.sys.dlsu.edu.ph/psp/ps/"
            start_chrome(url)

            if shouldStopFlag.is_set():
                break

            # login into Animosys
            wait_until(Button('Sign In').exists, timeout_secs=PATIENCE)

            if shouldStopFlag.is_set():
                break

            write(ID_NUMBER, into="User ID:")

            if shouldStopFlag.is_set():
                break

            write(PASSWORD, into="Password:")

            if shouldStopFlag.is_set():
                break

            click("Sign In")

            url = "https://animo.sys.dlsu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true"
            go_to(url)

            if shouldStopFlag.is_set():
                break

            click("Enrollment: Add Classes")

            if shouldStopFlag.is_set():
                break
    except:
        gone_wrong = True

    # enlist in classes in shopping cart
    try:
        while not shouldStopFlag.is_set() and not gone_wrong:
            if shouldStopFlag.is_set():
                break

            wait_until(Link("Proceed to Step 2 of 3").exists, timeout_secs=20)

            if shouldStopFlag.is_set():
                break
            elif Link("Proceed to Step 2 of 3").exists:
                click("Proceed to Step 2 of 3")
            else: 
                url = "https://animo.sys.dlsu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true"
                go_to(url)
                click("Enrollment: Add Classes")
                continue

            wait_until(Link("Finish Enrolling").exists, timeout_secs=20)

            if shouldStopFlag.is_set():
                break
            elif Link("Finish Enrolling").exists:
                click("Finish Enrolling")
            else: 
                url = "https://animo.sys.dlsu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true"
                go_to(url)
                click("Enrollment: Add Classes")
                continue

            wait_until(Link("Add Another Class").exists, timeout_secs=20)

            if shouldStopFlag.is_set():
                break
            elif Link("Add Another Class").exists:
                click("Add Another Class")
            else:
                url = "https://animo.sys.dlsu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true"
                go_to(url)
                click("Enrollment: Add Classes")

            sleep(TIMEOUT)
    except:
        kill_browser()
        
    try:
        kill_browser()
    except:
        pass

class ThreadHandler:
    def __init__(self):
        self.thread = None
        self.event = None
        self.hasBeenInitialized = False
    def setThreadAndEvent(self, thread, event):
        self.thread = thread
        self.event = event
        self.hasBeenInitialized = True
    def startThread(self):
        if not self.hasBeenInitialized:
            return
        self.thread.start()
    def stopThread(self):
        if not self.hasBeenInitialized:
            return
        self.event.set()
        self.thread.join()
        self.event.clear()

if __name__ == "__main__":

    shouldStopFlag = Event()
    threadHandler = ThreadHandler()

    def startAutoclickThread():
        ID_NUMBER = id_number_textBox.get()
        PASSWORD = password_textBox.get()

        if not ID_NUMBER.isnumeric():
            tkinter.messagebox.showerror(message='DLSU ID number is not valid, was: ' + ID_NUMBER)
            return
        if PASSWORD.isspace():
            tkinter.messagebox.showerror(message='Password cannot be empty!')
            return

        thread = Thread(target=autoclick, args=(ID_NUMBER, PASSWORD, shouldStopFlag, ))
        threadHandler.setThreadAndEvent(thread, shouldStopFlag)
        threadHandler.startThread()

        id_number_textBox.config(state=tkinter.DISABLED)
        password_textBox.config(state=tkinter.DISABLED)
        start_button.config(state=tkinter.DISABLED)
        stop_button.config(state=tkinter.NORMAL)

    def stopAutoclickThread():
        threadHandler.stopThread()
        id_number_textBox.config(state=tkinter.NORMAL)
        password_textBox.config(state=tkinter.NORMAL)
        start_button.config(state=tkinter.NORMAL)
        stop_button.config(state=tkinter.DISABLED)

    window = tkinter.Tk()
    window.title('AS-Autoenlister UI')
    window.geometry('285x200')

    information_label = tkinter.Label(window, text='Please enter your credentials.')

    id_number_label = tkinter.Label(window, text='DLSU ID Number:')
    id_number_textBox = tkinter.Entry(window)

    password_label = tkinter.Label(window, text='Animo Sys Password:')
    password_textBox = tkinter.Entry(window, show='*')

    start_button = tkinter.Button(window, text="Start Autoclicking!", command=startAutoclickThread)
    stop_button = tkinter.Button(window, text="Stop Autoclicking.", command=stopAutoclickThread, state=tkinter.DISABLED)

    information_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), columnspan=2)

    id_number_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
    id_number_textBox.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))

    password_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10))
    password_textBox.grid(row=2, column=1, padx=(10, 10), pady=(10, 10))

    start_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))
    stop_button.grid(row=3, column=1, padx=(10, 10), pady=(10, 10))
    
    window.mainloop()