#! /usr/bin/env python
import subprocess
import shutil

arch = subprocess.check_output(["uname", "-m"]).decode().strip()
if arch.startswith("arm"):
    arch = "arm"
arch = arch.replace("powerpc", "ppc")
arch = arch.replace("_64", "-64")

shutil.copy("libmusashi.so", "src/main/resources/linux-{}/libmusashi.so".format(arch))
