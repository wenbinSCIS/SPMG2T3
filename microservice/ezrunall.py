import os
import _thread
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

# change the path in env based on your local path, e.g.:

# MICROSERVICE_PATH="C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\"
MICROSERVICE_PATH=os.environ.get("MICROSERVICE_PATH")
#MICROSERVICE_PATH = "C:\\wamp64\\www\\IS212\\microservice\\"

def run_app1():
    os.system(f'python {MICROSERVICE_PATH}courses.py') 
def run_app2():
    os.system(f'python {MICROSERVICE_PATH}learningjourney.py') 
def run_app3():
    os.system(f'python {MICROSERVICE_PATH}learningjourneycourses.py')
def run_app4():
    os.system(f'python {MICROSERVICE_PATH}roles.py') 
def run_app5():
    os.system(f'python {MICROSERVICE_PATH}skills_acquired_by_course.py') 
def run_app6():
    os.system(f'python {MICROSERVICE_PATH}skills_required_by_role.py')
def run_app7():
    os.system(f'python {MICROSERVICE_PATH}skills.py')
def run_app8():
    os.system(f'node {MICROSERVICE_PATH}learningJourney.mjs') 
def run_app9():
    os.system(f'node {MICROSERVICE_PATH}learningJourneyCourses.mjs')

if __name__=='__main__':
    t1 = Thread(target=run_app1)
    t1.start()
    t2 = Thread(target=run_app2)
    t2.start()
    t3 = Thread(target=run_app3)
    t3.start()
    t4 = Thread(target=run_app4)
    t4.start()
    t5 = Thread(target=run_app5)
    t5.start()
    t6 = Thread(target=run_app6)
    t6.start()
    t7 = Thread(target=run_app7)
    t7.start()
    t8 = Thread(target=run_app8)
    t8.start()
    t9 = Thread(target=run_app9)
    t9.start()