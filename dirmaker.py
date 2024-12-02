import os
import shutil

for i in range(3, 26):
    dirname = str(i).zfill(2)
    os.makedirs(dirname, exist_ok=True)
    for filename in ["1.py", "2.py"]:
        shutil.copy("template.py", os.path.join(dirname, filename))
    for filename in ["test.txt", "input.txt"]:
        with open(os.path.join(dirname, filename), "w"):
            pass
