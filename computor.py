
import sys
import re
from graph import graph

def get_polynomial_indexes(terms_arr):
    indexes_dict = dict()

    for term in terms_arr:
        term_part = re.split('\*?X\^?', term)
        is_power_part_exist = len(term_part) > 1

        term_sign = -1 if term_part[0][0] == '0' else 1

        term_power = int(term_part[1]) if is_power_part_exist and len(term_part[1]) > 0 else int(is_power_part_exist)
        term_index = float(term_part[0]) if len(term_part[0]) > 1 else term_sign

        if term_power in indexes_dict.keys():
            indexes_dict[term_power] += term_index
        else:
            indexes_dict[term_power] = term_index

    return indexes_dict


def get_polynomial_terms(polynomial_part):
    polynomial = str(polynomial_part).replace(' ', '')
    
    if len(polynomial) == 0:
        raise Exception()
    elif polynomial[0] not in '-+':
        polynomial = f'+{polynomial}'
    
    term_starts = [it.start() for it in re.finditer(r'[+-]', polynomial)][::-1]

    terms = []
    previous_start = len(polynomial)
    for start in term_starts:
        terms.append(polynomial[start:previous_start])
        previous_start = start

    if len(terms) == 0:
        raise Exception()
    
    return terms


def pars_argv(argv):
    polynomial_arr = str(argv).partition('=')

    left_polynomial_terms = get_polynomial_terms(polynomial_arr[0])
    right_polynomial_terms = get_polynomial_terms(polynomial_arr[2])

    left_index_arr = get_polynomial_indexes(left_polynomial_terms)
    right_index_arr = get_polynomial_indexes(right_polynomial_terms)

    for (key, value) in right_index_arr.items():
        if key in left_index_arr.keys():
            left_index_arr[key] -= value
        else:
            left_index_arr[key] = -value

    return left_index_arr


def get_index_to_term(i, power):

    index_part = f'{"+ " if i >= 0.0 else ""}{i}'
    power_part = '' if power == 0 else '*X'

    if power > 1:
        power_part += f'^{power}'

    return f'{index_part}{power_part}' 

def print_polynomial(indexes_arr):
    result_polynomial = [get_index_to_term(indexes_arr[i], i) for i in [*indexes_arr.keys()][::-1] if indexes_arr[i] != 0.0 ]
    result_polynomial += f"{'' if len(result_polynomial) > 0 else '0'}=0" 
    print(*result_polynomial)


def resolve_equation(index_arr):
    keys = index_arr.keys()
    a = index_arr[2] if 2 in keys else 0.0
    b = index_arr[1] if 1 in keys else 0.0
    c = index_arr[0] if 0 in keys else 0.0
    
    if a != 0.0:
        D = b * b - 4 * a * c
        a2 = a * 2.0

        print(f"D = {D}")
        if D < 0:
            sqrt_D = -D ** 0.5
            print(f'D < 0. Solutions:')
            print(f' x1 = { -b / a2 } + i * { - sqrt_D / a2 }')
            print(f' x2 = { -b/ a2 } + i * { sqrt_D / a2 }')
        elif D == 0:
            print(f'D == 0. Solution: x = {-b / (a2)}')
        else:
            sqrt_D = D ** 0.5
            print(f'D > 0. Solutions:')
            print(f' x1 = { -(b + sqrt_D) / a2 }')
            print(f' x2 = { (-b + sqrt_D) / a2 }')

    elif b != 0.0:
        print(f'solution: x = {-c / b}')
    elif c != 0.0:
        print('The equation has no solutions')
    else:
        print('X є R')


def validate_polynomial(polynomial_arr):

    max_power = None
    min_power = None
    for term_power, term_index in polynomial_arr.items():
        if term_index == 0:
            continue

        max_power = term_power if max_power is None else max(term_power, max_power)
        min_power = term_power if min_power is None else min(term_power, min_power)
    
    max_power = 0 if max_power is None else max_power
    min_power = 0 if min_power is None else min_power

    print(f'Polynomial degree: {max_power}')
    if max_power > 2 or min_power < 0:
        raise Exception()


def main(comand_line_params):
    #Mandatory part: solving equation 
    try:
        index_arr = pars_argv(comand_line_params[1])
        print_polynomial(index_arr)
        validate_polynomial(index_arr)
        resolve_equation(index_arr)

    except Exception as ex:
        print('Can`t solve this equation ')

    #Bonus part: graph rendering
    try:
        index_arr = pars_argv(comand_line_params[1])
        graph(index_arr)
    except Exception as ex:
        print('Can`t create graph')

if __name__ == "__main__":
    main(sys.argv)
