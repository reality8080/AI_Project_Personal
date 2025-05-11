import json
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'

def read_log_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Không thể đọc file {filename} hoặc file rỗng.")
        return []

data = read_log_data('Selections.json')

# Tổng hợp dữ liệu
metrics = {
    'execution_time': {},
    'states_explored': {},
    'path_length': {}
}

for entry in data:
    algo = entry['algorithm']
    for key in metrics:
        value = entry.get(key)
        if value is not None:
            metrics[key].setdefault(algo, []).append(value)

algorithms = sorted(set(algo for metric_data in metrics.values() for algo in metric_data))
x = np.arange(len(algorithms))

# Tính trung bình
avg_metrics = {
    metric: [np.mean(metrics[metric].get(algo, [0])) for algo in algorithms]
    for metric in metrics
}

# Bắt đầu vẽ
fig, ax1 = plt.subplots(figsize=(12, 6))

# Màu sắc và độ rộng
width = 0.35
color_time = '#FF6F61'
color_path = '#2ECC71'
color_states = '#4D96FF'

# Trục trái: thời gian và path_length
bars1 = ax1.bar(x - width/2, avg_metrics['execution_time'], width=width, label='Thời gian (giây)', color=color_time)
bars2 = ax1.bar(x + width/2, avg_metrics['path_length'], width=width, label='Độ dài đường đi', color=color_path)

ax1.set_ylabel('Thời gian (s) / Độ dài đường đi', fontsize=12)
ax1.set_xlabel('Thuật toán', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(algorithms, rotation=45, ha='right')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Trục phải: trạng thái duyệt
ax2 = ax1.twinx()
line = ax2.plot(x, avg_metrics['states_explored'], color=color_states, marker='o',
                label='Số trạng thái duyệt', linewidth=2)
ax2.set_ylabel('Số trạng thái duyệt', fontsize=12)
ax2.tick_params(axis='y')

# Hiển thị nhãn trên cột THỜI GIAN
for bar in bars1:
    value = bar.get_height()
    if value < 0.001:
        label = f'{value:.4f}'
    elif value < 1:
        label = f'{value:.3f}'
    else:
        label = f'{value:.2f}'
    ax1.text(bar.get_x() + bar.get_width()/2, value + 0.00005,
             label, ha='center', fontsize=9)

# Hiển thị nhãn trên cột ĐỘ DÀI ĐƯỜNG ĐI
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
             f'{bar.get_height():.0f}', ha='center', fontsize=9)

# Gộp chú thích
lines = [bars1, bars2, line[0]]
labels = ['Thời gian (giây)', 'Độ dài đường đi', 'Số trạng thái duyệt']
ax1.legend(lines, labels, loc='upper left', fontsize=11)

plt.title('So sánh các thuật toán theo thời gian, trạng thái và độ dài đường đi', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('PNG\\LocalSearch.png')
plt.show()
