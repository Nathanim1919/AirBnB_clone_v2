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
result = exec_command(my_console, "all Place", 4)
if result is None or result == "":
    print("FAIL: No places retrieved")
if "my_id_p_0" not in result or "my_id_c_0" not in result or "my_id_u_0" not in result or "House 0" not in result or "desc" not in result or "100" not in result or "14.3" not in result:
    print("FAIL: Missing information 0")
if "my_id_p_1" not in result or "my_id_c_0" not in result or "my_id_u_0" not in result or "House 1" not in result or "-12.4" not in result or "0.3" not in result:
    print("FAIL: Missing information 1")
if "my_id_p_2" not in result or "my_id_c_0" not in result or "my_id_u_1" not in result or "Test House 2" not in result:
    print("FAIL: Missing information 2")
if "my_id_p_3" not in result or "my_id_c_1" not in result or "my_id_u_1" not in result or "House Bla" not in result or "150" not in result:
    print("FAIL: Missing information 3") 

print("OK", end="")

shutil.copy("tmp_console_main.py", "console.py")
