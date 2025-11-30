clear; clc; close all;

% --- Inisialisasi ---
x0 = 3.0;           % Nilai tebakan awal (akar ada di antara 2 dan 3)
tol = 1e-8;         % Toleransi error
max_iter = 100;     % Maksimum iterasi

% --- Persiapan Penyimpanan Hasil ---
x_history = zeros(max_iter + 1, 1);
error_history = zeros(max_iter, 1);
x_history(1) = x0;
iter_count = 0;

% --- Proses Iterasi Titik Tetap ---
fprintf('Iterasi\t x\t\t Error Relatif\n');
fprintf('%d\t %.8f\n', 0, x0);

for i = 1:max_iter
    x_new = g3(x_history(i)); % Hitung x baru: x_new = g(x_old)
    x_history(i+1) = x_new;
    iter_count = i;
    
    % Hitung error relatif
    rel_error = abs((x_new - x_history(i)) / x_new);
    error_history(i) = rel_error;
    
    fprintf('%d\t %.8f\t %.2e\n', i, x_new, rel_error);
    
    % Cek kondisi berhenti
    if rel_error < tol
        break;
    end
end

% Rapikan data history sesuai jumlah iterasi
x_history = x_history(1:iter_count+1);
error_history = error_history(1:iter_count);
akar = x_history(end);

fprintf('\nKonvergensi tercapai.\n');
fprintf('Akar (x) = %.8f\n', akar);
fprintf('Error Relatif = %.2e\n', rel_error);
fprintf('Jumlah Iterasi = %d\n', iter_count);

% --- Plot 1: x vs Iterasi ---
figure;
plot(0:iter_count, x_history, 'mo-', 'LineWidth', 1.5, 'MarkerFaceColor', 'm');
title('Plot Nilai x vs. Iterasi (Soal 3)');
xlabel('Iterasi (n)');
ylabel('Nilai x_n');
grid on;

% --- Plot 2: y=g(x) dan y=x ---
figure;
% Tentukan rentang plot di sekitar akar
x_range = linspace(akar - 2, akar + 2, 200);
y_g = g3(x_range);
y_x = x_range;

plot(x_range, y_g, 'r-', 'LineWidth', 2, 'DisplayName', 'y = g(x) = 4 - ln(x)');
hold on;
plot(x_range, y_x, 'b--', 'LineWidth', 2, 'DisplayName', 'y = x');
plot(akar, g3(akar), 'ko', 'MarkerSize', 10, 'MarkerFaceColor', 'k', 'DisplayName', 'Akar (Titik Tetap)');
title('Plot y = g(x) dan y = x (Soal 3)');
xlabel('x');
ylabel('y');
legend('show');
grid on;
axis equal;
hold off;