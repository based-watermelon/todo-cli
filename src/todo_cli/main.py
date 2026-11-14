import os
import pickle
from datetime import datetime
from pathlib import Path 

#init empty list to store todo
todos = []

DATA_DIR = Path.home() / ".local" / "share" / "todo-cli"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TODO_FILE = DATA_DIR / "todos.pkl"

class Todo():
    def __init__(self, task, created_at, task_completed = False):
        self.task = task
        self.created_at = created_at
        self.task_completed = task_completed

def save_to_file():
    with open(TODO_FILE, "wb") as file:
        pickle.dump(todos, file)

def read_from_file():
    global todos

    if TODO_FILE.exists():
        with open(TODO_FILE, "rb") as file:
            todos = pickle.load(file)

def create_todo():

    task = input("Enter your task: ")
    created_at = datetime.now().strftime("%d|%m %H:%M")
    todo = Todo(task, created_at)
    todos.append(todo)

    save_to_file()


def print_todos():

    SEP = "+------+----------------------------+--------------+--------+"

    print(SEP)
    print("|  ID  | TASK                       | CREATED      | STATUS |")
    print(SEP)

    if not todos:
        print("|" + "( no todos yet )".center(59) + "|")
    else:
        for i, todo in enumerate(todos, start=1):
            task = todo.task
            if len(task) > 26:
                task = task[:23] + "..."

            created = todo.created_at
            # if len(created) > 12:
            #     created = created[:12]

            mark = "x" if todo.task_completed else " "

            print(f"| {i:03d}  | {task:<26} | {created:<12} |  [{mark}]   |")
    print(SEP)
    
def mark_as_complete():
    try:
        print_todos()

        todo_id = int(input("Enter Todo ID:")) -1

        todos[todo_id].task_completed = True
        save_to_file()
    except IndexError:
        print("Invalid TODO ID")
    except ValueError:
        print("Invalid Input")
    
def delete_todo():
    print_todos()

    try:
        todo_id = int(input("Enter Todo ID:")) -1
        del todos[todo_id]
        save_to_file()
    except IndexError:
        print("Invalid TODO ID")
    except ValueError:
        print("Invalid Input") 

def show_options():
    while True:
        user_choice = input("'A' : add  'D' : delete  'C' : complete  'Q' : quit \n").upper()

        if user_choice == 'A':
            create_todo()
        elif user_choice == 'D':
            delete_todo()
        elif user_choice == 'C':
            mark_as_complete()
        elif user_choice == 'Q':
            break
        else:
            print(f"command not found: {user_choice}")
        print_todos()
    
def first_init():
    if os.path.exists(TODO_FILE):
        read_from_file()
        print_todos()
    else:
        print("TODO LIST")
        read_from_file()
        print_todos()

def main():
    #clear console
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[32;1m")
    first_init()
    show_options()

if __name__ == "__main__":
    main()
    