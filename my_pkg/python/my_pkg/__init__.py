import os
import platform

curr_path = os.getenv("PATH")
print(curr_path)

if platform.system() == "Windows":
    for path in curr_path.split(";"):
        os.add_dll_directory(path)
