import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def exact_compressor_final(multiplier,multiplicand):
    half_adder_full_adder_pairs = []
    exact_compressor_columns = []
    def twos_complement(binary_array):
        complement = [1 if bit == 0 else 0 for bit in binary_array]
        carry = 1
        for i in range(len(complement) - 1, -1, -1):
            if complement[i] == 0 and carry == 1:
                complement[i] = 1
                carry = 0
            elif complement[i] == 1 and carry == 1:
                complement[i] = 0
        return complement

    def left_shift_binary_array(binary_array, shift_amount):
        shifted_array = binary_array[shift_amount:] + [0] * shift_amount
        return shifted_array


    def multiply_multiplier_with_multiplicand(multiplier, multiplicand):
        multiplicand_array = convert_to_binary_array(multiplicand)
        multiplier_array = generate_multiplier(multiplier)
        shift = 2
        length_of_product = calculate_length_of_product(
            multiplier_array, multiplicand_array, shift
        )
        result_array = []
        for i in range(0, len(multiplier_array)):
            result = multiply_multiplier_digit_with_multiplicand(
                multiplier_array[i], multiplicand_array
            )
            result_array.append(result)
        add_none_to_end_of_array(result_array, shift)
        add_zeros_to_start_of_array(result_array, length_of_product)
        return result_array


    def multiply_multiplier_digit_with_multiplicand(
        multiplier_binary_digit, multiplicand_array
    ):
        result_array = []
        if multiplier_binary_digit == 0 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == -1 :
            result_array = twos_complement(multiplicand_array)
        elif multiplier_binary_digit == 1 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == 2 :
            result_array = left_shift_binary_array(multiplicand_array,1)
        elif multiplier_binary_digit == -2 :
            two_s_complement = twos_complement(multiplicand_array)
            two_s_complement.append(0)
            result_array = two_s_complement
        return result_array
 
    def fill_start_with_zeros(array,array_length):
        while len(array) < array_length:
            array.insert(0,0)
        return array
    
    def convert_to_binary_array(number):
        binary_number = bin(number)[2:]
        array = []
        for each_digit in binary_number:
            array.append(int(each_digit))
        array = fill_start_with_zeros(array, 16)
        return array

    def convert_to_binary_from_binary_array(binary_array):
        binary_string = "".join(str(bit) for bit in binary_array)
        binary_number = int(binary_string)
        return binary_number


    def calculate_length_of_product(multiplier_array, multiplicand_array, shift):
        for i in range(0, len(multiplier_array)):
            if i == 0:
                result = len(multiplicand_array)
            else:
                result = result + shift
        result = result + shift
        return result


    def generate_multiplier(multiplier_as_decimal):
        multiplier_binary_array = convert_to_binary_array(multiplier_as_decimal)
        multiplier_binary_array = fill_start_with_zeros(multiplier_binary_array,16)
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


    def get_mappings_for_multiplier_bits(bit_array):
        return mapping_dictionary[bit_array[0],bit_array[1],bit_array[2]]




    def add_zeros_to_start_of_array(products_array, length_of_product):
        for each_product in products_array:
            while len(each_product) < length_of_product:
                each_product.insert(0, 0)
        return products_array


    def add_none_to_end_of_array(products_array, shift):
        for i in range(0, len(products_array)):
            for _ in range(i * shift):
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


    def get_splitted_column_array(columns_array):
        result_columns = []
        for each_column in columns_array:
            columns = split_column_by_half(each_column)
            result_columns.append(columns)
        return result_columns


    def get_effective_length_of_column(each_half):
        length = 0
        for each_element in each_half:
            if each_element != None:
                length = length + 1
        return length


    def add_exact_compressor_columns(splitted_columns_array):
        for i in range(len(splitted_columns_array)):
            for j in range(len(splitted_columns_array[i])):
                length_of_column = get_effective_length_of_column(
                    splitted_columns_array[i][j]
                )

                if i == len(splitted_columns_array)-1:
                    
                    exact_compressor_columns.append([splitted_columns_array[i][j],
                    [None,None,None,None],
                    [i,j]])
                if length_of_column == 4 and i < len(splitted_columns_array)-1:
                    exact_compressor_columns.append(
                        [
                            splitted_columns_array[i][j],
                            splitted_columns_array[i + 1][j],
                            [i, j],
                        ]
                    )
        return exact_compressor_columns


    def add_half_adder_full_adder_pairs(splitted_columns_array):
        for i in range(0, len(splitted_columns_array)):
            for j in range(0, len(splitted_columns_array[i])):
                if is_half_adder_column(get_effective_length_of_column(splitted_columns_array[i][j])) and half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
                    half_adder_column = splitted_columns_array[i][j]
                    full_adder_column = find_full_adder_column(i, j, splitted_columns_array)
                    full_adder_carry_column = find_full_adder_carry_column(i, j, splitted_columns_array)
                    if full_adder_column is not None:
                        half_full_pair = [
                            half_adder_column,
                            full_adder_column,
                            full_adder_carry_column,
                            [i, j],]
                        half_adder_full_adder_pairs.append(half_full_pair)
        return half_adder_full_adder_pairs


    def is_half_adder_column(effective_length_of_column):
        if effective_length_of_column == 3:
            return True
        return False


    def half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return False
        return True


    def find_full_adder_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        if get_effective_length_of_column(columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]) == 3 and half_adder_full_adder_pair_array_not_contains(index_i_of_half_adder_pair, index_j_of_half_adder_pair, half_adder_full_adder_pairs):
            return columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]
        


    def find_full_adder_carry_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        return columns_array[index_i_of_half_adder_pair + 2][index_j_of_half_adder_pair]




    def get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return each_pair
        return None


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
        x1, x2, x3, x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
        sum = int(x1 or x2 or x3 or x4 or cin)
        k1 = int(x1 ^ x2)
        k2 = int(k1 and x3)
        k3 = int(k2 and x1)
        k4 = int(not k3)
        cout = int(k2 or k4)
        d1 = int(x1 ^ x2 ^ x3 ^ x4)
        d2 = int(d1 and cin)
        d3 = int(d1 and x4)
        d4 = int(not d3)
        carry = int(d2 or d4)
        return sum,cout,carry

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

    def get_cout_from_cout_array(i, j, cout_array):
        for each_cout in cout_array:
            if each_cout[0] == [i, j]:
                return each_cout[1]
        return None


    def result_already_present(key_tuple, result):
        if key_tuple in result:
            return True
        return False


    def get_exact_compressor_pairs(i_of_pair, j_of_pair,exact_compressor_columns):
        for i in range(len(exact_compressor_columns)):
            each_pair = exact_compressor_columns[i]
            if each_pair[2] == [i_of_pair, j_of_pair]:
                return each_pair






    result_array = multiply_multiplier_with_multiplicand(multiplier,multiplicand)



    columns_array = get_columns_from_product_array(result_array)



    splitted_columns_array = get_splitted_column_array(columns_array)



    half_adder_full_adder_pairs = add_half_adder_full_adder_pairs(splitted_columns_array)


    exact_compressor_columns = add_exact_compressor_columns(splitted_columns_array)



    result = {}
    cout_array = []


    for i in range(len(splitted_columns_array)):
        for j in range(len(splitted_columns_array[i])):
            byte_array = splitted_columns_array[i][j]
            if get_effective_length_of_column(byte_array) == 1:
                sum = byte_array[0]
                result[i, j] = [sum, None]
            elif get_effective_length_of_column(byte_array) == 2:
                sum = byte_array[0]
                carry = byte_array[1]
                result[i, j] = [sum, carry]
            elif (
                get_effective_length_of_column(byte_array) == 3
                and half_adder_full_adder_pair_array_not_contains(i, j,half_adder_full_adder_pairs) is not True
            ):
            
                half_full_adder_array = get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs)
                half_adder_pair, i_half_adder_pair, j_half_adder_pair = (
                    half_full_adder_array[0],
                    i,
                    j,
                )
                full_adder_pair, i_full_adder_pair, j_full_adder_pair = (
                    half_full_adder_array[1],
                    i + 1,
                    j,
                )
                full_adder_carry_pair, i_full_adder_carry_pair, j_full_adder_carry_pair = (
                    half_full_adder_array[2],
                    i + 2,
                    j,
                )
                half_adder_bit_1 = half_adder_pair[0]
                half_adder_bit_2 = half_adder_pair[1]
                half_adder_sum, half_adder_carry = half_adder(
                    half_adder_bit_1, half_adder_bit_2
                )
                result[i_half_adder_pair, j_half_adder_pair] = [
                    half_adder_sum,
                    half_adder_carry,
                ]
                full_adder_bit_1 = full_adder_pair[0]
                full_adder_bit_2 = full_adder_pair[1]
                full_adder_sum, full_adder_carry = full_adder(
                    full_adder_bit_1, full_adder_bit_2, half_adder_carry
                )
                result[i_full_adder_pair, j_full_adder_pair] = [
                    full_adder_sum,
                    full_adder_carry,
                ]
                sum_exact, cout_exact, carry_exact = exact_compressor(
                    full_adder_carry_pair, full_adder_carry
                )
                result[i_full_adder_carry_pair, j_full_adder_carry_pair] = [
                    sum_exact,
                    carry_exact,
                ]
                cout_array.append(
                    [[i_full_adder_carry_pair, j_full_adder_carry_pair], cout_exact]
                )
            elif (
                get_effective_length_of_column(byte_array) == 4
                and result_already_present((i, j),result) is not True
                and (i and j) <= len(exact_compressor_columns)
            ):
                if i < len(splitted_columns_array)-1 :
                    exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                    if exact_compressor_pair_array is not None:
                        first_pair = exact_compressor_pair_array[0]
                        second_pair = exact_compressor_pair_array[1]
                        i_first_pair, j_first_pair = i, j
                        i_second_pair, j_second_pair = i + 1, j
                        c_in_of_first_pair = get_cout_from_cout_array(i - 1, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            cout_array.append(
                                [[i_second_pair, j_second_pair], cout_exact_second]
                            )
                if i == len(splitted_columns_array)-1 :
                        first_pair = exact_compressor_pair_array[0]
                        i_first_pair, j_first_pair = i, j
                        c_in_of_first_pair = get_cout_from_cout_array(i - 1, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]



    def generate_columns_before_cpa(result):
        columns = []
        for i in range(len(splitted_columns_array)):
            column_1 = result[i,0]
            column_2 = [None,None]
            if result_already_present((i,j),result):
                column_2 = result[i,1]
            column = [column_1[0],column_1[1],column_2[0],column_2[1]]
            columns.append(column)
        return columns


    splitted_columns_array_final = generate_columns_before_cpa(result)


    half_adder_full_adder_pairs_final = []
    exact_compressor_pairs_final = []

    def not_exists_in_half_adder_pairs_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            if index in each_pair[3]:
                return False
        return True

    def get_half_adder_full_adder_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if get_effective_length_of_column(each_column) == 3 and not_exists_in_half_adder_pairs_final(i):
                full_adder_pair = splitted_columns_array_final[i+1]
                full_adder_carry_pair = splitted_columns_array_final[i+2]
                half_adder_full_adder_pairs_final.append([each_column,full_adder_pair,full_adder_carry_pair,[i, i+1, i+2]])
        return half_adder_full_adder_pairs_final

    def get_exact_compressor_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if i == len(splitted_columns_array_final) - 1:
                exact_compressor_pairs_final.append([each_column,None,i])
            else:
                if get_effective_length_of_column(each_column) == 4:
                    next_column = splitted_columns_array_final[i+1]
                    exact_compressor_pairs_final.append([each_column,next_column,i])
        return exact_compressor_pairs_final

    half_adder_full_adder_pairs_final = get_half_adder_full_adder_pairs_final(splitted_columns_array_final)

    exact_compressor_pairs_final = get_exact_compressor_pairs_final(splitted_columns_array_final)


    def half_adder_full_adder_pair_final_not_contains(i):
        for each_array in half_adder_full_adder_pairs_final:
            if each_array[3] == i :
                return False
        return True


    cout_array_final = []


    def get_half_adder_full_adder_pair_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            i = each_pair[3][0]
            if i == index:
                return each_pair
        

    result_final = {}

    def get_cary_in_from_cout_final_array(index):
        for each_array in cout_array_final :
            if each_array[0] == index:
                return each_array[1]


    def get_exacy_compressor_pair_final(index):
        for each_pair in exact_compressor_pairs_final:
            if each_pair[2] == index:
                return each_pair


    for i in range(len(splitted_columns_array_final)):
        current_column = splitted_columns_array_final[i]
        i_of_next_column, j_of_next_column = i+1, j+1
        if get_effective_length_of_column(current_column) == 1:
            sum = current_column[0]
            result_final[i]=[sum,None]
        elif get_effective_length_of_column(current_column) == 2 :
            sum = current_column[0]
            carry = current_column[1]
            result_final[i]=[sum,carry]
        elif get_effective_length_of_column(current_column)== 3 and not result_already_present(i,result_final):
            result = get_half_adder_full_adder_pair_final(i)
            half_adder_pair = result[0]
            full_adder_pair = result[1]
            full_adder_carry_pair = result[2]
            i_half_adder_pair, i_full_adder_pair, i_full_adder_carry_pair = result[3][0],result[3][1],result[3][2]
            sum_half_adder, cout_half_adder = half_adder(half_adder_pair[0], half_adder_pair[1])
            carry_half_adder = half_adder_pair[2]
            sum_full_adder, cout_full_adder = full_adder(full_adder_pair[0],full_adder_pair[1],cout_half_adder)
            carry_full_adder = full_adder_pair[2]
            result_final[i_half_adder_pair] = [sum_half_adder,carry_half_adder]
            result_final[i_full_adder_pair] = [sum_full_adder,carry_full_adder]
            sum_final_carry,cout_final_carry,carry_final_carry = exact_compressor(full_adder_carry_pair,cout_full_adder)
            result_final[i_full_adder_carry_pair] = [sum_final_carry,carry_final_carry]
            cout_array_final.append([i_full_adder_carry_pair, cout_final_carry])
        elif get_effective_length_of_column(current_column) == 4 and not result_already_present(i, result_final):
            exact_compressor_pair = get_exacy_compressor_pair_final(i)
            next_column = exact_compressor_pair[1]
            c_in_first_column = get_cary_in_from_cout_final_array(i-1)
            sum_first_array, cout_first_array, carry_first_array = exact_compressor(current_column,c_in_first_column)
            result_final[i] = [sum_first_array,carry_first_array]
            if i != len(splitted_columns_array_final) - 1:
                sum_second_array, cout_second_array, carry_second_array = exact_compressor(next_column,cout_first_array)
                cout_array_final.append([i,cout_second_array])
                result_final[i] = [sum_second_array,carry_second_array]

    final_bit_array = []

    for i in range(len(splitted_columns_array_final)):
        final_result_bits = result_final[i]
        if final_result_bits[1] is not None:
            final_sum = final_result_bits[0] or final_result_bits[1]
            final_bit_array.append(final_sum)
        else :
            final_bit_array.append(final_result_bits[0])



    def convert_bin_array_to_decimal(bin_array):
        value =0 
        for i in range(len(bin_array)):
            digit = bin_array.pop()
            if digit == 1:
                value = value + pow(2, i)
        return value


    return convert_bin_array_to_decimal(final_bit_array)



def approximate_compressor_final(multiplier,multiplicand):
    half_adder_full_adder_pairs = []
    exact_compressor_columns = []
    def twos_complement(binary_array):
        complement = [1 if bit == 0 else 0 for bit in binary_array]
        carry = 1
        for i in range(len(complement) - 1, -1, -1):
            if complement[i] == 0 and carry == 1:
                complement[i] = 1
                carry = 0
            elif complement[i] == 1 and carry == 1:
                complement[i] = 0
        return complement

    def left_shift_binary_array(binary_array, shift_amount):
        shifted_array = binary_array[shift_amount:] + [0] * shift_amount
        return shifted_array


    def multiply_multiplier_with_multiplicand(multiplier, multiplicand):
        multiplicand_array = convert_to_binary_array(multiplicand)
        multiplier_array = generate_multiplier(multiplier)
        shift = 2
        length_of_product = calculate_length_of_product(
            multiplier_array, multiplicand_array, shift
        )
        result_array = []
        for i in range(0, len(multiplier_array)):
            result = multiply_multiplier_digit_with_multiplicand(
                multiplier_array[i], multiplicand_array
            )
            result_array.append(result)
        add_none_to_end_of_array(result_array, shift)
        add_zeros_to_start_of_array(result_array, length_of_product)
        return result_array


    def multiply_multiplier_digit_with_multiplicand(
        multiplier_binary_digit, multiplicand_array
    ):
        result_array = []
        if multiplier_binary_digit == 0 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == -1 :
            result_array = twos_complement(multiplicand_array)
        elif multiplier_binary_digit == 1 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == 2 :
            result_array = left_shift_binary_array(multiplicand_array,1)
        elif multiplier_binary_digit == -2 :
            two_s_complement = twos_complement(multiplicand_array)
            two_s_complement.append(0)
            result_array = two_s_complement
        return result_array


    def fill_start_with_zeros(array,array_length):
        while len(array) < array_length:
            array.insert(0,0)
        return array
    
    def convert_to_binary_array(number):
        binary_number = bin(number)[2:]
        array = []
        for each_digit in binary_number:
            array.append(int(each_digit))
        array = fill_start_with_zeros(array, 16)
        return array


    def calculate_length_of_product(multiplier_array, multiplicand_array, shift):
        for i in range(0, len(multiplier_array)):
            if i == 0:
                result = len(multiplicand_array)
            else:
                result = result + shift
        result = result + shift
        return result

    def generate_multiplier(multiplier_as_decimal):
        multiplier_binary_array = convert_to_binary_array(multiplier_as_decimal)
        multiplier_binary_array = fill_start_with_zeros(multiplier_binary_array,16)
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


    def get_mappings_for_multiplier_bits(bit_array):
        return mapping_dictionary[bit_array[0],bit_array[1],bit_array[2]]




    def add_zeros_to_start_of_array(products_array, length_of_product):
        for each_product in products_array:
            while len(each_product) < length_of_product:
                each_product.insert(0, 0)
        return products_array


    def add_none_to_end_of_array(products_array, shift):
        for i in range(0, len(products_array)):
            for _ in range(i * shift):
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


    def get_splitted_column_array(columns_array):
        result_columns = []
        for each_column in columns_array:
            columns = split_column_by_half(each_column)
            result_columns.append(columns)
        return result_columns


    def get_effective_length_of_column(each_half):
        length = 0
        for each_element in each_half:
            if each_element != None:
                length = length + 1
        return length


    def add_exact_compressor_columns(splitted_columns_array):
        for i in range(len(splitted_columns_array)):
            for j in range(len(splitted_columns_array[i])):
                length_of_column = get_effective_length_of_column(
                    splitted_columns_array[i][j]
                )

                if i == len(splitted_columns_array)-1:
                    
                    exact_compressor_columns.append([splitted_columns_array[i][j],
                    [None,None,None,None],
                    [i,j]])
                if length_of_column == 4 and i < len(splitted_columns_array)-1:
                    exact_compressor_columns.append(
                        [
                            splitted_columns_array[i][j],
                            splitted_columns_array[i + 1][j],
                            [i, j],
                        ]
                    )
        return exact_compressor_columns


    def add_half_adder_full_adder_pairs(splitted_columns_array):
        for i in range(0, len(splitted_columns_array)):
            for j in range(0, len(splitted_columns_array[i])):
                if is_half_adder_column(get_effective_length_of_column(splitted_columns_array[i][j])) and half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
                    half_adder_column = splitted_columns_array[i][j]
                    full_adder_column = find_full_adder_column(i, j, splitted_columns_array)
                    full_adder_carry_column = find_full_adder_carry_column(i, j, splitted_columns_array)
                    if full_adder_column is not None:
                        half_full_pair = [
                            half_adder_column,
                            full_adder_column,
                            full_adder_carry_column,
                            [i, j],]
                        half_adder_full_adder_pairs.append(half_full_pair)
        return half_adder_full_adder_pairs


    def is_half_adder_column(effective_length_of_column):
        if effective_length_of_column == 3:
            return True
        return False


    def half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return False
        return True


    def find_full_adder_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        if get_effective_length_of_column(columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]) == 3 and half_adder_full_adder_pair_array_not_contains(index_i_of_half_adder_pair, index_j_of_half_adder_pair, half_adder_full_adder_pairs):
            return columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]
        


    def find_full_adder_carry_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        return columns_array[index_i_of_half_adder_pair + 2][index_j_of_half_adder_pair]




    def get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return each_pair
        return None


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
        x1, x2, x3, x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
        sum = int(x1 or x2 or x3 or x4 or cin)
        k1 = int(x1 ^ x2)
        k2 = int(k1 and x3)
        k3 = int(k2 and x1)
        k4 = int(not k3)
        cout = int(k2 or k4)
        d1 = int(x1 ^ x2 ^ x3 ^ x4)
        d2 = int(d1 and cin)
        d3 = int(d1 and x4)
        d4 = int(not d3)
        carry = int(d2 or d4)
        return sum,cout,carry

    def approx_compressor(bytes_array):
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
        return sum_value, carry

    def get_cout_from_cout_array(i, j, cout_array):
        for each_cout in cout_array:
            if each_cout[0] == [i, j]:
                return each_cout[1]
        return None


    def result_already_present(key_tuple, result):
        if key_tuple in result:
            return True
        return False


    def get_exact_compressor_pairs(i_of_pair, j_of_pair,exact_compressor_columns):
        for i in range(len(exact_compressor_columns)):
            each_pair = exact_compressor_columns[i]
            if each_pair[2] == [i_of_pair, j_of_pair]:
                return each_pair


    result_array = multiply_multiplier_with_multiplicand(multiplier,multiplicand)

    columns_array = get_columns_from_product_array(result_array)

    splitted_columns_array = get_splitted_column_array(columns_array)

    half_adder_full_adder_pairs = add_half_adder_full_adder_pairs(splitted_columns_array)

    exact_compressor_columns = add_exact_compressor_columns(splitted_columns_array)



    result = {}
    cout_array = []



    for i in range(len(splitted_columns_array)):
        for j in range(len(splitted_columns_array[i])):
            byte_array = splitted_columns_array[i][j]
            if get_effective_length_of_column(byte_array) == 1:
                sum = byte_array[0]
                result[i, j] = [sum, None]
            elif get_effective_length_of_column(byte_array) == 2:
                sum = byte_array[0]
                carry = byte_array[1]
                result[i, j] = [sum, carry]
            elif (
                get_effective_length_of_column(byte_array) == 3
                and half_adder_full_adder_pair_array_not_contains(i, j,half_adder_full_adder_pairs) is not True
            ):
            
                half_full_adder_array = get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs)
                half_adder_pair, i_half_adder_pair, j_half_adder_pair = (
                    half_full_adder_array[0],
                    i,
                    j,
                )
                full_adder_pair, i_full_adder_pair, j_full_adder_pair = (
                    half_full_adder_array[1],
                    i + 1,
                    j,
                )
                full_adder_carry_pair, i_full_adder_carry_pair, j_full_adder_carry_pair = (
                    half_full_adder_array[2],
                    i + 2,
                    j,
                )
                half_adder_bit_1 = half_adder_pair[0]
                half_adder_bit_2 = half_adder_pair[1]
                half_adder_sum, half_adder_carry = half_adder(
                    half_adder_bit_1, half_adder_bit_2
                )
                result[i_half_adder_pair, j_half_adder_pair] = [
                    half_adder_sum,
                    half_adder_carry,
                ]
                full_adder_bit_1 = full_adder_pair[0]
                full_adder_bit_2 = full_adder_pair[1]
                full_adder_sum, full_adder_carry = full_adder(
                    full_adder_bit_1, full_adder_bit_2, half_adder_carry
                )
                result[i_full_adder_pair, j_full_adder_pair] = [
                    full_adder_sum,
                    full_adder_carry,
                ]
                sum_exact, carry_exact = approx_compressor(
                    full_adder_carry_pair
                )
                result[i_full_adder_carry_pair, j_full_adder_carry_pair] = [
                    sum_exact,
                    carry_exact,
                ]
            elif (
                get_effective_length_of_column(byte_array) == 4
                and result_already_present((i, j),result) is not True
                and (i and j) <= len(exact_compressor_columns)
            ):
                if i < len(splitted_columns_array)-1 :
                    exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                    if exact_compressor_pair_array is not None:
                        first_pair = exact_compressor_pair_array[0]
                        second_pair = exact_compressor_pair_array[1]
                        i_first_pair, j_first_pair = i, j
                        i_second_pair, j_second_pair = i + 1, j
                        (sum_exact_first,carry_exact_first) = approx_compressor(first_pair)
                        result[i_first_pair, j_first_pair] = [sum_exact_first,carry_exact_first]
                        (sum_exact_second,carry_exact_second) = approx_compressor(second_pair)
                        result[i_second_pair, j_second_pair] = [sum_exact_second,carry_exact_second]
                if i == len(splitted_columns_array)-1 :
                        first_pair = exact_compressor_pair_array[0]
                        i_first_pair, j_first_pair = i, j
                        (sum_exact_first,carry_exact_first) = approx_compressor(first_pair)
                        result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first
                            ]


    def generate_columns_before_cpa(result):
        columns = []
        for i in range(len(splitted_columns_array)):
            column_1 = result[i,0]
            column_2 = [None,None]
            if result_already_present((i,j),result):
                column_2 = result[i,1]
            column = [column_1[0],column_1[1],column_2[0],column_2[1]]
            columns.append(column)
        return columns
    

    splitted_columns_array_final = generate_columns_before_cpa(result)

    half_adder_full_adder_pairs_final = []
    exact_compressor_pairs_final = []

    def not_exists_in_half_adder_pairs_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            if index in each_pair[3]:
                return False
        return True

    def get_half_adder_full_adder_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if get_effective_length_of_column(each_column) == 3 and not_exists_in_half_adder_pairs_final(i):
                full_adder_pair = splitted_columns_array_final[i+1]
                full_adder_carry_pair = splitted_columns_array_final[i+2]
                half_adder_full_adder_pairs_final.append([each_column,full_adder_pair,full_adder_carry_pair,[i, i+1, i+2]])
        return half_adder_full_adder_pairs_final

    def get_exact_compressor_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if i == len(splitted_columns_array_final) - 1:
                exact_compressor_pairs_final.append([each_column,None,i])
            else:
                if get_effective_length_of_column(each_column) == 4:
                    next_column = splitted_columns_array_final[i+1]
                    exact_compressor_pairs_final.append([each_column,next_column,i])
        return exact_compressor_pairs_final

    half_adder_full_adder_pairs_final = get_half_adder_full_adder_pairs_final(splitted_columns_array_final)

    exact_compressor_pairs_final = get_exact_compressor_pairs_final(splitted_columns_array_final)


    def half_adder_full_adder_pair_final_not_contains(i):
        for each_array in half_adder_full_adder_pairs_final:
            if each_array[3] == i :
                return False
        return True


    cout_array_final = []


    def get_half_adder_full_adder_pair_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            i = each_pair[3][0]
            if i == index:
                return each_pair
        

    result_final = {}

    def get_cary_in_from_cout_final_array(index):
        for each_array in cout_array_final :
            if each_array[0] == index:
                return each_array[1]


    def get_exacy_compressor_pair_final(index):
        for each_pair in exact_compressor_pairs_final:
            if each_pair[2] == index:
                return each_pair


    for i in range(len(splitted_columns_array_final)):
        current_column = splitted_columns_array_final[i]
        i_of_next_column, j_of_next_column = i+1, j+1
        if get_effective_length_of_column(current_column) == 1:
            sum = current_column[0]
            result_final[i]=[sum,None]
        elif get_effective_length_of_column(current_column) == 2 :
            sum = current_column[0]
            carry = current_column[1]
            result_final[i]=[sum,carry]
        elif get_effective_length_of_column(current_column)== 3 and not result_already_present(i,result_final):
            result = get_half_adder_full_adder_pair_final(i)
            half_adder_pair = result[0]
            full_adder_pair = result[1]
            full_adder_carry_pair = result[2]
            i_half_adder_pair, i_full_adder_pair, i_full_adder_carry_pair = result[3][0],result[3][1],result[3][2]
            sum_half_adder, cout_half_adder = half_adder(half_adder_pair[0], half_adder_pair[1])
            carry_half_adder = half_adder_pair[2]
            sum_full_adder, cout_full_adder = full_adder(full_adder_pair[0],full_adder_pair[1],cout_half_adder)
            carry_full_adder = full_adder_pair[2]
            result_final[i_half_adder_pair] = [sum_half_adder,carry_half_adder]
            result_final[i_full_adder_pair] = [sum_full_adder,carry_full_adder]
            sum_final_carry,carry_final_carry = approx_compressor(full_adder_carry_pair)
            result_final[i_full_adder_carry_pair] = [sum_final_carry,carry_final_carry]
        elif get_effective_length_of_column(current_column) == 4 and not result_already_present(i, result_final):
            exact_compressor_pair = get_exacy_compressor_pair_final(i)
            next_column = exact_compressor_pair[1]
            c_in_first_column = get_cary_in_from_cout_final_array(i-1)
            sum_first_array, carry_first_array = approx_compressor(current_column)
            result_final[i] = [sum_first_array,carry_first_array]
            if i != len(splitted_columns_array_final) - 1:
                sum_second_array, carry_second_array = approx_compressor(next_column)
                result_final[i] = [sum_second_array,carry_second_array]


    final_bit_array = []

    for i in range(len(splitted_columns_array_final)):
        final_result_bits = result_final[i]
        if final_result_bits[1] is not None:
            final_sum = final_result_bits[0] or final_result_bits[1]
            final_bit_array.append(final_sum)
        else :
            final_bit_array.append(final_result_bits[0])



    def convert_bin_array_to_decimal(bin_array):
        value =0 
        for i in range(len(bin_array)):
            digit = bin_array.pop()
            if digit == 1:
                value = value + pow(2, i)
        return value
    
    return convert_bin_array_to_decimal(final_bit_array)




def approximate_in_seven_and_eight_final(multiplier,multiplicand):
    half_adder_full_adder_pairs = []
    exact_compressor_columns = []
    def twos_complement(binary_array):
        complement = [1 if bit == 0 else 0 for bit in binary_array]
        carry = 1
        for i in range(len(complement) - 1, -1, -1):
            if complement[i] == 0 and carry == 1:
                complement[i] = 1
                carry = 0
            elif complement[i] == 1 and carry == 1:
                complement[i] = 0
        return complement

    def left_shift_binary_array(binary_array, shift_amount):
        shifted_array = binary_array[shift_amount:] + [0] * shift_amount
        return shifted_array


    def multiply_multiplier_with_multiplicand(multiplier, multiplicand):
        multiplicand_array = convert_to_binary_array(multiplicand)
        multiplier_array = generate_multiplier(multiplier)
        shift = 2
        length_of_product = calculate_length_of_product(
            multiplier_array, multiplicand_array, shift
        )
        result_array = []
        for i in range(0, len(multiplier_array)):
            result = multiply_multiplier_digit_with_multiplicand(
                multiplier_array[i], multiplicand_array
            )
            result_array.append(result)
        add_none_to_end_of_array(result_array, shift)
        add_zeros_to_start_of_array(result_array, length_of_product)
        return result_array


    def multiply_multiplier_digit_with_multiplicand(
        multiplier_binary_digit, multiplicand_array
    ):
        result_array = []
        if multiplier_binary_digit == 0 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == -1 :
            result_array = twos_complement(multiplicand_array)
        elif multiplier_binary_digit == 1 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == 2 :
            result_array = left_shift_binary_array(multiplicand_array,1)
        elif multiplier_binary_digit == -2 :
            two_s_complement = twos_complement(multiplicand_array)
            two_s_complement.append(0)
            result_array = two_s_complement
        return result_array


    def fill_start_with_zeros(array,array_length):
        while len(array) < array_length:
            array.insert(0,0)
        return array
    
    def convert_to_binary_array(number):
        binary_number = bin(number)[2:]
        array = []
        for each_digit in binary_number:
            array.append(int(each_digit))
        array = fill_start_with_zeros(array, 16)
        return array
    
    def convert_to_binary_from_binary_array(binary_array):
        binary_string = "".join(str(bit) for bit in binary_array)
        binary_number = int(binary_string)
        return binary_number


    def calculate_length_of_product(multiplier_array, multiplicand_array, shift):
        for i in range(0, len(multiplier_array)):
            if i == 0:
                result = len(multiplicand_array)
            else:
                result = result + shift
        result = result + shift
        return result

    def generate_multiplier(multiplier_as_decimal):
        multiplier_binary_array = convert_to_binary_array(multiplier_as_decimal)
        multiplier_binary_array = fill_start_with_zeros(multiplier_binary_array,16)
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


    def get_mappings_for_multiplier_bits(bit_array):
        return mapping_dictionary[bit_array[0],bit_array[1],bit_array[2]]




    def add_zeros_to_start_of_array(products_array, length_of_product):
        for each_product in products_array:
            while len(each_product) < length_of_product:
                each_product.insert(0, 0)
        return products_array


    def add_none_to_end_of_array(products_array, shift):
        for i in range(0, len(products_array)):
            for _ in range(i * shift):
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


    def get_splitted_column_array(columns_array):
        result_columns = []
        for each_column in columns_array:
            columns = split_column_by_half(each_column)
            result_columns.append(columns)
        return result_columns


    def get_effective_length_of_column(each_half):
        length = 0
        for each_element in each_half:
            if each_element != None:
                length = length + 1
        return length


    def add_exact_compressor_columns(splitted_columns_array):
        for i in range(len(splitted_columns_array)):
            for j in range(len(splitted_columns_array[i])):
                length_of_column = get_effective_length_of_column(
                    splitted_columns_array[i][j]
                )

                if i == len(splitted_columns_array)-1:
                    
                    exact_compressor_columns.append([splitted_columns_array[i][j],
                    [None,None,None,None],
                    [i,j]])
                if length_of_column == 4 and i < len(splitted_columns_array)-1:
                    exact_compressor_columns.append(
                        [
                            splitted_columns_array[i][j],
                            splitted_columns_array[i + 1][j],
                            [i, j],
                        ]
                    )
        return exact_compressor_columns


    def add_half_adder_full_adder_pairs(splitted_columns_array):
        for i in range(0, len(splitted_columns_array)):
            for j in range(0, len(splitted_columns_array[i])):
                if is_half_adder_column(get_effective_length_of_column(splitted_columns_array[i][j])) and half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
                    half_adder_column = splitted_columns_array[i][j]
                    full_adder_column = find_full_adder_column(i, j, splitted_columns_array)
                    full_adder_carry_column = find_full_adder_carry_column(i, j, splitted_columns_array)
                    if full_adder_column is not None:
                        half_full_pair = [
                            half_adder_column,
                            full_adder_column,
                            full_adder_carry_column,
                            [i, j],]
                        half_adder_full_adder_pairs.append(half_full_pair)
        return half_adder_full_adder_pairs


    def is_half_adder_column(effective_length_of_column):
        if effective_length_of_column == 3:
            return True
        return False


    def half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return False
        return True


    def find_full_adder_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        if get_effective_length_of_column(columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]) == 3 and half_adder_full_adder_pair_array_not_contains(index_i_of_half_adder_pair, index_j_of_half_adder_pair, half_adder_full_adder_pairs):
            return columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]
        


    def find_full_adder_carry_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        return columns_array[index_i_of_half_adder_pair + 2][index_j_of_half_adder_pair]




    def get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return each_pair
        return None


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
        x1, x2, x3, x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
        sum = int(x1 or x2 or x3 or x4 or cin)
        k1 = int(x1 ^ x2)
        k2 = int(k1 and x3)
        k3 = int(k2 and x1)
        k4 = int(not k3)
        cout = int(k2 or k4)
        d1 = int(x1 ^ x2 ^ x3 ^ x4)
        d2 = int(d1 and cin)
        d3 = int(d1 and x4)
        d4 = int(not d3)
        carry = int(d2 or d4)
        return sum,cout,carry

    def approx_compressor(bytes_array):
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
        return sum_value, carry

    def get_cout_from_cout_array(i, j, cout_array):
        for each_cout in cout_array:
            if each_cout[0] == [i, j]:
                return each_cout[1]
        return 0


    def result_already_present(key_tuple, result):
        if key_tuple in result:
            return True
        return False


    def get_exact_compressor_pairs(i_of_pair, j_of_pair,exact_compressor_columns):
        for i in range(len(exact_compressor_columns)):
            each_pair = exact_compressor_columns[i]
            if each_pair[2] == [i_of_pair, j_of_pair]:
                return each_pair


    result_array = multiply_multiplier_with_multiplicand(multiplier,multiplicand)
    columns_array = get_columns_from_product_array(result_array)

    splitted_columns_array = get_splitted_column_array(columns_array)

    half_adder_full_adder_pairs = add_half_adder_full_adder_pairs(splitted_columns_array)

    exact_compressor_columns = add_exact_compressor_columns(splitted_columns_array)

    result = {}
    cout_array = []


    for i in range(len(splitted_columns_array)):
        for j in range(len(splitted_columns_array[i])):
            byte_array = splitted_columns_array[i][j]
            if (i == 6 or i==7) and result_already_present((i, j),result) is not True:
                exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                if exact_compressor_pair_array is not None:
                    first_pair = exact_compressor_pair_array[0]
                    second_pair = exact_compressor_pair_array[1]
                    i_first_pair, j_first_pair = i, j
                    (sum_exact_first,carry_exact_first) = approx_compressor(first_pair)
                    result[i_first_pair, j_first_pair] = [sum_exact_first,carry_exact_first]
            if get_effective_length_of_column(byte_array) == 1:
                sum = byte_array[0]
                result[i, j] = [sum, None]
            elif get_effective_length_of_column(byte_array) == 2:
                sum = byte_array[0]
                carry = byte_array[1]
                result[i, j] = [sum, carry]
            elif (
                get_effective_length_of_column(byte_array) == 3
                and half_adder_full_adder_pair_array_not_contains(i, j,half_adder_full_adder_pairs) is not True
            ):
            
                half_full_adder_array = get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs)
                half_adder_pair, i_half_adder_pair, j_half_adder_pair = (
                    half_full_adder_array[0],
                    i,
                    j,
                )
                full_adder_pair, i_full_adder_pair, j_full_adder_pair = (
                    half_full_adder_array[1],
                    i + 1,
                    j,
                )
                full_adder_carry_pair, i_full_adder_carry_pair, j_full_adder_carry_pair = (
                    half_full_adder_array[2],
                    i + 2,
                    j,
                )
                half_adder_bit_1 = half_adder_pair[0]
                half_adder_bit_2 = half_adder_pair[1]
                half_adder_sum, half_adder_carry = half_adder(
                    half_adder_bit_1, half_adder_bit_2
                )
                result[i_half_adder_pair, j_half_adder_pair] = [
                    half_adder_sum,
                    half_adder_carry,
                ]
                full_adder_bit_1 = full_adder_pair[0]
                full_adder_bit_2 = full_adder_pair[1]
                full_adder_sum, full_adder_carry = full_adder(
                    full_adder_bit_1, full_adder_bit_2, half_adder_carry
                )
                result[i_full_adder_pair, j_full_adder_pair] = [
                    full_adder_sum,
                    full_adder_carry,
                ]
                sum_exact, cout_exact, carry_exact = exact_compressor(
                    full_adder_carry_pair, full_adder_carry
                )
                result[i_full_adder_carry_pair, j_full_adder_carry_pair] = [
                    sum_exact,
                    carry_exact,
                ]
                cout_array.append(
                    [[i_full_adder_carry_pair, j_full_adder_carry_pair], cout_exact]
                )
            elif (
                get_effective_length_of_column(byte_array) == 4
                and result_already_present((i, j),result) is not True
                and (i and j) <= len(exact_compressor_columns)
                and (i != 6) and (i != 7) 
            ):
                if i < len(splitted_columns_array)-1 :
                    exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                    if exact_compressor_pair_array is not None:
                        first_pair = exact_compressor_pair_array[0]
                        second_pair = exact_compressor_pair_array[1]
                        i_first_pair, j_first_pair = i, j
                        i_second_pair, j_second_pair = i + 1, j
                        index_of_cout_array = 0
                        if i== 8 : 
                            index_of_cout_array = 6
                        else :
                            index_of_cout_array =i-1
                        c_in_of_first_pair = get_cout_from_cout_array(index_of_cout_array, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            cout_array.append(
                                [[i_second_pair, j_second_pair], cout_exact_second]
                            )
                if i == len(splitted_columns_array)-1 :
                        first_pair = exact_compressor_pair_array[0]
                        i_first_pair, j_first_pair = i, j
                        c_in_of_first_pair = get_cout_from_cout_array(i - 1, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]


    def generate_columns_before_cpa(result):
        columns = []
        for i in range(len(splitted_columns_array)):
            column_1 = result[i,0]
            column_2 = [None,None]
            if result_already_present((i,j),result):
                column_2 = result[i,1]
            column = [column_1[0],column_1[1],column_2[0],column_2[1]]
            columns.append(column)
        return columns


    splitted_columns_array_final = generate_columns_before_cpa(result)


    half_adder_full_adder_pairs_final = []
    exact_compressor_pairs_final = []

    def not_exists_in_half_adder_pairs_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            if index in each_pair[3]:
                return False
        return True

    def get_half_adder_full_adder_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if get_effective_length_of_column(each_column) == 3 and not_exists_in_half_adder_pairs_final(i):
                full_adder_pair = splitted_columns_array_final[i+1]
                full_adder_carry_pair = splitted_columns_array_final[i+2]
                half_adder_full_adder_pairs_final.append([each_column,full_adder_pair,full_adder_carry_pair,[i, i+1, i+2]])
        return half_adder_full_adder_pairs_final

    def get_exact_compressor_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if i == len(splitted_columns_array_final) - 1:
                exact_compressor_pairs_final.append([each_column,None,i])
            else:
                if get_effective_length_of_column(each_column) == 4:
                    next_column = splitted_columns_array_final[i+1]
                    exact_compressor_pairs_final.append([each_column,next_column,i])
        return exact_compressor_pairs_final

    half_adder_full_adder_pairs_final = get_half_adder_full_adder_pairs_final(splitted_columns_array_final)

    exact_compressor_pairs_final = get_exact_compressor_pairs_final(splitted_columns_array_final)



    def half_adder_full_adder_pair_final_not_contains(i):
        for each_array in half_adder_full_adder_pairs_final:
            if each_array[3] == i :
                return False
        return True


    cout_array_final = []


    def get_half_adder_full_adder_pair_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            i = each_pair[3][0]
            if i == index:
                return each_pair
        

    result_final = {}

    def get_cary_in_from_cout_final_array(index):
        for each_array in cout_array_final :
            if each_array[0] == index:
                return each_array[1]


    def get_exacy_compressor_pair_final(index):
        for each_pair in exact_compressor_pairs_final:
            if each_pair[2] == index:
                return each_pair


    for i in range(len(splitted_columns_array_final)):
        current_column = splitted_columns_array_final[i]
        i_of_next_column, j_of_next_column = i+1, j+1
        if get_effective_length_of_column(current_column) == 1:
            sum = current_column[0]
            result_final[i]=[sum,None]
        elif get_effective_length_of_column(current_column) == 2 :
            sum = current_column[0]
            carry = current_column[1]
            result_final[i]=[sum,carry]
        elif get_effective_length_of_column(current_column)== 3 and not result_already_present(i,result_final):
            result = get_half_adder_full_adder_pair_final(i)
            half_adder_pair = result[0]
            full_adder_pair = result[1]
            full_adder_carry_pair = result[2]
            i_half_adder_pair, i_full_adder_pair, i_full_adder_carry_pair = result[3][0],result[3][1],result[3][2]
            sum_half_adder, cout_half_adder = half_adder(half_adder_pair[0], half_adder_pair[1])
            carry_half_adder = half_adder_pair[2]
            sum_full_adder, cout_full_adder = full_adder(full_adder_pair[0],full_adder_pair[1],cout_half_adder)
            carry_full_adder = full_adder_pair[2]
            result_final[i_half_adder_pair] = [sum_half_adder,carry_half_adder]
            result_final[i_full_adder_pair] = [sum_full_adder,carry_full_adder]
            sum_final_carry,cout_final_carry,carry_final_carry = exact_compressor(full_adder_carry_pair,cout_full_adder)
            result_final[i_full_adder_carry_pair] = [sum_final_carry,carry_final_carry]
            cout_array_final.append([i_full_adder_carry_pair, cout_final_carry])
        elif get_effective_length_of_column(current_column) == 4 and not result_already_present(i, result_final):
            exact_compressor_pair = get_exacy_compressor_pair_final(i)
            next_column = exact_compressor_pair[1]
            c_in_first_column = get_cary_in_from_cout_final_array(i-1)
            sum_first_array, cout_first_array, carry_first_array = exact_compressor(current_column,c_in_first_column)
            result_final[i] = [sum_first_array,carry_first_array]
            if i != len(splitted_columns_array_final) - 1:
                sum_second_array, cout_second_array, carry_second_array = exact_compressor(next_column,cout_first_array)
                cout_array_final.append([i,cout_second_array])
                result_final[i] = [sum_second_array,carry_second_array]


    final_bit_array = []

    for i in range(len(splitted_columns_array_final)):
        final_result_bits = result_final[i]
        if final_result_bits[1] is not None:
            final_sum = final_result_bits[0] or final_result_bits[1]
            final_bit_array.append(final_sum)
        else :
            final_bit_array.append(final_result_bits[0])


    def convert_bin_array_to_decimal(bin_array):
        value =0 
        for i in range(len(bin_array)):
            digit = bin_array.pop()
            if digit == 1:
                value = value + pow(2, i)
        return value

    return convert_bin_array_to_decimal(final_bit_array)

def approximate_in_seven_eight_nine_final(multiplier, multiplicand):
    half_adder_full_adder_pairs = []
    exact_compressor_columns = []
    def twos_complement(binary_array):
        complement = [1 if bit == 0 else 0 for bit in binary_array]
        carry = 1
        for i in range(len(complement) - 1, -1, -1):
            if complement[i] == 0 and carry == 1:
                complement[i] = 1
                carry = 0
            elif complement[i] == 1 and carry == 1:
                complement[i] = 0
        return complement

    def left_shift_binary_array(binary_array, shift_amount):
        shifted_array = binary_array[shift_amount:] + [0] * shift_amount
        return shifted_array


    def multiply_multiplier_with_multiplicand(multiplier, multiplicand):
        multiplicand_array = convert_to_binary_array(multiplicand)
        multiplier_array = generate_multiplier(multiplier)
        shift = 2
        length_of_product = calculate_length_of_product(
            multiplier_array, multiplicand_array, shift
        )
        result_array = []
        for i in range(0, len(multiplier_array)):
            result = multiply_multiplier_digit_with_multiplicand(
                multiplier_array[i], multiplicand_array
            )
            result_array.append(result)
        add_none_to_end_of_array(result_array, shift)
        add_zeros_to_start_of_array(result_array, length_of_product)
        return result_array


    def multiply_multiplier_digit_with_multiplicand(
        multiplier_binary_digit, multiplicand_array
    ):
        result_array = []
        if multiplier_binary_digit == 0 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == -1 :
            result_array = twos_complement(multiplicand_array)
        elif multiplier_binary_digit == 1 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == 2 :
            result_array = left_shift_binary_array(multiplicand_array,1)
        elif multiplier_binary_digit == -2 :
            two_s_complement = twos_complement(multiplicand_array)
            two_s_complement.append(0)
            result_array = two_s_complement
        return result_array

    def fill_start_with_zeros(array,array_length):
        while len(array) < array_length:
            array.insert(0,0)
        return array
    
    def convert_to_binary_array(number):
        binary_number = bin(number)[2:]
        array = []
        for each_digit in binary_number:
            array.append(int(each_digit))
        array = fill_start_with_zeros(array, 16)
        return array
    
    def convert_to_binary_from_binary_array(binary_array):
        binary_string = "".join(str(bit) for bit in binary_array)
        binary_number = int(binary_string)
        return binary_number


    def calculate_length_of_product(multiplier_array, multiplicand_array, shift):
        for i in range(0, len(multiplier_array)):
            if i == 0:
                result = len(multiplicand_array)
            else:
                result = result + shift
        result = result + shift
        return result


    def generate_multiplier(multiplier_as_decimal):
        multiplier_binary_array = convert_to_binary_array(multiplier_as_decimal)
        multiplier_binary_array = fill_start_with_zeros(multiplier_binary_array,16)
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


    def get_mappings_for_multiplier_bits(bit_array):
        return mapping_dictionary[bit_array[0],bit_array[1],bit_array[2]]




    def add_zeros_to_start_of_array(products_array, length_of_product):
        for each_product in products_array:
            while len(each_product) < length_of_product:
                each_product.insert(0, 0)
        return products_array


    def add_none_to_end_of_array(products_array, shift):
        for i in range(0, len(products_array)):
            for _ in range(i * shift):
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


    def get_splitted_column_array(columns_array):
        result_columns = []
        for each_column in columns_array:
            columns = split_column_by_half(each_column)
            result_columns.append(columns)
        return result_columns


    def get_effective_length_of_column(each_half):
        length = 0
        for each_element in each_half:
            if each_element != None:
                length = length + 1
        return length


    def add_exact_compressor_columns(splitted_columns_array):
        for i in range(len(splitted_columns_array)):
            for j in range(len(splitted_columns_array[i])):
                length_of_column = get_effective_length_of_column(
                    splitted_columns_array[i][j]
                )

                if i == len(splitted_columns_array)-1:
                    
                    exact_compressor_columns.append([splitted_columns_array[i][j],
                    [None,None,None,None],
                    [i,j]])
                if length_of_column == 4 and i < len(splitted_columns_array)-1:
                    exact_compressor_columns.append(
                        [
                            splitted_columns_array[i][j],
                            splitted_columns_array[i + 1][j],
                            [i, j],
                        ]
                    )
        return exact_compressor_columns


    def add_half_adder_full_adder_pairs(splitted_columns_array):
        for i in range(0, len(splitted_columns_array)):
            for j in range(0, len(splitted_columns_array[i])):
                if is_half_adder_column(get_effective_length_of_column(splitted_columns_array[i][j])) and half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
                    half_adder_column = splitted_columns_array[i][j]
                    full_adder_column = find_full_adder_column(i, j, splitted_columns_array)
                    full_adder_carry_column = find_full_adder_carry_column(i, j, splitted_columns_array)
                    if full_adder_column is not None:
                        half_full_pair = [
                            half_adder_column,
                            full_adder_column,
                            full_adder_carry_column,
                            [i, j],]
                        half_adder_full_adder_pairs.append(half_full_pair)
        return half_adder_full_adder_pairs


    def is_half_adder_column(effective_length_of_column):
        if effective_length_of_column == 3:
            return True
        return False


    def half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return False
        return True


    def find_full_adder_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        if get_effective_length_of_column(columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]) == 3 and half_adder_full_adder_pair_array_not_contains(index_i_of_half_adder_pair, index_j_of_half_adder_pair, half_adder_full_adder_pairs):
            return columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]
        


    def find_full_adder_carry_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        return columns_array[index_i_of_half_adder_pair + 2][index_j_of_half_adder_pair]




    def get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return each_pair
        return None


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
        x1, x2, x3, x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
        sum = int(x1 or x2 or x3 or x4 or cin)
        k1 = int(x1 ^ x2)
        k2 = int(k1 and x3)
        k3 = int(k2 and x1)
        k4 = int(not k3)
        cout = int(k2 or k4)
        d1 = int(x1 ^ x2 ^ x3 ^ x4)
        d2 = int(d1 and cin)
        d3 = int(d1 and x4)
        d4 = int(not d3)
        carry = int(d2 or d4)
        return sum,cout,carry

    def approx_compressor(bytes_array):
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
        return sum_value, carry

    def get_cout_from_cout_array(i, j, cout_array):
        for each_cout in cout_array:
            if each_cout[0] == [i, j]:
                return each_cout[1]
        return 0


    def result_already_present(key_tuple, result):
        if key_tuple in result:
            return True
        return False


    def get_exact_compressor_pairs(i_of_pair, j_of_pair,exact_compressor_columns):
        for i in range(len(exact_compressor_columns)):
            each_pair = exact_compressor_columns[i]
            if each_pair[2] == [i_of_pair, j_of_pair]:
                return each_pair


    result_array = multiply_multiplier_with_multiplicand(multiplier,multiplicand)


    columns_array = get_columns_from_product_array(result_array)



    splitted_columns_array = get_splitted_column_array(columns_array)


    half_adder_full_adder_pairs = add_half_adder_full_adder_pairs(splitted_columns_array)



    exact_compressor_columns = add_exact_compressor_columns(splitted_columns_array)



    result = {}
    cout_array = []


    for i in range(len(splitted_columns_array)):
        for j in range(len(splitted_columns_array[i])):
            byte_array = splitted_columns_array[i][j]
            if i == 6 or i==7 or i == 8 and result_already_present((i, j),result) is not True:
                exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                if exact_compressor_pair_array is not None:
                    first_pair = exact_compressor_pair_array[0]
                    second_pair = exact_compressor_pair_array[1]
                    i_first_pair, j_first_pair = i, j
                    (sum_exact_first,carry_exact_first) = approx_compressor(first_pair)
                    result[i_first_pair, j_first_pair] = [sum_exact_first,carry_exact_first]
            if get_effective_length_of_column(byte_array) == 1:
                sum = byte_array[0]
                result[i, j] = [sum, None]
            elif get_effective_length_of_column(byte_array) == 2:
                sum = byte_array[0]
                carry = byte_array[1]
                result[i, j] = [sum, carry]
            elif (
                get_effective_length_of_column(byte_array) == 3
                and half_adder_full_adder_pair_array_not_contains(i, j,half_adder_full_adder_pairs) is not True
            ):
            
                half_full_adder_array = get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs)
                half_adder_pair, i_half_adder_pair, j_half_adder_pair = (
                    half_full_adder_array[0],
                    i,
                    j,
                )
                full_adder_pair, i_full_adder_pair, j_full_adder_pair = (
                    half_full_adder_array[1],
                    i + 1,
                    j,
                )
                full_adder_carry_pair, i_full_adder_carry_pair, j_full_adder_carry_pair = (
                    half_full_adder_array[2],
                    i + 2,
                    j,
                )
                half_adder_bit_1 = half_adder_pair[0]
                half_adder_bit_2 = half_adder_pair[1]
                half_adder_sum, half_adder_carry = half_adder(
                    half_adder_bit_1, half_adder_bit_2
                )
                result[i_half_adder_pair, j_half_adder_pair] = [
                    half_adder_sum,
                    half_adder_carry,
                ]
                full_adder_bit_1 = full_adder_pair[0]
                full_adder_bit_2 = full_adder_pair[1]
                full_adder_sum, full_adder_carry = full_adder(
                    full_adder_bit_1, full_adder_bit_2, half_adder_carry
                )
                result[i_full_adder_pair, j_full_adder_pair] = [
                    full_adder_sum,
                    full_adder_carry,
                ]
                sum_exact, cout_exact, carry_exact = exact_compressor(
                    full_adder_carry_pair, full_adder_carry
                )
                result[i_full_adder_carry_pair, j_full_adder_carry_pair] = [
                    sum_exact,
                    carry_exact,
                ]
                cout_array.append(
                    [[i_full_adder_carry_pair, j_full_adder_carry_pair], cout_exact]
                )
            elif (
                get_effective_length_of_column(byte_array) == 4
                and result_already_present((i, j),result) is not True
                and (i and j) <= len(exact_compressor_columns)
                and (i != 6) and (i != 7) and (i != 8)
            ):
                if i < len(splitted_columns_array)-1 :
                    exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                    if exact_compressor_pair_array is not None:
                        first_pair = exact_compressor_pair_array[0]
                        second_pair = exact_compressor_pair_array[1]
                        i_first_pair, j_first_pair = i, j
                        i_second_pair, j_second_pair = i + 1, j
                        index_of_cout_array = 0
                        if i== 9 : 
                            index_of_cout_array = 6
                        else :
                            index_of_cout_array =i-1
                        c_in_of_first_pair = get_cout_from_cout_array(index_of_cout_array, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            cout_array.append(
                                [[i_second_pair, j_second_pair], cout_exact_second]
                            )
                if i == len(splitted_columns_array)-1 :
                        first_pair = exact_compressor_pair_array[0]
                        i_first_pair, j_first_pair = i, j
                        c_in_of_first_pair = get_cout_from_cout_array(i - 1, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]

    def generate_columns_before_cpa(result):
        columns = []
        for i in range(len(splitted_columns_array)):
            column_1 = result[i,0]
            column_2 = [None,None]
            if result_already_present((i,j),result):
                column_2 = result[i,1]
            column = [column_1[0],column_1[1],column_2[0],column_2[1]]
            columns.append(column)
        return columns


    splitted_columns_array_final = generate_columns_before_cpa(result)


    half_adder_full_adder_pairs_final = []
    exact_compressor_pairs_final = []

    def not_exists_in_half_adder_pairs_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            if index in each_pair[3]:
                return False
        return True

    def get_half_adder_full_adder_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if get_effective_length_of_column(each_column) == 3 and not_exists_in_half_adder_pairs_final(i):
                full_adder_pair = splitted_columns_array_final[i+1]
                full_adder_carry_pair = splitted_columns_array_final[i+2]
                half_adder_full_adder_pairs_final.append([each_column,full_adder_pair,full_adder_carry_pair,[i, i+1, i+2]])
        return half_adder_full_adder_pairs_final

    def get_exact_compressor_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if i == len(splitted_columns_array_final) - 1:
                exact_compressor_pairs_final.append([each_column,None,i])
            else:
                if get_effective_length_of_column(each_column) == 4:
                    next_column = splitted_columns_array_final[i+1]
                    exact_compressor_pairs_final.append([each_column,next_column,i])
        return exact_compressor_pairs_final

    half_adder_full_adder_pairs_final = get_half_adder_full_adder_pairs_final(splitted_columns_array_final)
    exact_compressor_pairs_final = get_exact_compressor_pairs_final(splitted_columns_array_final)


    def half_adder_full_adder_pair_final_not_contains(i):
        for each_array in half_adder_full_adder_pairs_final:
            if each_array[3] == i :
                return False
        return True


    cout_array_final = []


    def get_half_adder_full_adder_pair_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            i = each_pair[3][0]
            if i == index:
                return each_pair
        

    result_final = {}

    def get_cary_in_from_cout_final_array(index):
        for each_array in cout_array_final :
            if each_array[0] == index:
                return each_array[1]


    def get_exacy_compressor_pair_final(index):
        for each_pair in exact_compressor_pairs_final:
            if each_pair[2] == index:
                return each_pair


    for i in range(len(splitted_columns_array_final)):
        current_column = splitted_columns_array_final[i]
        i_of_next_column, j_of_next_column = i+1, j+1
        if get_effective_length_of_column(current_column) == 1:
            sum = current_column[0]
            result_final[i]=[sum,None]
        elif get_effective_length_of_column(current_column) == 2 :
            sum = current_column[0]
            carry = current_column[1]
            result_final[i]=[sum,carry]
        elif get_effective_length_of_column(current_column)== 3 and not result_already_present(i,result_final):
            result = get_half_adder_full_adder_pair_final(i)
            half_adder_pair = result[0]
            full_adder_pair = result[1]
            full_adder_carry_pair = result[2]
            i_half_adder_pair, i_full_adder_pair, i_full_adder_carry_pair = result[3][0],result[3][1],result[3][2]
            sum_half_adder, cout_half_adder = half_adder(half_adder_pair[0], half_adder_pair[1])
            carry_half_adder = half_adder_pair[2]
            sum_full_adder, cout_full_adder = full_adder(full_adder_pair[0],full_adder_pair[1],cout_half_adder)
            carry_full_adder = full_adder_pair[2]
            result_final[i_half_adder_pair] = [sum_half_adder,carry_half_adder]
            result_final[i_full_adder_pair] = [sum_full_adder,carry_full_adder]
            sum_final_carry,cout_final_carry,carry_final_carry = exact_compressor(full_adder_carry_pair,cout_full_adder)
            result_final[i_full_adder_carry_pair] = [sum_final_carry,carry_final_carry]
            cout_array_final.append([i_full_adder_carry_pair, cout_final_carry])
        elif get_effective_length_of_column(current_column) == 4 and not result_already_present(i, result_final):
            exact_compressor_pair = get_exacy_compressor_pair_final(i)
            next_column = exact_compressor_pair[1]
            c_in_first_column = get_cary_in_from_cout_final_array(i-1)
            sum_first_array, cout_first_array, carry_first_array = exact_compressor(current_column,c_in_first_column)
            result_final[i] = [sum_first_array,carry_first_array]
            if i != len(splitted_columns_array_final) - 1:
                sum_second_array, cout_second_array, carry_second_array = exact_compressor(next_column,cout_first_array)
                cout_array_final.append([i,cout_second_array])
                result_final[i] = [sum_second_array,carry_second_array]


    final_bit_array = []

    for i in range(len(splitted_columns_array_final)):
        final_result_bits = result_final[i]
        if final_result_bits[1] is not None:
            final_sum = final_result_bits[0] or final_result_bits[1]
            final_bit_array.append(final_sum)
        else :
            final_bit_array.append(final_result_bits[0])



    def convert_bin_array_to_decimal(bin_array):
        value =0 
        for i in range(len(bin_array)):
            digit = bin_array.pop()
            if digit == 1:
                value = value + pow(2, i)
        return value


    return convert_bin_array_to_decimal(final_bit_array)



def approximate_in_seven_to_twelve_final(multiplier,multiplicand):
    half_adder_full_adder_pairs = []
    exact_compressor_columns = []
    def twos_complement(binary_array):
        complement = [1 if bit == 0 else 0 for bit in binary_array]
        carry = 1
        for i in range(len(complement) - 1, -1, -1):
            if complement[i] == 0 and carry == 1:
                complement[i] = 1
                carry = 0
            elif complement[i] == 1 and carry == 1:
                complement[i] = 0
        return complement

    def left_shift_binary_array(binary_array, shift_amount):
        shifted_array = binary_array[shift_amount:] + [0] * shift_amount
        return shifted_array


    def multiply_multiplier_with_multiplicand(multiplier, multiplicand):
        multiplicand_array = convert_to_binary_array(multiplicand)
        multiplier_array = generate_multiplier(multiplier)
        shift = 2
        length_of_product = calculate_length_of_product(
            multiplier_array, multiplicand_array, shift
        )
        result_array = []
        for i in range(0, len(multiplier_array)):
            result = multiply_multiplier_digit_with_multiplicand(
                multiplier_array[i], multiplicand_array
            )
            result_array.append(result)
        add_none_to_end_of_array(result_array, shift)
        add_zeros_to_start_of_array(result_array, length_of_product)
        return result_array


    def multiply_multiplier_digit_with_multiplicand(
        multiplier_binary_digit, multiplicand_array
    ):
        result_array = []
        if multiplier_binary_digit == 0 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == -1 :
            result_array = twos_complement(multiplicand_array)
        elif multiplier_binary_digit == 1 :
            for each_digit in multiplicand_array:
                result_array.append(each_digit&multiplier_binary_digit)
        elif multiplier_binary_digit == 2 :
            result_array = left_shift_binary_array(multiplicand_array,1)
        elif multiplier_binary_digit == -2 :
            two_s_complement = twos_complement(multiplicand_array)
            two_s_complement.append(0)
            result_array = two_s_complement
        return result_array


    def fill_start_with_zeros(array,array_length):
        while len(array) < array_length:
            array.insert(0,0)
        return array
    
    def convert_to_binary_array(number):
        binary_number = bin(number)[2:]
        array = []
        for each_digit in binary_number:
            array.append(int(each_digit))
        array = fill_start_with_zeros(array, 16)
        return array
    
    def convert_to_binary_from_binary_array(binary_array):
        binary_string = "".join(str(bit) for bit in binary_array)
        binary_number = int(binary_string)
        return binary_number


    def calculate_length_of_product(multiplier_array, multiplicand_array, shift):
        for i in range(0, len(multiplier_array)):
            if i == 0:
                result = len(multiplicand_array)
            else:
                result = result + shift
        result = result + shift
        return result

    def generate_multiplier(multiplier_as_decimal):
        multiplier_binary_array = convert_to_binary_array(multiplier_as_decimal)
        multiplier_binary_array = fill_start_with_zeros(multiplier_binary_array,16)
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


    def get_mappings_for_multiplier_bits(bit_array):
        return mapping_dictionary[bit_array[0],bit_array[1],bit_array[2]]




    def add_zeros_to_start_of_array(products_array, length_of_product):
        for each_product in products_array:
            while len(each_product) < length_of_product:
                each_product.insert(0, 0)
        return products_array


    def add_none_to_end_of_array(products_array, shift):
        for i in range(0, len(products_array)):
            for _ in range(i * shift):
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


    def get_splitted_column_array(columns_array):
        result_columns = []
        for each_column in columns_array:
            columns = split_column_by_half(each_column)
            result_columns.append(columns)
        return result_columns


    def get_effective_length_of_column(each_half):
        length = 0
        for each_element in each_half:
            if each_element != None:
                length = length + 1
        return length


    def add_exact_compressor_columns(splitted_columns_array):
        for i in range(len(splitted_columns_array)):
            for j in range(len(splitted_columns_array[i])):
                length_of_column = get_effective_length_of_column(
                    splitted_columns_array[i][j]
                )

                if i == len(splitted_columns_array)-1:
                    
                    exact_compressor_columns.append([splitted_columns_array[i][j],
                    [None,None,None,None],
                    [i,j]])
                if length_of_column == 4 and i < len(splitted_columns_array)-1:
                    exact_compressor_columns.append(
                        [
                            splitted_columns_array[i][j],
                            splitted_columns_array[i + 1][j],
                            [i, j],
                        ]
                    )
        return exact_compressor_columns


    def add_half_adder_full_adder_pairs(splitted_columns_array):
        for i in range(0, len(splitted_columns_array)):
            for j in range(0, len(splitted_columns_array[i])):
                if is_half_adder_column(get_effective_length_of_column(splitted_columns_array[i][j])) and half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
                    half_adder_column = splitted_columns_array[i][j]
                    full_adder_column = find_full_adder_column(i, j, splitted_columns_array)
                    full_adder_carry_column = find_full_adder_carry_column(i, j, splitted_columns_array)
                    if full_adder_column is not None:
                        half_full_pair = [
                            half_adder_column,
                            full_adder_column,
                            full_adder_carry_column,
                            [i, j],]
                        half_adder_full_adder_pairs.append(half_full_pair)
        return half_adder_full_adder_pairs


    def is_half_adder_column(effective_length_of_column):
        if effective_length_of_column == 3:
            return True
        return False


    def half_adder_full_adder_pair_array_not_contains(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return False
        return True


    def find_full_adder_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        if get_effective_length_of_column(columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]) == 3 and half_adder_full_adder_pair_array_not_contains(index_i_of_half_adder_pair, index_j_of_half_adder_pair, half_adder_full_adder_pairs):
            return columns_array[index_i_of_half_adder_pair + 1][index_j_of_half_adder_pair]
        


    def find_full_adder_carry_column(index_i_of_half_adder_pair, index_j_of_half_adder_pair, columns_array):
        return columns_array[index_i_of_half_adder_pair + 2][index_j_of_half_adder_pair]




    def get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs):
        for each_pair in half_adder_full_adder_pairs:
            if each_pair[3] == [i, j]:
                return each_pair
        return None


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
        x1, x2, x3, x4 = bytes_array[0], bytes_array[1], bytes_array[2], bytes_array[3]
        sum = int(x1 or x2 or x3 or x4 or cin)
        k1 = int(x1 ^ x2)
        k2 = int(k1 and x3)
        k3 = int(k2 and x1)
        k4 = int(not k3)
        cout = int(k2 or k4)
        d1 = int(x1 ^ x2 ^ x3 ^ x4)
        d2 = int(d1 and cin)
        d3 = int(d1 and x4)
        d4 = int(not d3)
        carry = int(d2 or d4)
        return sum,cout,carry

    def approx_compressor(bytes_array):
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
        return sum_value, carry

    def get_cout_from_cout_array(i, j, cout_array):
        for each_cout in cout_array:
            if each_cout[0] == [i, j]:
                return each_cout[1]
        return 0


    def result_already_present(key_tuple, result):
        if key_tuple in result:
            return True
        return False


    def get_exact_compressor_pairs(i_of_pair, j_of_pair,exact_compressor_columns):
        for i in range(len(exact_compressor_columns)):
            each_pair = exact_compressor_columns[i]
            if each_pair[2] == [i_of_pair, j_of_pair]:
                return each_pair






    result_array = multiply_multiplier_with_multiplicand(multiplier,multiplicand)


    columns_array = get_columns_from_product_array(result_array)


    splitted_columns_array = get_splitted_column_array(columns_array)


    half_adder_full_adder_pairs = add_half_adder_full_adder_pairs(splitted_columns_array)

    exact_compressor_columns = add_exact_compressor_columns(splitted_columns_array)



    result = {}
    cout_array = []


    for i in range(len(splitted_columns_array)):
        for j in range(len(splitted_columns_array[i])):
            byte_array = splitted_columns_array[i][j]
            if (i == 6 or i==7 or i == 8 or i==9 or i==10 or i==11) and result_already_present((i, j),result) is not True:
                exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                if exact_compressor_pair_array is not None:
                    first_pair = exact_compressor_pair_array[0]
                    second_pair = exact_compressor_pair_array[1]
                    i_first_pair, j_first_pair = i, j
                    (sum_exact_first,carry_exact_first) = approx_compressor(first_pair)
                    result[i_first_pair, j_first_pair] = [sum_exact_first,carry_exact_first]
            if get_effective_length_of_column(byte_array) == 1:
                sum = byte_array[0]
                result[i, j] = [sum, None]
            elif get_effective_length_of_column(byte_array) == 2:
                sum = byte_array[0]
                carry = byte_array[1]
                result[i, j] = [sum, carry]
            elif (
                get_effective_length_of_column(byte_array) == 3
                and half_adder_full_adder_pair_array_not_contains(i, j,half_adder_full_adder_pairs) is not True
            ):
            
                half_full_adder_array = get_half_adder_full_adder_pairs(i, j, half_adder_full_adder_pairs)
                half_adder_pair, i_half_adder_pair, j_half_adder_pair = (
                    half_full_adder_array[0],
                    i,
                    j,
                )
                full_adder_pair, i_full_adder_pair, j_full_adder_pair = (
                    half_full_adder_array[1],
                    i + 1,
                    j,
                )
                full_adder_carry_pair, i_full_adder_carry_pair, j_full_adder_carry_pair = (
                    half_full_adder_array[2],
                    i + 2,
                    j,
                )
                half_adder_bit_1 = half_adder_pair[0]
                half_adder_bit_2 = half_adder_pair[1]
                half_adder_sum, half_adder_carry = half_adder(
                    half_adder_bit_1, half_adder_bit_2
                )
                result[i_half_adder_pair, j_half_adder_pair] = [
                    half_adder_sum,
                    half_adder_carry,
                ]
                full_adder_bit_1 = full_adder_pair[0]
                full_adder_bit_2 = full_adder_pair[1]
                full_adder_sum, full_adder_carry = full_adder(
                    full_adder_bit_1, full_adder_bit_2, half_adder_carry
                )
                result[i_full_adder_pair, j_full_adder_pair] = [
                    full_adder_sum,
                    full_adder_carry,
                ]
                sum_exact, cout_exact, carry_exact = exact_compressor(
                    full_adder_carry_pair, full_adder_carry
                )
                result[i_full_adder_carry_pair, j_full_adder_carry_pair] = [
                    sum_exact,
                    carry_exact,
                ]
                cout_array.append(
                    [[i_full_adder_carry_pair, j_full_adder_carry_pair], cout_exact]
                )
            elif (
                get_effective_length_of_column(byte_array) == 4
                and result_already_present((i, j),result) is not True
                and (i and j) <= len(exact_compressor_columns)
                and (i != 6) and (i != 7) and (i != 8) and i != 9 and (i != 10) and (i != 11)
            ):
                if i < len(splitted_columns_array)-1 :
                    exact_compressor_pair_array = get_exact_compressor_pairs(i, j, exact_compressor_columns)
                    if exact_compressor_pair_array is not None:
                        first_pair = exact_compressor_pair_array[0]
                        second_pair = exact_compressor_pair_array[1]
                        i_first_pair, j_first_pair = i, j
                        i_second_pair, j_second_pair = i + 1, j
                        index_of_cout_array = 0
                        if i== 12 : 
                            index_of_cout_array = 6
                        else :
                            index_of_cout_array =i-1
                        c_in_of_first_pair = get_cout_from_cout_array(index_of_cout_array, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            (
                                sum_exact_second,
                                cout_exact_second,
                                carry_exact_second,
                            ) = exact_compressor(second_pair, cout_exact_first)
                            result[i_second_pair, j_second_pair] = [
                                sum_exact_second,
                                carry_exact_second,
                            ]
                            cout_array.append(
                                [[i_second_pair, j_second_pair], cout_exact_second]
                            )
                if i == len(splitted_columns_array)-1 :
                        first_pair = exact_compressor_pair_array[0]
                        i_first_pair, j_first_pair = i, j
                        c_in_of_first_pair = get_cout_from_cout_array(i - 1, j, cout_array)
                        if c_in_of_first_pair is not None:
                            (
                                sum_exact_first,
                                cout_exact_first,
                                carry_exact_first,
                            ) = exact_compressor(first_pair, c_in_of_first_pair)
                            result[i_first_pair, j_first_pair] = [
                                sum_exact_first,
                                carry_exact_first,
                            ]


    def generate_columns_before_cpa(result):
        columns = []
        for i in range(len(splitted_columns_array)):
            column_1 = result[i,0]
            column_2 = [None,None]
            if result_already_present((i,j),result):
                column_2 = result[i,1]
            column = [column_1[0],column_1[1],column_2[0],column_2[1]]
            columns.append(column)
        return columns


    splitted_columns_array_final = generate_columns_before_cpa(result)


    half_adder_full_adder_pairs_final = []
    exact_compressor_pairs_final = []

    def not_exists_in_half_adder_pairs_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            if index in each_pair[3]:
                return False
        return True

    def get_half_adder_full_adder_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if get_effective_length_of_column(each_column) == 3 and not_exists_in_half_adder_pairs_final(i):
                full_adder_pair = splitted_columns_array_final[i+1]
                full_adder_carry_pair = splitted_columns_array_final[i+2]
                half_adder_full_adder_pairs_final.append([each_column,full_adder_pair,full_adder_carry_pair,[i, i+1, i+2]])
        return half_adder_full_adder_pairs_final

    def get_exact_compressor_pairs_final(splitted_columns_array_final):
        for i in range(len(splitted_columns_array_final)):
            each_column = splitted_columns_array_final[i]
            if i == len(splitted_columns_array_final) - 1:
                exact_compressor_pairs_final.append([each_column,None,i])
            else:
                if get_effective_length_of_column(each_column) == 4:
                    next_column = splitted_columns_array_final[i+1]
                    exact_compressor_pairs_final.append([each_column,next_column,i])
        return exact_compressor_pairs_final

    half_adder_full_adder_pairs_final = get_half_adder_full_adder_pairs_final(splitted_columns_array_final)
    exact_compressor_pairs_final = get_exact_compressor_pairs_final(splitted_columns_array_final)


    def half_adder_full_adder_pair_final_not_contains(i):
        for each_array in half_adder_full_adder_pairs_final:
            if each_array[3] == i :
                return False
        return True


    cout_array_final = []


    def get_half_adder_full_adder_pair_final(index):
        for each_pair in half_adder_full_adder_pairs_final:
            i = each_pair[3][0]
            if i == index:
                return each_pair
        

    result_final = {}

    def get_cary_in_from_cout_final_array(index):
        for each_array in cout_array_final :
            if each_array[0] == index:
                return each_array[1]


    def get_exacy_compressor_pair_final(index):
        for each_pair in exact_compressor_pairs_final:
            if each_pair[2] == index:
                return each_pair


    for i in range(len(splitted_columns_array_final)):
        current_column = splitted_columns_array_final[i]
        i_of_next_column, j_of_next_column = i+1, j+1
        if get_effective_length_of_column(current_column) == 1:
            sum = current_column[0]
            result_final[i]=[sum,None]
        elif get_effective_length_of_column(current_column) == 2 :
            sum = current_column[0]
            carry = current_column[1]
            result_final[i]=[sum,carry]
        elif get_effective_length_of_column(current_column)== 3 and not result_already_present(i,result_final):
            result = get_half_adder_full_adder_pair_final(i)
            half_adder_pair = result[0]
            full_adder_pair = result[1]
            full_adder_carry_pair = result[2]
            i_half_adder_pair, i_full_adder_pair, i_full_adder_carry_pair = result[3][0],result[3][1],result[3][2]
            sum_half_adder, cout_half_adder = half_adder(half_adder_pair[0], half_adder_pair[1])
            carry_half_adder = half_adder_pair[2]
            sum_full_adder, cout_full_adder = full_adder(full_adder_pair[0],full_adder_pair[1],cout_half_adder)
            carry_full_adder = full_adder_pair[2]
            result_final[i_half_adder_pair] = [sum_half_adder,carry_half_adder]
            result_final[i_full_adder_pair] = [sum_full_adder,carry_full_adder]
            sum_final_carry,cout_final_carry,carry_final_carry = exact_compressor(full_adder_carry_pair,cout_full_adder)
            result_final[i_full_adder_carry_pair] = [sum_final_carry,carry_final_carry]
            cout_array_final.append([i_full_adder_carry_pair, cout_final_carry])
        elif get_effective_length_of_column(current_column) == 4 and not result_already_present(i, result_final):
            exact_compressor_pair = get_exacy_compressor_pair_final(i)
            next_column = exact_compressor_pair[1]
            c_in_first_column = get_cary_in_from_cout_final_array(i-1)
            sum_first_array, cout_first_array, carry_first_array = exact_compressor(current_column,c_in_first_column)
            result_final[i] = [sum_first_array,carry_first_array]
            if i != len(splitted_columns_array_final) - 1:
                sum_second_array, cout_second_array, carry_second_array = exact_compressor(next_column,cout_first_array)
                cout_array_final.append([i,cout_second_array])
                result_final[i] = [sum_second_array,carry_second_array]

    final_bit_array = []

    for i in range(len(splitted_columns_array_final)):
        final_result_bits = result_final[i]
        if final_result_bits[1] is not None:
            final_sum = final_result_bits[0] or final_result_bits[1]
            final_bit_array.append(final_sum)
        else :
            final_bit_array.append(final_result_bits[0])



    def convert_bin_array_to_decimal(bin_array):
        value =0 
        for i in range(len(bin_array)):
            digit = bin_array.pop()
            if digit == 1:
                value = value + pow(2, i)
        return value

    return convert_bin_array_to_decimal(final_bit_array)


def generate_input_numbers():
    first_number = 0b0000000000000000
    last_number = 0b1111111111111111
    result = []
    for i in range(first_number + 1, last_number):
        result.append(i)
    return result

def generate_multiplier_multiplicand_pair_array():
    multipliers = generate_input_numbers()
    multiplicands = generate_input_numbers()
    result = []
    for each_multiplier in multipliers:
        for each_multiplicand in multiplicands:
            result.append([each_multiplicand,each_multiplier])
    return result
# multiplier_multiplicand_pair_array = generate_multiplier_multiplicand_pair_array()


# med1 = 0
# med2 = 0
# med3 = 0
# med4 = 0
# mred1 = 0
# mred2 = 0
# mred3 = 0
# mred4 = 0
# nmed1 = 0
# nmed2 = 0
# nmed3 = 0
# nmed4 = 0
# for each_pair in multiplier_multiplicand_pair_array:
#     multiplier = each_pair[0]
#     multiplicand = each_pair[1]
#     med1 = med1 + (exact_compressor_final(multiplier, multiplicand) - approximate_compressor_final(multiplier,multiplicand))
#     med2 = med2 + (exact_compressor_final(multiplier, multiplicand) - approximate_in_seven_and_eight_final(multiplier,multiplicand))
#     med3 = med3 + (exact_compressor_final(multiplier, multiplicand) - approximate_in_seven_eight_nine_final(multiplier,multiplicand))
#     med4 = med4 + (exact_compressor_final(multiplier, multiplicand) - approximate_in_seven_to_twelve_final(multiplier,multiplicand))
#     mred1 = mred1 + ((exact_compressor_final(multiplier, multiplicand) - approximate_compressor_final(multiplier,multiplicand))/exact_compressor_final(multiplier,multiplicand))
#     mred2 = mred2 + ((exact_compressor_final(multiplier, multiplicand) - approximate_in_seven_and_eight_final(multiplier,multiplicand))/exact_compressor_final(multiplier,multiplicand))
#     mred3 = mred3 + ((exact_compressor_final(multiplier, multiplicand) - approximate_in_seven_eight_nine_final(multiplier,multiplicand))/exact_compressor_final(multiplier,multiplicand))
#     mred4 = mred4 + ((exact_compressor_final(multiplier, multiplicand) - approximate_in_seven_to_twelve_final(multiplier,multiplicand))/exact_compressor_final(multiplier,multiplicand))


# med1 = med1 /len(multiplier_multiplicand_pair_array)
# med2 = med2 /len(multiplier_multiplicand_pair_array)
# med3 = med3 /len(multiplier_multiplicand_pair_array)
# med4 = med4 /len(multiplier_multiplicand_pair_array)
# mred1 = mred1/len(multiplier_multiplicand_pair_array)
# mred2 = mred2/len(multiplier_multiplicand_pair_array)
# mred3= mred3/len(multiplier_multiplicand_pair_array)
# mred4= mred4/len(multiplier_multiplicand_pair_array)


# print(f"MED of Approximate Compressor : {med1}")

# print(f"MED of Approximate Compressor 7,8 : {med2}")

# print(f"MED of Approximate Compressor 7,8,9 : {med3}")

# print(f"MED of Approximate Compressor 7,8,9,10,11,12 : {med4} ")


# print(f"MRED of Approximate Compressor : {mred1}")

# print(f"MRED of Approximate Compressor 7,8 : {mred2}")

# print(f"MRED of Approximate Compressor 7,8,9 : {mred3}")

# print(f"MRED of Approximate Compressor 7,8,9,10,11,12 : {mred4}")




def dct2(block):
    print(block)
    M, N = block.shape
    dct_block = np.zeros_like(block, dtype=np.float64)

    for u in range(M):
        for v in range(N):
            cu = 1.0 / np.sqrt(2) if u == 0 else 1.0
            cv = 1.0 / np.sqrt(2) if v == 0 else 1.0

            sum_val = 0.0
            for x in range(M):
                for y in range(N):
                    sum_val += approximate_compressor_final(x,y) * np.cos((2 * x + 1) * u * np.pi / (2 * M)) * np.cos(
                        (2 * y + 1) * v * np.pi / (2 * N)
                    )

            dct_block[u, v] = cu * cv * sum_val / np.sqrt(M * N)

    return dct_block

def idct2(block):
    M, N = block.shape
    idct_block = np.zeros_like(block, dtype=np.float64)

    for x in range(M):
        for y in range(N):
            sum_val = 0.0
            for u in range(M):
                for v in range(N):
                    cu = 1.0 / np.sqrt(2) if u == 0 else 1.0
                    cv = 1.0 / np.sqrt(2) if v == 0 else 1.0

                    sum_val += cu * cv * block[u, v] * np.cos((2 * x + 1) * u * np.pi / (2 * M)) * np.cos(
                        (2 * y + 1) * v * np.pi / (2 * N)
                    )

            idct_block[x, y] = sum_val / np.sqrt(M * N)

    return idct_block

def apply_dct(image):
    image_array = np.array(image, dtype=np.uint16)
    dct_image = np.zeros_like(image_array, dtype=np.float64)

    for i in range(0, image_array.shape[0], 8):
        for j in range(0, image_array.shape[1], 8):
            dct_image[i:i+8, j:j+8] = dct2(image_array[i:i+8, j:j+8])

    return dct_image

def apply_idct(dct_image):
    image_array = np.zeros_like(dct_image, dtype=np.uint16)

    for i in range(0, image_array.shape[0], 8):
        for j in range(0, image_array.shape[1], 8):
            image_array[i:i+8, j:j+8] = idct2(dct_image[i:i+8, j:j+8])

    return np.clip(image_array, 0, 65535).astype(np.uint16)

image_path = './lena1.jpg'
original_image = Image.open(image_path).convert('L')  # Convert to grayscale

dct_image = apply_dct(original_image)

idct_image = apply_idct(dct_image)
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(original_image, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(np.log1p(np.abs(dct_image)), cmap='gray')
plt.title('DCT Image')

plt.subplot(1, 3, 3)
plt.imshow(idct_image, cmap='gray')
plt.title('IDCT Image')

plt.show()