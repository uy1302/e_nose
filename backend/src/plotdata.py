import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dữ liệu
df = pd.read_csv('../data/processed/esp32_data.csv')

# Kiểm tra cấu trúc dữ liệu
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)
print("Unique classes:", df['class'].unique() if 'class' in df.columns else df['label'].unique() if 'label' in df.columns else "No class column found")

# Xác định cột class
class_col = 'class' if 'class' in df.columns else 'label' if 'label' in df.columns else df.columns[-1]
print(f"Using class column: {class_col}")

# Tạo 3D figure
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

# Định nghĩa màu sắc cho mỗi class
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
unique_classes = df[class_col].unique()

# Plot mỗi class với màu khác nhau trong 3D
for i, class_name in enumerate(unique_classes):
    class_data = df[df[class_col] == class_name]
    ax.scatter(class_data['MQ2'], class_data['MQ4'], class_data['MQ7'],
               c=colors[i % len(colors)], 
               label=f'{class_name} (n={len(class_data)})',
               alpha=0.7, 
               s=60)

# Tùy chỉnh 3D plot
ax.set_xlabel('MQ2 (Smoke, Propane, Hydrogen)', fontsize=12)
ax.set_ylabel('MQ4 (Methane, CNG Gas)', fontsize=12) 
ax.set_zlabel('MQ7 (Carbon Monoxide)', fontsize=12)
ax.set_title('3D Scatter Plot: MQ2 vs MQ4 vs MQ7 by Class', fontsize=14, fontweight='bold')

# Đặt legend ở vị trí tốt
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Thêm grid
ax.grid(True, alpha=0.3)

# Xoay view để nhìn rõ hơn
ax.view_init(elev=20, azim=45)

# Thêm thống kê
fig.text(0.02, 0.02, f'Total samples: {len(df)}', fontsize=10)

# Lưu plot
plt.tight_layout()
plt.savefig('../docs/images/mq2_mq4_mq7_3d_scatter_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("3D Plot saved to ../docs/images/mq2_mq4_mq7_3d_scatter_plot.png")

