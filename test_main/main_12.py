#!/usr/bin/python3
import inspect
import io
import sys
import cmd
import shutil
import os

"""
 Backup console file
"""
if os.path.exists("tmp_console_main.py"):
    shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("console.py", "tmp_console_main.py")


"""
 Updating console to remove "__main__"
"""
with open("tmp_console_main.py", "r") as file_i:
    console_lines = file_i.readlines()
    with open("console.py", "w") as file_o:
        in_main = False
        for line in console_lines:
            if "__main__" in line:
                in_main = True
            elif in_main:
                if "cmdloop" not in line:
                    file_o.write(line.lstrip("    ")) 
            else:
                file_o.write(line)

import console


"""
 Create console
"""
console_obj = "HBNBCommand"
for name, obj in inspect.getmembers(console):
    if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
        console_obj = obj

my_console = console_obj(stdout=io.StringIO(), stdin=io.StringIO())
my_console.use_rawinput = False


"""
 Exec command
"""
def exec_command(my_console, the_command, last_lines = 1):
    my_console.stdout = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = my_console.stdout
    my_console.onecmd(the_command)
    sys.stdout = real_stdout
    lines = my_console.stdout.getvalue().split("\n")
    return "\n".join(lines[(-1*(last_lines+1)):-1])


"""
 Tests
"""
result = exec_command(my_console, "all User", 4)
if result is None or result == "":
    print("FAIL: No users retrieved")
if "my_id_0" not in result or "email0@gmail.com" not in result or "pwd0" not in result or "John" not in result or "Doe" not in result:
    print("FAIL: Missing information 0")
if "my_id_1" not in result or "email1@gmail.com" not in result or "pwd1" not in result or "Bob" not in result:
    print("FAIL: Missing information 1")
if "my_id_2" not in result or "email2@gmail.com" not in result or "pwd2" not in result or "Did" not in result:
    print("FAIL: Missing information 2")
if "my_id_3" not in result or "email3@gmail.com" not in result or "pwd3" not in result:
    print("FAIL: Missing information 3")
    
print("OK", end="")

shutil.copy("tmp_console_main.py", "console.py")
