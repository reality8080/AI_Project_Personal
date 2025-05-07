import json
import matplotlib.pyplot as plt
import numpy as np

# Cài font mặc định Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Đọc dữ liệu từ file JSON
def read_log_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Không thể đọc file {filename} hoặc file rỗng.")
        return []

# Chuẩn bị dữ liệu cho biểu đồ
data = read_log_data('Selections.json')

# Lấy danh sách các thuật toán duy nhất và thời gian trung bình
algorithm_times = {}
for entry in data:
    algo = entry['algorithm']
    time = entry['execution_time']
    if algo in algorithm_times:
        algorithm_times[algo].append(time)
    else:
        algorithm_times[algo] = [time]

# Tính thời gian trung bình cho mỗi thuật toán
algorithms = list(algorithm_times.keys())
times = [np.mean(algorithm_times[algo]) for algo in algorithms]

# Tạo biểu đồ
plt.figure(figsize=(10, 6))
colors = ['#FF6F61', '#6BCB77', '#4D96FF', '#FFB74D', '#8E44AD', '#9B59B6', '#E74C3C', '#3498DB', '#2ECC71', '#F1C40F', '#E67E22', '#1ABC9C']
bars = plt.bar(algorithms, times, color=colors[:len(algorithms)], edgecolor='black', width=0.6)

# Tiêu đề và nhãn trục
plt.title('So sánh thời gian thực hiện các thuật toán', fontsize=16, fontweight='bold')
plt.xlabel('Thuật toán', fontsize=14)
plt.ylabel('Thời gian (giây)', fontsize=14)

# Hiển thị giá trị trên đỉnh cột
for bar, time in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + max(times) * 0.01,
             f'{time:.6f}',
             ha='center', va='bottom',
             fontsize=12, fontweight='bold', color='black')

# Điều chỉnh trục
plt.ylim(0, max(times) * 1.1)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Thêm lưới ngang nhẹ
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# Lưu biểu đồ
plt.savefig('algorithm_comparison.png')
plt.close()