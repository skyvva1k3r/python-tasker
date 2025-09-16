import time
import os
from datetime import datetime

l = []
obj = ["name", "description", "current", "deadline", "status"]

def menu():
    print("\nPrint '1' to list all tasks.\nPrint '2' to add task.\nPrint '3' to change status of the task.\nPrint '4' to delete task.\nPrint '5' to save and quit.\n")
    n = input()
    match n:
        case "1":
            list_task()
        case "2":   
            add_task()
        case "3":
            status()
        case "4":
            delete_task()
        case "5":
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
    graphics()


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
    temp.append("Planned")
    l.append(temp)

def status():
    os.system('cls')
    print("Enter name of the task, which status you want to change.\n")
    name = input()
    for i in range(len(l)):
        if name == l[i][0]:
            print("Enter current status of the task. (Completed/In progress)")
            status = input()
            if status == "Completed":
                l[i][-1] = "Completed"
                return 0
            elif status == "In progress":
                l[i][-1] = "In progress"

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
    if n == 0:
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
    print("\nEnter the name of the task you want to delete:\n(Attention, will be deleted first found task with entered name.)")
    temp = -1
    name = input()
    for i in range(len(l)):
        if name in l[i][0]:
            temp = l.pop(i)
            break
    os.system('cls')
    if temp == -1:
        print("\nTask not found.")
    else:
        print("Task was successfully deleted.")

def graphics():
    local = time.localtime()
    temp = (local[3]*60*60)+(local[4]*60)+(local[5])
    local = time.mktime(local)-temp
    print()
    for task in l:
        print(f"Task {task[0][:10].ljust(10, ' ')}", end = "")
        for i in range(7):
            print("[", end = " ")
            for j in range(12):
                if  time.mktime(time.strptime(task[2], "%a %b %d %H:%M:%S %Y")) < (local+((j*60*120)+(i*12*120*60))) and\
                    time.mktime(time.strptime(task[3], "%a %b %d %H:%M:%S %Y")) > (local+((j*60*120)+(i*12*120*60))):
                        print("0", end = " ")
                else:
                    print("-", end = " ")
            print("]", end = "")
        print("")

load()

while True:
    menu()