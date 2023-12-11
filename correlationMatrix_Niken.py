import csv

# Mempersiapkan Tahapan Kalkulasi Correlation Matrix
# Menyiapkan Pembacaan File Data CSV
def read_csv(dataHotel):
    data = []
    with open(dataHotel, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def calculate_correlation_matrix(data):
    num_rows = len(data)
    num_cols = len(data[0])

    # Menghitung mean (rata-rata) untuk setiap kolom
    mean = []
    for j in range(num_cols):
        column_sum = 0
        count = 0
        for i in range(num_rows):
            try:
                value = float(data[i][j])
                column_sum += value
                count += 1
            except ValueError:
                continue
        mean.append(round(column_sum / count, 3)) if count else mean.append(0)

    # Menghitung korelasi matriks
    correlation_matrix = [[0] * num_cols for _ in range(num_cols)]
    for i in range(num_cols):
        for j in range(num_cols):
            num = 0
            den1 = 0
            den2 = 0
            for k in range(num_rows):
                try:
                    value_i = float(data[k][i])
                    value_j = float(data[k][j])
                    num += (value_i - mean[i]) * (value_j - mean[j])
                    den1 += (value_i - mean[i]) ** 2
                    den2 += (value_j - mean[j]) ** 2
                except ValueError:
                    continue
            cor = num / ((den1 ** 0.5) * (den2 ** 0.5))
            correlation_matrix[i][j] = round(cor, 3)

    return correlation_matrix

def display_csv_data(data):
    # Menampilkan header row dari file CSV
    header = data[0]
    print(header)

    # Menampilkan isi data dari file CSV
    for row in data[1:]:
        print(row)

def display_correlation_matrix_table(correlation_matrix, header):
    # Menampilkan hasil Tabel Perhitungan Korelasi Matriks
    print(f"----- Tabel Correlation Matrix -----")
    for row in correlation_matrix:
        print(row)

def display_correlation_matrix_results(correlation_matrix, header):
    # Menampilkan hasil korelasi matriks
    print("\n")
    print(f"----- Hasil Pembacaan dari Tabel Correlation Matrix -----")
    header = header[1:]  # Menghapus kolom pertama dari header
    for i in range(len(header)):
        print(f"Korelasi dengan {header[i]}:")
        for j in range(len(header)):
            print(f"{header[j]}: {correlation_matrix[i][j]}")
        print()

# Memasukkan nama file CSV yang ingin dibaca
file_name = "european-hotel-data.csv"

# Membaca data dari file CSV
data = read_csv(file_name)

# Opening
print("----- UTS DATA MINING NIKEN MAHARANI PERMATA (SIB_3E / 2141762006 / 19) -----\n")

# Data Understanding
print("Terdapat Data European Hotel Satisfaction dengan kategori data sebagai berikut:")
dataKategori = ["1. Hotel wifi service", "2. Departure/Arrival convenience", "3. Ease of Online booking",	
                "4. Hotel location", "5. Food and drink", "6. Stay comfort", "7. Common Room entertainment",	
                "8. Checkin/Checkout service", "9. Other service", "10. Cleanliness"]
for item in dataKategori:
    print(item)

# Menu selection function
print()
def menu():
    print("Berikut Menu yang Dapat Dipilih")
    print("1. Tampilkan data CSV")
    print("2. Tampilkan tabel korelasi matriks")
    print("3. Tampilkan hasil korelasi matriks")
    print("0. Keluar")
    print("\n")

# Main program
while True:
    menu()
    choice = input("Pilih menu: ")
    if choice == "1":
        display_csv_data(data)
        print("\n")
    elif choice == "2":
        correlation_matrix = calculate_correlation_matrix(data[1:])
        display_correlation_matrix_table(correlation_matrix, data[0])
        print("\n")
    elif choice == "3":
        correlation_matrix = calculate_correlation_matrix(data[1:])
        display_correlation_matrix_results(correlation_matrix, data[0])
        print("\n")
    elif choice == "0":
        print("Sekian. Terima Kasih.")
        break
    else:
        print("Pilihan tidak valid. Silakan pilih lagi.")