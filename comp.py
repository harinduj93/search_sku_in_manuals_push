import csv

def read_csv(file, delimiter):
    skus_prices = {}
    with open(file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            sku = row["SKU"].strip()
            price = float(row["PRICE"].strip().replace(',', '.'))
            if sku in skus_prices:
                skus_prices[sku] = max(skus_prices[sku], price)
            else:
                skus_prices[sku] = price
    return skus_prices

file1_data = read_csv('file1.csv', ';')
file2_data = read_csv('file2.csv', ';')

for sku in file1_data.keys() | file2_data.keys():
    price_file1 = file1_data.get(sku, float('-inf'))
    price_file2 = file2_data.get(sku, float('-inf'))
    highest_price = max(price_file1, price_file2)
    if highest_price > float('-inf'):
        print(f'SKU: {sku}, Highest Price: {highest_price}')
