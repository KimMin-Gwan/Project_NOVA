# Re-importing necessary libraries after environment reset
import matplotlib.pyplot as plt

# Re-defining the algorithm function
def algo(case, start=0):
    weights = [start]
    now_weigh = start
    k = 0

    for i in range(1, len(case)):
        k += case[i]
        next_weight = now_weigh + ((case[i] - case[i - 1]) / (k ** 0.5)) * 0.9

        # 새로운 정규화: 상한선 기반 축소 (threshold=0.5, reduction factor=0.1)
        threshold = 0.5
        if next_weight > threshold:
            next_weight = threshold + (next_weight - threshold) * 0.1

        now_weigh = max(next_weight, 0)  # 음수 값 방지
        weights.append(now_weigh)

    return weights

# Creating datasets for testing
case_increasing_exlarge = [0] + [i * 20 for i in range(1, 18)]  # Large steady increase
case_increasing_large = [0] + [i * 10 for i in range(1, 18)]  # Large steady increase
case_increasing_small = [0] + [i * 2 for i in range(1, 18)]   # Small steady increase
case_up_down_large = [0, 10, 50, 100, 150, 200, 250, 200, 150, 100, 50, 0, 0 , 0 , 0 , 0]  # Large increase, large decrease
case_up_down_small = [0, 10, 20, 30, 40, 50, 60, 50, 40, 30, 20, 10, 0, 0 , 0 , 0 , 0]        # Large increase, small decrease
case_peak_and_fall = [0, 100, 90, 70, 50, 30, 10, 5, 2, 1, 0, 0, 0, 0 , 0 , 0 , 0]            # Peak and gradual fall
case_new_trend = [0, 1, 2, 0, 2, 100, 80, 40, 10, 2, 0, 1, 0, 0 , 0 , 0 , 0]            # Peak and gradual fall
case_sudden_trend = [0, 1, 2, 0, 2, 100, 80, 40, 10, 80, 100, 90, 0, 0 , 0 , 0 , 0]            # Peak and gradual fall

# Running the algorithm for each case
results = {
    "Increasing (ExLarge)" : algo(case_increasing_exlarge),
    "Increasing (Large)": algo(case_increasing_large),
    "Increasing (Small)": algo(case_increasing_small),
    "Up-Down (Large)": algo(case_up_down_large),
    "Up-Down (Small)": algo(case_up_down_small),
    "Peak and Fall": algo(case_peak_and_fall),
    "case_new_trend": algo(case_new_trend),
    "sudden_trend": algo(case_sudden_trend)
}

# Visualizing the results
plt.figure(figsize=(12, 8))
for label, weights in results.items():
    plt.plot(weights, label=label, marker='o')

plt.title("Weight Changes Based on Cases", fontsize=16)
plt.xlabel("Steps", fontsize=14)
plt.ylabel("Weight", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

