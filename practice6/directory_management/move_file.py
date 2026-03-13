from pathlib import Path

source_file = Path("raw.txt")
target_dir = Path("archive")
target_file = target_dir / "raw.txt"

target_dir.mkdir(parents=True, exist_ok=True)

if source_file.exists():
    source_file.rename(target_file)
    print(f"Файл {source_file.name} перемещен.")
else:
    print("Файл не существует.")

from pathlib import Path

source_file = Path("archive/raw.txt")
target_file = Path("raw.txt")

if source_file.exists():
    source_file.rename(target_file)
    print(f"Файл {source_file.name} вернулся обратно.")
else:
    print("Такого файла в архиве не существует")



