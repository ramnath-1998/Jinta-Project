half_adder_full_adder_pairs = []
exact_compressor_columns = []

def convert_to_binary_array(number):
    binary_number = bin(number)[2:]
    array = []
    for each_digit in binary_number:
        array.append(int(each_digit))
    return array

def convert_to_binary_from_binary_array(binary_array):
    binary_string = ''.join(str(bit) for bit in binary_array)
    binary_number = bin(int(binary_string))[2:]
    return binary_number

def calculate_length_of_product(multiplier_array,multiplicand_array,shift):
    for i in range(0,len(multiplier_array)):
        if i == 0 :
            result = len(multiplicand_array)
        else :
            result = result + shift
    result = result + shift
    return result


def final_array_not_contains(pair):
    for each_pair in half_adder_full_adder_pairs:
        for each_value in each_pair:
            if pair == each_value :
                return False
    return True

def add_zeros_to_start_of_array(products_array, length_of_product):
    for each_product in products_array:
       while len(each_product) < length_of_product:
           each_product.insert(0,0)
    return products_array

def add_none_to_end_of_array(products_array, shift):
    for i in range(0,len(products_array)):
        for _ in range(i*shift):
            products_array[i].append(None)
    return products_array
        
def get_columns_from_product_array(product_array):
    columns = []
    number_of_rows = len(product_array[0])
    for i in range(number_of_rows):
        column = []
        for each_product in product_array:
            column.append(each_product[i])
        columns.append(column)
    columns.reverse()
    return columns

def split_column_by_half(column):
    columns = []
    half_length = len(column) // 2
    first_half, second_half = column[:half_length], column[half_length:]
    columns.append(first_half)
    columns.append(second_half)
    return columns

def get_effective_length_of_column(each_half):
    length = 0
    for each_element in each_half:
        if each_element != None :
            length = length + 1
    return length

def multiply_multiplier_digit_with_multiplicand(multiplier_binary_digit, multiplicand_array):
    result_array = []
    for each_digit in multiplicand_array:
        result_array.append(each_digit&multiplier_binary_digit)
    return result_array

def get_splitted_column_array(columns_array):
    result_columns = []
    for each_column in columns_array:
        columns = split_column_by_half(each_column)
        result_columns.append(columns)
    return result_columns

def multiply_multiplier_with_multiplicand(multiplier, multiplicand):
    multiplicand_array = convert_to_binary_array(multiplicand)
    multiplier_array = convert_to_binary_array(multiplier)
    shift = 2
    length_of_product = calculate_length_of_product(multiplier_array, multiplicand_array, shift)
    result_array = []
    for i in range(0,len(multiplier_array)):
        result = multiply_multiplier_digit_with_multiplicand(multiplier_array[i],multiplicand_array)
        result_array.append(result)
    add_none_to_end_of_array(result_array, shift)
    add_zeros_to_start_of_array(result_array, length_of_product)
    return result_array


def add_half_adder_full_adder_pairs(splitted_columns_array):
    for i in range(0,len(splitted_columns_array)):
        for j in range(0,len(splitted_columns_array[i])):
            if is_half_adder_column(get_effective_length_of_column(splitted_columns_array[i][j])) and final_array_not_contains(splitted_columns_array[i][j]):
                half_adder_column = splitted_columns_array[i][j]
                full_adder_column= find_full_adder_column(i, j, splitted_columns_array)
                full_adder_carry_column = find_full_adder_carry_column(i, j, splitted_columns_array)
                if full_adder_column is not None:
                    half_full_pair = [half_adder_column, full_adder_column, full_adder_carry_column,[i,j]]
                    half_adder_full_adder_pairs.append(half_full_pair)
    return half_adder_full_adder_pairs

def add_exact_compressor_columns(splitted_columns_array):
    for i in range(len(splitted_columns_array)):
        for j in range(len(splitted_columns_array[i])):
            length_of_column = get_effective_length_of_column(splitted_columns_array[i][j])
            if length_of_column == 4 and i < len(splitted_columns_array) - 1:
                exact_compressor_columns.append([splitted_columns_array[i][j], splitted_columns_array[i+1][j],[i,j]])
    return exact_compressor_columns


def find_full_adder_column(index_i_of_half_adder_pair,index_j_of_half_adder_pair,columns_array):
    if final_array_not_contains(columns_array[index_i_of_half_adder_pair+1][index_j_of_half_adder_pair]):
        return columns_array[index_i_of_half_adder_pair+1][index_j_of_half_adder_pair]
    return None
def find_full_adder_carry_column(index_i_of_half_adder_pair,index_j_of_half_adder_pair, columns_array):
    if final_array_not_contains(columns_array[index_i_of_half_adder_pair+2][index_j_of_half_adder_pair]):
        return columns_array[index_i_of_half_adder_pair+2][index_j_of_half_adder_pair]
    return None

def is_half_adder_column(effective_length_of_column):
    if effective_length_of_column == 3 :
        return True
    return False

def half_adder(bit1, bit2):
    sum_bit = bit1 ^ bit2
    carry_bit = bit1 & bit2
    return sum_bit, carry_bit

def full_adder(bit1, bit2, carry_in):
    sum_bit_1, carry_1 = half_adder(bit1, bit2)
    sum_bit_2, carry_2 = half_adder(sum_bit_1, carry_in)
    sum_bit = sum_bit_2
    carry_out = carry_1 or carry_2
    return sum_bit, carry_out

def exact_compressor(bytes_array, cin):
    x1,x2,x3,x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
    sum_value = int(x1 ^ x2 ^ x3 ^ x4 ^ cin)
    k = int(x1 ^ x2)
    kc = int(not k)
    r1 = int(k and x3)
    r2 = int(kc and x1)
    cout = int(r1 or r2)
    j = int(x1 ^ x2 ^ x3 ^ x4)
    jc = int(not j)
    j1 = int(j and cin)
    j2 = int(jc and x4)
    carry = int(j1 or j2)
    return sum_value, cout, carry

def approx_compressor(bytes_array, cin):
    x1,x2,x3,x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
    k1 = int(x1 ^ x2)
    k2 = int(x3 ^ x4)
    k1c = int(not k1)
    k2c = int(not k2)
    sum_value= int(k1c or k2c)
    p1 = int(x1 and x2)
    p2 = int(x3 and x4)
    p1c = int(not p1)
    p2c = int(not p2)
    p_or= int(p1c or p2c)
    carry=int(not p_or)
    cout=cin
    return sum_value, cout, carry


def is_input_of_half_adder(byte_array):
    for each_byte_array in half_adder_full_adder_pairs:
        if each_byte_array[0] == byte_array :
            return True, each_byte_array[1]
    return False,None

def is_input_of_full_adder(byte_array):
    for each_byte_array in half_adder_full_adder_pairs:
        if each_byte_array[1] == byte_array:
            return True, each_byte_array[2]
    return False, None
def is_input_of_compressor(byte_array):
    for each_byte_array in exact_compressor_columns:
        if each_byte_array[0] == byte_array:
            return True, each_byte_array[1]
    return False, None

multiplier = 215
multiplicand = 64135
result_array = multiply_multiplier_with_multiplicand(multiplier,multiplicand)

print(f"Result Array : {result_array}")

columns_array = get_columns_from_product_array(result_array)

print(f"Columns Array : {columns_array}")

splitted_columns_array = get_splitted_column_array(columns_array)

print(f"Splitted Columns Array : {splitted_columns_array}")

half_adder_full_adder_pairs =add_half_adder_full_adder_pairs(splitted_columns_array)

print(f"Half Adder Pairs : {half_adder_full_adder_pairs}")

exact_compressor_columns = add_exact_compressor_columns(splitted_columns_array)

print(f"Exact Compressor Columns : {exact_compressor_columns}")

def get_carry_from_carry_array(array_to_get_carry, carry_array):
    for each_array in carry_array:
        if each_array[0] == array_to_get_carry:
            return each_array[1]
    return None



