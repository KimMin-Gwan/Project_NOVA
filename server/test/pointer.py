

def func1():
    print("hello")
    return

def func2():
    return func1

get = func2()

print(get)


#1. hello
#2. func2의 주소 출력
#3. fucn1의 주소 출력