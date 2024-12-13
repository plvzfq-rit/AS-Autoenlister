from helium import *
from helium._impl import sleep

ID_NUMBER = ENTER_YOUR_ID_NUMBER_HERE
PASSWORD = ENTER_YOUR_PASSWORD_HERE

TIMEOUT = 0.5 # time in seconds to wait after enlistment attempt

url = "https://animo.sys.dlsu.edu.ph/psp/ps/"
start_chrome(url)

# login into Animosys
wait_until(Button('Sign In').exists)
write(ID_NUMBER, into="User ID:")
write(PASSWORD, into="Password:")
click("Sign In")

url = "https://animo.sys.dlsu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=HCCC_ENROLLMENT&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ENROLLMENT&IsFolder=true"
go_to(url)
click("Enrollment: Add Classes")

# enlist in classes in shopping cart
while True:
    wait_until(Link("Proceed to Step 2 of 3").exists)
    click("Proceed to Step 2 of 3")
    wait_until(Link("Finish Enrolling").exists)
    click("Finish Enrolling")
    wait_until(Link("Add Another Class").exists)
    click("Add Another Class")
    sleep(TIMEOUT)
