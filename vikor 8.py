import numpy as np
import pandas as pd

print("\n------------------------------------------------------------------------------")
print(" GREEN SUPPLIER SELECTION BASED ON MULTI CRITERIA DECISION METHOD - VIKOR")
print("-------------------------------------------------------------------------------\n")


# Matriks kriteria
matriks_kriteria = [
    [65300, 60500, 68300, 59000, 63700, 60000, 64000, 62500],
    [218000, 120000, 122000, 120000, 195000, 125000, 115000, 210000],
    [5, 3, 4, 4, 4, 3, 4, 4],
    [0.1, 0, 0.15, 0, 0.15, 0.15, 0, 0],
    [3, 5, 3, 4, 4, 4, 5, 3],
    [4, 4, 3, 4, 3, 4, 3, 4],
    [30, 20, 22, 19, 30, 20, 22, 31],
    [5, 3, 4, 4, 5, 4, 3, 4],
    [3, 3, 3, 3, 3, 5, 3, 4],
    [3, 3, 4, 4, 3, 3, 4, 3],
    [4, 3, 4, 4, 4, 4, 4, 3],
    [3, 3, 4, 5, 3, 4, 4, 4],
    [3, 3, 4, 4, 5, 4, 4, 3],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2]
]

# Bobot dan jenis kriteria
bobot_kriteria = {
    'C1': {'bobot': 0.053, 'jenis': 'benefit'},
    'C2': {'bobot': 0.177, 'jenis': 'benefit'},
    'C3': {'bobot': 0.044, 'jenis': 'benefit'},
    'C4': {'bobot': 0.075, 'jenis': 'benefit'},
    'C5': {'bobot': 0.115, 'jenis': 'cost'},
    'C6': {'bobot': 0.115, 'jenis': 'cost'},
    'C7': {'bobot': 0.038, 'jenis': 'benefit'},
    'C8': {'bobot': 0.126, 'jenis': 'benefit'},
    'C9': {'bobot': 0.063, 'jenis': 'benefit'},
    'C10': {'bobot': 0.025, 'jenis': 'benefit'},
    'C11': {'bobot': 0.075, 'jenis': 'cost'},
    'C12': {'bobot': 0.031, 'jenis': 'benefit'},
    'C13': {'bobot': 0.031, 'jenis': 'benefit'},
    'C14': {'bobot': 0.016, 'jenis': 'cost'},
    'C15': {'bobot': 0.016, 'jenis': 'benefit'},
}

## STEP 1 - 2
# Tampilkan matriks awal dalam bentuk Pandas DataFrame
df_initial_matrix = pd.DataFrame(matriks_kriteria, columns=[f'A{i+1}' for i in range(len(matriks_kriteria[0]))])
df_initial_matrix.index = [f'C{i+1}' for i in range(len(matriks_kriteria))]
print("Matriks Awal:")
print(df_initial_matrix)
print("\n")

# Tampilkan pembobotan tiap kriteria dalam bentuk Pandas DataFrame
df_weight = pd.DataFrame(bobot_kriteria).T[['bobot', 'jenis']]
df_weight.index.name = 'Kriteria'
print("Pembobotan Tiap Kriteria:")
print(df_weight)
print("\n")


## STEP 3
# Inisialisasi array untuk menyimpan solusi ideal positif (fi+) dan solusi ideal negatif (fi-)
fi_plus = []
fi_minus = []

# Hitung nilai fi+ dan fi- untuk setiap kriteria
for i in range(len(matriks_kriteria)):
    values_i = matriks_kriteria[i]

    if bobot_kriteria[f'C{i+1}']['jenis'] == 'benefit':
        fi_plus.append(max(values_i))
        fi_minus.append(min(values_i))
    elif bobot_kriteria[f'C{i+1}']['jenis'] == 'cost':
        fi_plus.append(min(values_i))
        fi_minus.append(max(values_i))

# Tampilkan hasilnya dalam bentuk Pandas DataFrame dengan nilai desimal
df_result = pd.DataFrame({
    'Kriteria': list(bobot_kriteria.keys()),
    'fi+ (Solusi Ideal Positif)': [float("{:.6f}".format(val)) for val in fi_plus],
    'fi- (Solusi Ideal Negatif)': [float("{:.6f}".format(val)) for val in fi_minus]
})

# Set Kriteria sebagai indeks
df_result.set_index('Kriteria', inplace=True)

# Tampilkan hasilnya
print("Solusi Ideal Positif (fi+), Solusi Ideal Negatif (fi-):")
print(df_result)
print("\n")


## STEP 4
# Matriks X
matriks_X = np.array(matriks_kriteria)

# Normalisasi matriks X
normalized_matrix = np.zeros_like(matriks_X, dtype=float)

for i in range(len(matriks_kriteria)):
    f_plus_i = fi_plus[i]
    f_minus_i = fi_minus[i]

    for j in range(len(matriks_kriteria[0])):
        f_ij = matriks_X[i, j]

        # Penanganan nilai NaN dan nilai normalisasi tidak kurang dari 0
        if f_plus_i == f_minus_i:
            normalized_matrix[i, j] = 0
        else:
            normalized_matrix[i, j] = max(0, (f_plus_i - f_ij) / (f_plus_i - f_minus_i))

# Tampilkan hasil normalisasi dalam bentuk Pandas DataFrame dengan nilai desimal
df_normalized = pd.DataFrame(normalized_matrix, columns=[f'A{i+1}' for i in range(len(matriks_kriteria[0]))])

# Set Kriteria sebagai indeks
df_normalized.index = list(bobot_kriteria.keys())

# Tampilkan hasilnya
print("Matriks X yang sudah dinormalisasi:")
print(df_normalized)


## STEP 5
# Inisialisasi array untuk menyimpan nilai terbobot
weighted_values = []

# Hitung nilai terbobot untuk setiap kriteria
for i in range(len(bobot_kriteria)):
    weights_i = bobot_kriteria[f'C{i+1}']['bobot']

    for j in range(len(matriks_kriteria[0])):
        normalized_value_ij = normalized_matrix[i, j]

        # Hitung nilai terbobot menggunakan rumus F_ij = w_(j^.) * N_ji
        weighted_value_ij = weights_i * normalized_value_ij
        weighted_values.append(weighted_value_ij)

# Reshape array menjadi matriks dengan ukuran yang sama seperti matriks X
weighted_matrix = np.array(weighted_values).reshape(normalized_matrix.shape)

# Tampilkan hasil nilai terbobot dalam bentuk Pandas DataFrame dengan nilai desimal
df_weighted = pd.DataFrame(weighted_matrix, columns=[f'A{i+1}' for i in range(len(matriks_kriteria[0]))])

# Set Kriteria sebagai indeks
df_weighted.index = list(bobot_kriteria.keys())

# Tampilkan hasilnya
print("\n")
print("Matriks X yang sudah dinormalisasi dan nilai terbobot:")
print(df_weighted)

## STEP 6
# Menghitung Nilai Utility Measure (S) dan Regret Measure (R)
S_values = []
R_values = []

for j in range(len(matriks_kriteria[0])):
    # Menghitung Nilai Utility Measure (S) untuk setiap alternatif
    S_j = sum(weighted_matrix[i, j] for i in range(len(bobot_kriteria)))
    S_values.append(S_j)

    # Menghitung Regret Measure (R) untuk setiap alternatif
    R_j = max(weighted_matrix[i, j] for i in range(len(bobot_kriteria)))
    R_values.append(R_j)

# Tampilkan hasil Nilai Utility Measure (S) dalam bentuk Pandas DataFrame dengan nilai desimal
df_S = pd.DataFrame({'Nilai Utility Measure (S)': [float("{:.6f}".format(val)) for val in S_values]})
df_S.index = [f'A{i+1}' for i in range(len(matriks_kriteria[0]))]

# Tampilkan hasilnya
print("\n")
print("Nilai Utility Measure (S):")
print(df_S)

# Tampilkan hasil Regret Measure (R) dalam bentuk Pandas DataFrame dengan nilai desimal
df_R = pd.DataFrame({'Regret Measure (R)': [float("{:.6f}".format(val)) for val in R_values]})
df_R.index = [f'A{i+1}' for i in range(len(matriks_kriteria[0]))]

# Tampilkan hasilnya
print("\n")
print("Regret Measure (R):")
print(df_R)


## STEP 7
# Menghitung nilai indeks VIKOR (Q)
v = 0.5  # Anda dapat mengganti nilai v sesuai kebutuhan

Q_values = []

# Menghitung nilai indeks VIKOR (Q) untuk setiap alternatif
for j in range(len(matriks_kriteria[0])):
    S_j = S_values[j]
    R_j = R_values[j]

    S_plus = max(S_values)
    S_minus = min(S_values)
    R_plus = max(R_values)
    R_minus = min(R_values)

    Q_j = (v * ((S_j - S_minus) / (S_plus - S_minus))) + ((1 - v) * ((R_j - R_minus) / (R_plus - R_minus)))
    Q_values.append(Q_j)

# Tampilkan hasil nilai indeks VIKOR (Q) dalam bentuk Pandas DataFrame dengan nilai desimal
df_Q = pd.DataFrame({'Nilai Indeks VIKOR (Q)': [float("{:.6f}".format(val)) for val in Q_values]})
df_Q.index = [f'A{i+1}' for i in range(len(matriks_kriteria[0]))]

# Tampilkan hasilnya
print("\n")
print("Nilai Indeks VIKOR (Q):")
print(df_Q)


## STEP 8
# Mengurutkan nilai indeks VIKOR (Q) dari terkecil ke terbesar
df_ranking = df_Q.sort_values(by='Nilai Indeks VIKOR (Q)')

# Tampilkan hasil peringkat dalam bentuk Pandas DataFrame
df_ranking['Peringkat'] = range(1, len(df_ranking) + 1)  # Tambahkan kolom Peringkat
df_ranking['Keterangan'] = pd.cut(df_ranking['Nilai Indeks VIKOR (Q)'], bins=len(df_ranking),
                                  labels=['Terbaik'] + ['Baik'] * (len(df_ranking) - 1),
                                  include_lowest=True, ordered=False)

# Tampilkan hasil peringkat dengan keterangan dalam bentuk Pandas DataFrame
print("\n")
print("Peringkat berdasarkan Nilai Indeks VIKOR (Q) dengan Keterangan:")
print(df_ranking[['Nilai Indeks VIKOR (Q)', 'Peringkat', 'Keterangan']])








