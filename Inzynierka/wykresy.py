import matplotlib.pyplot as plt

# symbols_count = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# ocr_times = [34, 37, 40, 51, 56, 70, 70, 70, 81, 87]
#
# plt.figure(figsize=(8, 5))
# plt.scatter(symbols_count, ocr_times, color='blue', label="Autorski OCR")
#
# plt.xlabel("Liczba symboli w równaniu")
# plt.ylabel("Czas rozpoznawania (ms)")
# plt.title("Zależność czasu rozpoznawania od liczby symboli")
#
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.show()
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.where(x == 0, 0, x**x)
lower_bound = 0
upper_bound = 4
num_samples = 10000

x_samples = np.random.uniform(lower_bound, upper_bound, num_samples)

y_samples = f(x_samples)

integral_value = (upper_bound - lower_bound) * np.mean(y_samples)

x = np.linspace(lower_bound, upper_bound, 500)
y = f(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='$f(x) = x^x$', color='blue')
plt.fill_between(x, y, alpha=0.2, color='blue', label='Obszar pod krzywą')

num_plot_samples = 5000
x_plot_samples = np.random.uniform(lower_bound, upper_bound, num_plot_samples)
y_plot_samples = np.random.uniform(0, np.max(y), num_plot_samples)

under_curve = y_plot_samples <= f(x_plot_samples)
plt.scatter(x_plot_samples[under_curve], y_plot_samples[under_curve], color='green', s=10, label='Punkty pod krzywą')
plt.scatter(x_plot_samples[~under_curve], y_plot_samples[~under_curve], color='red', s=10, label='Punkty nad krzywą')

plt.title('Całkowanie Monte Carlo dla funkcji $f(x) = x^x$ od 0 do 4')
plt.xlabel('$x$')
plt.ylabel('$f(x)$')
plt.legend()
plt.grid(True)
plt.show()