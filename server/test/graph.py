import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 데이터 생성
users = np.linspace(1000, 20000, 100)  # 사용자 수
advertisers = np.linspace(1, 100, 100)  # 광고주 수
users, advertisers = np.meshgrid(users, advertisers)
exposure_rate = (5 / advertisers) * (users * 5 / (advertisers * users * 5))  # 노출률 계산





# 3D 그래프 생성
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(users, advertisers, exposure_rate, cmap='viridis')
ax.set_xlabel('User Count')
ax.set_ylabel('Advertiser Count')
ax.set_zlabel('Exposure Rate')
plt.show()