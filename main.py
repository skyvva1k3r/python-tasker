import time
import os
from datetime import datetime
l = []
obj = ["name", "description", "expires", "deadline"]

def menu():
    print("Print '1' to list all tasks.\nPrint '2' to add task.\nPrint '3' to delete task.\nPrint '4' to kill tasker.")
    n = input()
    match n:
        case "1":
            list_task()
        case "2":
            add_task()
        case "3":
            delete_task()
        case "4":
            os._exit(0)
        case _:
            print("wrong input")
            return 0

def list_task():
    for i in range(len(l)):
        print(*l[i])

def add_task():
    temp = []
    tempStr = ""
    for i in range(len(obj)):
        match i:
            case 0:
                temp.append(input("Enter the name of task:\n"))
            case 1:
                temp.append(input("Enter the desc of task:\n"))
            case 2:
                tempStr = input("Enter a date (YYYY-MM-DD HH:MM): ")
                tempStr = datetime.strptime(tempStr, "%Y-%m-%d %H:%M")
                tempStr = datetime.strftime(tempStr, "%c")
                temp.append(tempStr)
            case 3:
                temp.append(time.ctime(time.mktime(time.gmtime())+10800))
        print(temp)
    l.append(temp)

def delete_task():
    return 0


while True:
    menu()