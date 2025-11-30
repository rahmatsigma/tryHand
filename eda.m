% 1. Membaca Data
data = readtable('youth_unemployment_global.csv');

% Menampilkan 5 baris pertama untuk pengecekan
disp(head(data));

% 2. Membersihkan Data (Hapus baris yang kosong pada kolom YouthUnemployment)
data = data(~isnan(data.YouthUnemployment), :);

% 3. Analisis Tren Global (Rata-rata per Tahun)
years = unique(data.Year);
avg_unemployment = zeros(length(years), 1);

for i = 1:length(years)
    idx = data.Year == years(i);
    avg_unemployment(i) = mean(data.YouthUnemployment(idx));
end

% Plot Tren Global
figure;
plot(years, avg_unemployment, '-o', 'LineWidth', 2);
title('Tren Rata-rata Pengangguran Pemuda Global');
xlabel('Tahun');
ylabel('Rata-rata Pengangguran (%)');
grid on;

% 4. Top 5 Negara dengan Pengangguran Tertinggi (Rata-rata)
countries = unique(data.Country);
avg_by_country = zeros(length(countries), 1);

for i = 1:length(countries)
    idx = strcmp(data.Country, countries{i});
    avg_by_country(i) = mean(data.YouthUnemployment(idx));
end

% Membuat tabel ringkasan
T = table(countries, avg_by_country);
T = sortrows(T, 'avg_by_country', 'descend'); % Urutkan dari terbesar
top5 = T(1:5, :);

% Plot Bar Chart Top 5
figure;
bar(categorical(top5.countries), top5.avg_by_country);
title('Top 5 Negara dengan Pengangguran Pemuda Tertinggi');
ylabel('Rata-rata Pengangguran (%)');