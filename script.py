from helium import *
from helium._impl import sleep

ID_NUMBER = "ID_NUMBER"
PASSWORD = "PASSWORD"
PATIENCE = 300 # time in seconds to wait when site loads before timing out
ENROLL = True # set true if you're enrolling, false if you're sniping

TIMEOUT = 0.5 # time in seconds to wait after enlistment attempt

url = "https://animo.sys.dlsu.edu.ph/psp/ps/"
start_chrome(url)

# login into Animosys
wait_until(Button('Sign In').exists, timeout_secs=PATIENCE)
write(ID_NUMBER, into="User ID:")
write(PASSWORD, into="Password:")
click("Sign In")

wait_until(Link("Self Service").exists, timeout_secs=PATIENCE)
url = "https://animo.sys.dlsu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true"
go_to(url)
click("Enrollment: Add Classes")

# enlist in classes in shopping cart
while True:
    wait_until(Link("Proceed to Step 2 of 3").exists, timeout_secs=PATIENCE)
    click("Proceed to Step 2 of 3")

    try:
        wait_until(Link("Finish Enrolling").exists, timeout_secs=(1 if ENROLL else PATIENCE))
    except:
        continue

    click("Finish Enrolling")

    wait_until(Link("Add Another Class").exists, timeout_secs=PATIENCE)
    click("Add Another Class")
    sleep(TIMEOUT)
