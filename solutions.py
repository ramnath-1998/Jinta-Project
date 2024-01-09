def convert_to_binary_array(number):
    binary_number = bin(number)[2:]
    array = []
    for each_digit in binary_number:
        array.append(int(each_digit))
    while len(array) < 16:
        array.insert(0,0)
    return array
print(convert_to_binary_array(3))