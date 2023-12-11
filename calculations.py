
mapping_dictionary = {
    (0, 0, 0): 0,
    (0, 0, 1): 1,
    (0, 1, 0): 1,
    (0, 1, 1): 2,
    (1, 0, 0): -2,
    (1, 0, 1): -1,
    (1, 1, 0): -1,
    (1, 1, 1): 0,
}


def convert_to_binary_array(number):
    binary_number = bin(number)[2:]
    array = []
    for each_digit in binary_number:
        array.append(int(each_digit))
    return array



def get_mappings_for_multiplier_bits(bit_array):
    return mapping_dictionary[bit_array[0],bit_array[1],bit_array[2]]


def generate_multiplier(multiplier_as_decimal):
    multiplier_binary_array = convert_to_binary_array(multiplier_as_decimal)
    multiplier_binary_array.insert(0, 0)
    result = []
    temp = []
    for each_bit in multiplier_binary_array:
        temp.append(each_bit)
        if len(temp) == 3:
            result.append(temp)
            temp = temp[:1]
    final_result = []
    for each_bit in result :
        final_result.append(get_mappings_for_multiplier_bits(each_bit))
    return final_result


def approx_compressor(bytes_array, cin):
    x1, x2, x3, x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
    k1 = int(x1 ^ x2)
    k2 = int(x3 ^ x4)
    k1c = int(not k1)
    k2c = int(not k2)
    sum_value = int(k1c or k2c)
    p1 = int(x1 and x2)
    p2 = int(x3 and x4)
    p1c = int(not p1)
    p2c = int(not p2)
    p_or = int(p1c or p2c)
    carry = int(not p_or)
    cout = cin
    return sum_value, cout, carry


multiplier = int(input("Enter the multiplier as Decimal : "))
print(f"Your Multiplier Array is :{generate_multiplier(multiplier)}")


for i in range(5):
    x1 = int(input("Enter the x1 : "))
    x2 = int(input("Enter the x2 : "))
    x3 = int(input("Enter the x3 : "))
    x4 = int(input("Enter the x4 : "))
    cin = int(input("Enter the cin : "))
    bytes_array = [x1,x2,x3,x4]
    sum, cout, carry = approx_compressor(bytes_array, cin)
    print(f"The sum is : {sum}")
    print(f"The cout is : {cout}")
    print(f"The carry is : {carry}")
