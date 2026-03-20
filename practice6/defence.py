import os
import functools

folder_path = "sales"
files = os.listdir(folder_path)
print(f"Найденные файлы: {files}")
products = []

for file in files:
    with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
        for line in f:
            if "," in line:
                name, qty = line.strip().split(",")
                products.append((name, int(qty)))

print("Список продуктов:")
print(products)

total=len(products)
print(f"Totl number of records: {total}")
SUM=sum(p[1] for p in products)
print(f"Total_sum: {SUM}")

all=[p[1] for p in products]
highest=max(all)
lowest=min(all)

print(f"Max in products list: {highest}")
print(f"Min in products list: {lowest}")
x2_prod=list(map(lambda p: (p[0],p[1]+2),products))
print(f"Increased_list: {x2_prod}")

most=list(filter(lambda p: p[1]>5, products))
print(f"Products sold more than 5: {most}")

from functools import reduce
product_all=reduce(lambda x, y: x * y, all)
print(f"Product of all: {product_all}")

for i,v in enumerate(products, start=1):
    print(f"{i} {v[0]} {v[1]}")


names=[p[0] for p in products]
quantities=[p[1] for p in products]

zipped=list(zip(names, quantities))

print(f"Final zip(): {zipped}")

sorted_products=sorted(products, key=lambda x: x[1])
print(f"Sorted products: {sorted_products}")

avg_qty = sum(p[1] for p in products) / total if total > 0 else 0
popular_products = list(filter(lambda p:p[1]>5,products))
with open("sales_report.txt", "w", encoding="utf-8") as report:
    report.write(f"Totl number of records: {total}\n")
    report.write(f"Average quantity sold: {avg_qty:.1f}\n")
    report.write(f"Max in products list: {highest}\n")
    report.write(f"Min in products list: {lowest}\n")
    
    report.write("Popular products:\n")
    for name, qty in popular_products:
        report.write(f"{name} {qty}\n")