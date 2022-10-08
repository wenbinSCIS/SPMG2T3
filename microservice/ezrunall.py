import os
import _thread
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

# change the path in env based on your local path, e.g.:
# MICROSERVICE_PATH="C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\"
MICROSERVICE_PATH=os.environ.get("MICROSERVICE_PATH")
# MICROSERVICE_PATH = "F:\\Code\\SPMG2T3\\microservice\\"

def run_app1():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\courses.py') 

def run_app2():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\learningjourney.py') 
def run_app3():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\learningjourneycourses.py')
def run_app4():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\roles.py') 
def run_app5():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\skills_acquired_by_course.py') 
def run_app6():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\microservice\\skills_required_by_role.py')
def run_app7():
    os.system('python C:\\Users\\wenbi\Desktop\\SPMG2T3\\microservice\\skills.py')  

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