import math
import matplotlib.pyplot as plt

# 從鍵盤輸入半徑
radius = float(input("請輸入圓的半徑: "))

# 計算圓面積
area = math.pi * (radius ** 2)
print("圓的面積是:", area)

# 畫出圓形
circle = plt.Circle((0, 0), radius, color='blue', fill=False)
fig, ax = plt.subplots()
ax.add_artist(circle)
ax.set_xlim(-radius-1, radius+1)
ax.set_ylim(-radius-1, radius+1)
ax.set_aspect('equal', 'box')
plt.title("圓形圖")
plt.xlabel("X軸")
plt.ylabel("Y軸")
plt.grid(True)
plt.show()
