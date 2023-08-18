def remove_percent(input):
    return 'null' if (input == '-') else float(input[:-1]) / 100


def to_number(input):
    if (input == '-'):
        return 'null'
    magnitude = ['K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if (input[-1] not in magnitude):
        return float(input)
    return float(input[:-1]) * pow(1e3, magnitude.index(input[-1]) + 1)


def remove_comma(input):
    return 'null' if (input == '-') else ''.join(i for i in input if i != ',')


def list_to_string(input):
    output = ''.join(f"'{str(i)}'," for i in input)
    return output[:-1]


# turn a list into valid form
# data1 = ["Bitcoin","Dec 18, 2022","16,717.0","16,777.0","16,797.3","16,666.5","124.18K","-0.36%"]
# validate(data1) = "'Bitcoin','Dec 18, 2022','16717.0','16777.0','16797.3','16666.5','124180.0','-0.0036'"
# data2 = ["Bitcoin", "Dec 18, 2022", "16,717.0","16,777.0", "-", "16,666.5", "-", "-"]
# validate(data2) = "'Bitcoin','Dec 18, 2022','16717.0','16777.0','null','16666.5','null','null'"


def validate(input):
    for i in range(2, 8):
        input[i] = remove_comma(input[i])     # Price, Open, High, Low
    input[6] = to_number(input[6])            # Vol.
    input[7] = remove_percent(input[7])       # Change
    return list_to_string(input)
