class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        priority, text = int(args[0]), args[1]
        if not priority in self.current_items:
            print(f"Added task: \"{text}\" with priority {priority}")
            self.current_items[priority] = text
        else:
            print(f"Added task: \"{text}\" with priority {priority}")
            while priority in self.current_items:
                temp = self.current_items[priority]
                self.current_items[priority] = text
                text = temp
                priority += 1
            self.current_items[priority] = text
        self.write_current()

    def done(self, args):
        priority = int(args[0])
        if priority in self.current_items:
            item = self.current_items[priority]
            del self.current_items[priority]

            self.completed_items.append(item)
            print("Marked item as done.")
            self.write_current()
            self.write_completed()
        else:
            print(
                f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])
        if priority in self.current_items:
            del self.current_items[priority]
            print(f"Deleted item with priority {priority}")
        else:
            print(
                f"Error: item with priority {priority} does not exist. Nothing deleted.")
        self.write_current()

    def ls(self):
        for index, priority in enumerate(sorted(self.current_items.keys())):
            print(f"{index+1}. {self.current_items[priority]} [{priority}]")

    def report(self):
        print(f"Pending : {len(self.current_items.keys())}")
        for index, priority in enumerate(sorted(self.current_items.keys())):
            print(f"{index+1}. {self.current_items[priority]} [{priority}]")
        print(f"\nCompleted : {len(self.completed_items)}")
        for index, task in enumerate(self.completed_items):
            print(f"{index+1}. {task}")
