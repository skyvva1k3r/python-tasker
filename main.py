import time
import os
from datetime import datetime

l = []
obj = ["name", "description", "expires", "deadline"]

def menu():
    print("\nPrint '1' to list all tasks.\nPrint '2' to add task.\nPrint '3' to delete task.\nPrint '4' to kill tasker.\n")
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
    print("List of your tasks")
    for i in range(len(l)):
        print("\n", *l[i], sep = "\n")

def add_task():
    temp = []
    tempStr = ""
    for i in range(len(obj)):
        match i:
            case 0:
                temp.append(input("\nEnter the name of task:\n"))
            case 1:
                temp.append(input("Enter the desc of task:\n"))
            case 2:
                tempStr = input("Enter a date (YYYY-MM-DD HH:MM):\n")
                try: 
                    tempStr = datetime.strptime(tempStr, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("\nWrong time format, try again.")
                    return 0
                tempStr = datetime.strftime(tempStr, "%c")
                temp.append(tempStr)
            case 3:
                temp.append(time.ctime(time.mktime(time.gmtime())+10800))
    l.append(temp)

def delete_task():
    print("\nEnter the name of the task you want to delete:\n")
    

while True:
    menu()