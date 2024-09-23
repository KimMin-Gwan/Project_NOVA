
from typing import Any
from random import randint
import sys
import os
import time


sample_list = []

class Sample:
    def __init__(self, content):
        self.content = content
        self.flag = False

    def __call__(self):
        print(self.content)

def make_init_data():
    content_list = [1,2,3,4,5]

    for target in content_list:
        num = 0
        while True:
            if num == 25:
                break
            sample =Sample(content=target)
            sample_list.append(sample)
            num += 1


make_init_data()

# 아래에 마저 작성
# 이쁘게 열을 맞춰서 25개씩 출력할것
def printing():
    for i, sample in enumerate(sample_list, start=1):
        # sample 객체를 호출하여 content 출력
        print(sample.content, sample.flag, end=" ")

        # 25개마다 줄 바꿈
        if i % 25 == 0:
            print()  # 줄 바꿈


def dice_argo(option):
    len_option = len(option)
    key = randint(0, 1000)
    target = key % len_option
    result = option[target]
    return result

def pick_something(target): 
    for sample in sample_list:
        if sample.flag:
            continue
        if sample.content == target:
            sample.flag = True
            return

    for sample in sample_list:
        if sample.flag:
            continue
        sample.flag = True
        break
    return


def start():
    option = [1,2,2,2,1]
    for _ in sample_list:
        time.sleep(0.1)
        os.system("cls")
        result = dice_argo(option=option)
        pick_something(target=result)
        printing()


start()

