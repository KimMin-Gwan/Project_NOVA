import copy


list1 = ["1", "2", "3", "4", "5"]
list2 = ["a", "b", "c", "d", "e"]


list3 = copy.copy(list1)

list3.append("6")
print(list1)
print(list3)