


# Data Cleaning:
# Identifikasi dan penanganan data yang hilang, duplikat, atau tidak valid. Misalnya, jika terdapat penilaian yang hilang, Anda perlu memutuskan apakah akan mengisi nilai yang hilang atau memperlakukan data tersebut secara berbeda.

# Data Normalization:
# Mengubah data ke dalam skala yang seragam. Ini penting untuk mencegah perbedaan skala yang dapat mempengaruhi kualitas rekomendasi. Misalnya, mengubah peringkat pengguna ke dalam skala antara 0 dan 1.

# User-Item Matrix Creation:
# Membentuk matriks pengguna-item, di mana setiap baris mewakili pengguna dan setiap kolom mewakili item. Entri matriks dapat berisi informasi seperti peringkat atau interaksi pengguna dengan item. Matriks ini merupakan dasar untuk algoritma collaborative filtering.

# Feature Engineering:
# Menciptakan fitur tambahan yang dapat meningkatkan kualitas rekomendasi. Ini bisa berupa informasi tentang pengguna (misalnya, lokasi, usia) atau informasi tentang item (misalnya, genre film). Fitur-fitur ini dapat membantu model rekomendasi memahami preferensi pengguna dengan lebih baik.

# Handling Sparse Data:
# Jika terdapat banyak entri yang hilang dalam matriks pengguna-item, diperlukan strategi untuk mengatasi masalah data yang tidak lengkap. Teknik seperti imputasi (mengisi nilai yang hilang dengan nilai perkiraan) dapat digunakan.