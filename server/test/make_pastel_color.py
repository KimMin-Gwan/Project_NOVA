import random

def generate_vivid_pastel_color():
    # 더 쨍하고 밝은 색상을 위해 범위 설정
    r = random.randint(170, 255)  # 밝은 색상 범위
    g = random.randint(170, 255)
    b = random.randint(170, 255)
    
    # 흰색과의 혼합을 줄여 더 선명한 색상 유지
    r = (r * 3 + 255) // 4
    g = (g * 3 + 255) // 4
    b = (b * 3 + 255) // 4
    
    return f'#{r:02x}{g:02x}{b:02x}'

# 색상 코드 생성 예시
for _ in range(5):  # 5개의 색상 코드 생성
    print(generate_vivid_pastel_color())
