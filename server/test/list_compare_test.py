list1 = ["a","b","c","d","e"]

list2 = [4, 5]


#for data in list2:
    #if data in list1:
        #print(True)
        #break
    #else:
        #print(False)

#print(list1[1:])

#for i in range(1, len(list1)):
    #print("hello"):

target = None
index = 0
count = 0
while True:
    if count > 4:
        break

    for i in range(index, len(list1)):
        target = list1[-(i+1)]
        index = i + 1
        break

    count += 1
    print(index)
    print(target)
