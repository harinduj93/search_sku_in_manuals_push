import csv


def read_csv(file_path, delimiter):
    data = {}
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            data[row['SKU'].strip()] = float(row['PRICE'].replace(',', '.'))
    return data


def find_matching_skus(file1_data, file2_data):
    matching_skus = set(file1_data.keys()) & set(file2_data.keys())
    return matching_skus


def write_matching_skus_with_price_range(matching_skus, file1_data, file2_data):
    with open('matching_skus_with_price_range.csv', 'w', newline='') as csvfile:
        fieldnames = ['SKU', 'Highest Price', 'Lowest Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sku in matching_skus:
            highest_price = max(file1_data.get(sku, 0), file2_data.get(sku, 0))
            lowest_price = min(file1_data.get(sku, float('inf')), file2_data.get(sku, float('inf')))
            writer.writerow({'SKU': sku, 'Highest Price': highest_price, 'Lowest Price': lowest_price})


def write_skus_with_different_prices(diff_skus, file1_data, file2_data):
    with open('skus_with_different_prices.csv', 'w', newline='') as csvfile:
        fieldnames = ['SKU', 'Price in File 1', 'Price in File 2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sku in diff_skus:
            writer.writerow({'SKU': sku, 'Price in File 1': file1_data.get(sku, 'N/A'), 'Price in File 2': file2_data.get(sku, 'N/A')})


def main():
    file1_path = 'file1.csv'
    file2_path = 'file2.csv'

    file1_data = read_csv(file1_path, ';')
    file2_data = read_csv(file2_path, ';')

    print("SKUs and Prices in File 1:")
    print(file1_data)
    print("\nSKUs and Prices in File 2:")
    print(file2_data)

    matching_skus = find_matching_skus(file1_data, file2_data)

    if matching_skus:
        print("\nMatching SKUs:")
        for sku in matching_skus:
            print(sku)
        write_matching_skus_with_price_range(matching_skus, file1_data, file2_data)
        print("Matching SKUs with price range have been written to 'matching_skus_with_price_range.csv'.")

        # Find SKUs with different prices
        diff_skus = set()
        for sku in matching_skus:
            if file1_data.get(sku) != file2_data.get(sku):
                diff_skus.add(sku)
        if diff_skus:
            print("\nSKUs with different prices:")
            for sku in diff_skus:
                print(sku)
            write_skus_with_different_prices(diff_skus, file1_data, file2_data)
            print("SKUs with different prices have been written to 'skus_with_different_prices.csv'.")
        else:
            print("\nNo SKUs found with different prices.")
    else:
        print("\nNo matching SKUs found.")


if __name__ == "__main__":
    main()
