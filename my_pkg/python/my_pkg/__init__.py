import platform

if platform.system() == "Windows":
    import sysconfig
    import os

    os.add_dll_directory(sysconfig.get_path("scripts"))
