
list_data = [1, 2,3,4,5,6,7,8,9]

def sample():
    for i, data in enumerate(reversed(list_data)):
        reverse_index = len(list_data) - 1 - i

        if data == 4:
            return reverse_index


index = sample()

reversed_sample = list_data[index:len(list_data)][::-1]

print(reversed_sample)


