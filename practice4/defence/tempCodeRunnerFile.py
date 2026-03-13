import json

with open("cars.json", "r", encoding="utf-8") as f:
    data = json.load(f)

while True:
    car_name = input("Введите марку машины: ")
    if car_name == "exit":
        break

    found = None
    for car in data["cars"]:
        if car["brend"] == car_name:
            found = car
            break

    with open("result.json", "a", encoding="utf-8") as f:
        f.write("\n")
        if found:
            f.write("Да, такая машина есть!\n")
            f.write(f"Марка: {found['brend']}\n")
            f.write(f"Модель: {found['model']}\n")
            f.write(f"Цена: {found['price']}\n")
        else:
            f.write("Такой машины нет в базе.\n")

    print("Результат записан в result.json")