import pdb
def swap(indices, direction, index):
    if direction[index] == True and index - 1 >= 0:
        tmp1 = indices[index-1]
        tmp2 = direction[index-1]
        indices[index-1] = indices[index]
        direction[index-1] = direction[index]
        indices[index] = tmp1
        direction[index] = tmp2
    elif direction[index] == False and index + 1 <= len(indices)-1:
        tmp1 = indices[index+1]
        tmp2 = direction[index+1]
        indices[index+1] = indices[index]
        direction[index+1] = direction[index]
        indices[index] = tmp1
        direction[index] = tmp2


def reverse(indices, direction, mobile_integer_value):
    i = 0
    while i < len(indices):
        if indices[i] > mobile_integer_value:
            direction[i] =  not direction[i]
        i += 1

def largest_mobile_integer(indices, direction):
    max_index = -1
    max_v = -1
    i = 0
    while i < len(indices):
        if direction[i] == True and i - 1 >= 0:
            if indices[i] > indices[i-1] and indices[i] > max_v:
                max_v = indices[i]
                max_index = i 
        if direction[i] == False and i + 1 <= len(indices) - 1:
            if indices[i] > indices[i+1] and indices[i] > max_v:
                max_v = indices[i]
                max_index = i 
        i += 1
    return max_index

def permutation(l):
    indices = range(len(l))
    direction = [True] * len(l)
    mobile_integer_index = largest_mobile_integer(indices, direction)
    while mobile_integer_index > -1:
        mobile_integer_value = indices[mobile_integer_index]
        swap(indices, direction, mobile_integer_index)
        yield [l[i] for i in indices]
        reverse(indices, direction, mobile_integer_value)
        mobile_integer_index = largest_mobile_integer(indices, direction)


for i in permutation(["a","b","c"]):
    print i
