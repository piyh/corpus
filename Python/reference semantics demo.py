#reference semantics sucks

array = [1,2,3]

def changesArray(array):
    array.append(4)
    return array

def doesNotChangeArray(array):
    a = array.copy()
    a.append(4)
    return a

print(f'starting {array=}')
doesNotChangeArray(array)
print(f'after calling function that changes copy of an array {array=}')
changesArray(array)
print(f'after calling function that appends an array without copying first {array=}')

number = 5

def changesNumber(number):
    number += 5
    return number
    
print(number)
changesNumber(5)
print(number)