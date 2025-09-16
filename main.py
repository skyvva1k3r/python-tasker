import time
import os
from datetime import datetime

l = []
obj = ["name", "description", "current", "deadline"]

def menu():
    print("\nPrint '1' to list all tasks.\nPrint '2' to add task.\nPrint '3' to delete task.\nPrint '4' to save and quit.\n")
    n = input()
    match n:
        case "1":
            list_task()
        case "2":   
            add_task()
        case "3":
            delete_task()
        case "4":
            save()
            os._exit(0)
        case _:
            print("wrong input")
            return 0

def list_task():
    os.system('cls')
    if len(l) == 0:
        os.system('cls')
        print("You have no tasks for now.")
    else:
        print("List of your tasks:")
    for i in range(len(l)):
        print("\n", *l[i], sep = "\n")

def add_task():
    os.system('cls')
    temp = []
    tempStr = ""
    for i in range(len(obj)):
        match i:
            case 0:
                temp.append(input("\nEnter the name of task:\n"))
            case 1:
                temp.append(input("Enter the desc of task:\n"))
            case 3:
                tempStr = input("Enter a date (YYYY-MM-DD HH:MM):\n")
                try: 
                    tempStr = datetime.strptime(tempStr, "%Y-%m-%d %H:%M")
                except ValueError:
                    os.system('cls')
                    print("\nWrong time format, try again.")
                    return 0
                tempStr = datetime.strftime(tempStr, "%c")
                if time.mktime(time.strptime(tempStr, "%a %b %d %H:%M:%S %Y")) <= (time.mktime(time.gmtime())+10800):
                    os.system('cls')
                    print("Deadline is in past.")
                    return 0
                temp.append(tempStr)
            case 2:
                temp.append(time.ctime(time.mktime(time.gmtime())+10800))
    l.append(temp)

def save():
    file = open('data.txt', 'w')
    file.write(str(len(l)))
    file.write("\n")
    for task in l:
        file.write("|".join(task))
        file.write("\n")
    file.close()

def load():
    file = open('data.txt', 'r')
    try:
        n = int(file.readline())
    except ValueError:
        print("Nothing to load.\n")
        return 0
    for i in range(n):
        temp = (file.readline()).split("|")
        temp[-1] = temp[-1][:-1]
        l.append(temp)
        temp = []
    print(n, "tasks was loaded successfully.")

def delete_task():
    os.system('cls')
    print("\nEnter the name of the task you want to delete:\n(Attention, will be deleted first found task with entered name)")
    name = input()
    for i in range(len(l)):
        if name in l[i]:
            l.pop(i)
            break
    os.system('cls')
    print("\nTask not found.")
    


load()

while True:
    menu()