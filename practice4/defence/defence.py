import json

with open("cars.json", "r", encoding="utf-8") as f:
    data = json.load(f)

added_brends = set()   
total_price = 0

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
            if found["brend"] not in added_brends:
                added_brends.add(found["brend"])
                total_price += float(found["price"])

                f.write("Да, такая машина есть!\n")
                f.write(f"Марка: {found['brend']}\n")
                f.write(f"Модель: {found['model']}\n")
                f.write(f"Цена: {found['price']}\n")
            else:
                f.write("Эта машина уже добавлена.\n")
        else:
            f.write("Такой машины нет в базе.\n")

    print("Результат записан в result.json")

print(f"\nИТОГО (без повторов): {total_price}")