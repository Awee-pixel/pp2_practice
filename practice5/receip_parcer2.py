import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r'\d[\d ]*,\d{2}', text)

prices_clean = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

products = re.findall(r'\d+\.\n(.+)', text)

total = sum(prices_clean)

datetime_match = re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}', text)
datetime = datetime_match.group() if datetime_match else None

payment_match = re.search(r'Банковская карта', text)
payment_method = payment_match.group() if payment_match else "Unknown"

data = {
    "products": products,
    "prices": prices_clean,
    "total_calculated": total,
    "datetime": datetime,
    "payment_method": payment_method
}

print(json.dumps(data, indent=4, ensure_ascii=False))