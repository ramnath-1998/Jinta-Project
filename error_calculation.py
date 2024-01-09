def generate_input_numbers():
    first_number = 0b1000000000000000
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
            if len(result) == 10000000 :
                return result
    return result
multiplier_multiplicand_pair_array = generate_multiplier_multiplicand_pair_array()
