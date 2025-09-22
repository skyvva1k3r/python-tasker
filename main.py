import time
import os
from datetime import datetime
import click

l = []
obj = ["name", "description", "current", "deadline", "status"]
week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def list_task():
    os.system('cls')
    if len(l) == 0:
        os.system('cls')
        print("You have no tasks for now.")
        return 0
    else:
        print("List of your tasks:")
    for i in range(len(l)):
        print("\n", *l[i], sep = "\n")
    graphics()

def add_task_interactive():
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
    return temp[0]  # возвращаем имя задачи

def add_task_cli(name, description, deadline):
    temp = []
    tempStr = ""
    
    # Проверка дедлайна
    try: 
        tempStr = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Wrong time format. Use: YYYY-MM-DD HH:MM")
        return False
        
    tempStr = datetime.strftime(tempStr, "%c")
    if time.mktime(time.strptime(tempStr, "%a %b %d %H:%M:%S %Y")) <= (time.mktime(time.gmtime())+10800):
        print("Deadline is in past.")
        return False
    
    temp.extend([name, description, time.ctime(time.mktime(time.gmtime())+10800), tempStr, "Planned"])
    l.append(temp)
    return True

def status_interactive():
    os.system('cls')
    print("Enter name of the task, which status you want to change.\n")
    name = input()
    for i in range(len(l)):
        if name == l[i][0]:
            print("Enter current status of the task. (Completed/In progress)")
            status = input()
            if status == "Completed":
                l[i][-1] = "Completed"
                return name
            elif status == "In progress":
                l[i][-1] = "In progress"
                return name
    return None

def status_cli(name, new_status):
    for i in range(len(l)):
        if name == l[i][0]:
            if new_status in ["Completed", "In progress", "Planned"]:
                l[i][-1] = new_status
                return True
            else:
                print("Invalid status. Use: Completed/In progress/Planned")
                return False
    return False

def save():
    file = open('data.txt', 'w')
    file.write(str(len(l)))
    file.write("\n")
    for task in l:
        file.write("|".join(task))
        file.write("\n")
    file.close()

def load():
    try:
        file = open('data.txt', 'r')
    except FileNotFoundError:
        return 0
    try:
        n = int(file.readline())
    except ValueError:
        return 0
    if n == 0:
        return 0
    for i in range(n):
        temp = (file.readline()).split("|")
        temp[-1] = temp[-1][:-1]
        l.append(temp)
        temp = []
    return n

def delete_task_interactive():
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
        return None
    else:
        print("Task was successfully deleted.")
        return temp[0]

def delete_task_cli(name):
    for i in range(len(l)):
        if name == l[i][0]:
            deleted_task = l.pop(i)
            return True
    return False

def graphics():
    local = time.localtime()
    temp = (local[3]*60*60)+(local[4]*60)+(local[5])
    local = time.mktime(local)-temp
    print()
    print("\t   ", end = "")
    for i in range(7):
        current_day_index = time.gmtime()[6]
        day_index = (current_day_index + i) % 7
        print(week[day_index].ljust(19, " "), end = "")
    print()
    for task in l:
        print(f"Task {task[0][:5].ljust(5, ' ')}", end = "")
        for i in range(7):
            print("[", end = " ")
            for j in range(8):
                if  time.mktime(time.strptime(task[2], "%a %b %d %H:%M:%S %Y")) < (local+((j*60*180)+(i*12*180*60))) and\
                    time.mktime(time.strptime(task[3], "%a %b %d %H:%M:%S %Y")) > (local+((j*60*180)+(i*12*180*60))):
                        print("0", end = " ")
                else:
                    print("-", end = " ")
            print("]", end = "")
        print("")

# CLI команды с Click
@click.group()
def cli():
    """Task Manager - управление задачами из командной строки"""
    loaded_count = load()
    if loaded_count > 0:
        click.echo(f"Loaded {loaded_count} tasks")
    pass

@cli.command()
def list():
    """Показать все задачи"""
    list_task()

@cli.command()
@click.option('--name', prompt='Task name', help='Название задачи')
@click.option('--description', prompt='Description', help='Описание задачи')
@click.option('--deadline', prompt='Deadline (YYYY-MM-DD HH:MM)', help='Дедлайн задачи')
def add(name, description, deadline):
    """Добавить новую задачу"""
    if add_task_cli(name, description, deadline):
        click.echo(f"Task '{name}' added successfully!")
        save()
    else:
        click.echo("Failed to add task")

@cli.command()
@click.option('--name', prompt='Task name', help='Название задачи')
@click.option('--status', type=click.Choice(['Completed', 'In progress', 'Planned']), 
              prompt='New status', help='Новый статус задачи')
def status(name, status):
    """Изменить статус задачи"""
    if status_cli(name, status):
        click.echo(f"Status of task '{name}' changed to '{status}'")
        save()
    else:
        click.echo(f"Task '{name}' not found")

@cli.command()
@click.option('--name', prompt='Task name', help='Название задачи для удаления')
def delete(name):
    """Удалить задачу"""
    if delete_task_cli(name):
        click.echo(f"Task '{name}' deleted successfully!")
        save()
    else:
        click.echo(f"Task '{name}' not found")

@cli.command()
def interactive():
    """Интерактивный режим (твое оригинальное меню)"""
    while True:
        click.echo("\n" + "="*50)
        click.echo("1. List all tasks")
        click.echo("2. Add task")
        click.echo("3. Change status of the task")
        click.echo("4. Delete task")
        click.echo("5. Save and quit")
        click.echo("="*50)
        
        choice = click.prompt("Enter your choice", type=click.Choice(['1', '2', '3', '4', '5']))
        
        match choice:
            case "1":
                list_task()
            case "2":   
                add_task_interactive()
                save()
            case "3":
                result = status_interactive()
                if result:
                    save()
            case "4":
                result = delete_task_interactive()
                if result:
                    save()
            case "5":
                save()
                click.echo("Goodbye!")
                break

if __name__ == "__main__":
    cli()