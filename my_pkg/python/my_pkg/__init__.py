import os
import platform

curr_path = os.getenv("PATH")
print(curr_path)

if platform.system() == "Windows":
    from pathlib import Path

    for path in curr_path.split(";"):
        if not Path(path).exists():
            continue
        os.add_dll_directory(path)
