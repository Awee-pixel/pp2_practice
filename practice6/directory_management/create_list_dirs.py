import os

curdir=os.getcwd()
print(f"CURRENT_DIR: {curdir}")

files=os.listdir("practice6")
print(files)
os.mkdir("test_folder")
if os.path.exists("test_folder"):
    try:
        os.rmdir("test_folder") 
    except:
        print("File is already deleted")
    else:
        print("GoodBye")

from pathlib import Path
path=Path("practice6")
print(path)
for file in path.iterdir():
    print(file)

extra_files=list(path.glob("*.csv"))
print(extra_files)

Path("practice6/test").mkdir(parents=True,exist_ok=True)

file=Path("practice6/test.csv")
print(file.exists())

data_dir=Path("practice6")
for file in data_dir.glob("*.csv"):
    print(f"Processing {file}")

