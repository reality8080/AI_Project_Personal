import matplotlib.pyplot as plt

# Cài font mặc định Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Dữ liệu mới, thêm Genetic
algorithms = ['BFS', 'DFS', 'UCS', 'IDDFS']
times = [0.000273,0.011306,0.000411,0.000432]

# Tạo biểu đồ
plt.figure(figsize=(8, 5))
colors = ['#FF6F61', '#6BCB77', '#4D96FF', '#FFB74D', '#8E44AD', '#9B59B6']
bars = plt.bar(algorithms, times, color=colors, edgecolor='black', width=0.6)

# Tiêu đề và nhãn trục
plt.title('So sánh thời gian thực hiện các thuật toán Uninformed Search', fontsize=16, fontweight='bold')
plt.xlabel('Thuật toán', fontsize=14)
plt.ylabel('Thời gian (giây)', fontsize=14)

# Hiển thị giá trị trên đỉnh cột
for bar, time in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.00001,
             f'{time:.6f}',
             ha='center', va='bottom',
             fontsize=12, fontweight='bold', color='black')

# Điều chỉnh trục
plt.ylim(0, max(times) + 0.001)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Thêm lưới ngang nhẹ
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()