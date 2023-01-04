def remove_percent(input):
    if (input == '-'):
        return 'null'
    return float(input[:-1]) / 100


def to_number(input):
    if (input == '-'):
        return 'null'
    magnitude = ['K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if (input[-1] not in magnitude):
        return float(input)
    return float(input[:-1]) * pow(1e3, magnitude.index(input[-1]) + 1)


def remove_comma(input):
    if (input == '-'):
        return 'null'
    result = ''
    for i in input:
        if i != ',':
            result += i
    return result


def list_to_string(input):
    output = ''
    for i in input:
        output += "'" + str(i) + "',"
    output = output[:-1]
    return output


# turn a list into valid form
# data1 = ["Bitcoin","Dec 18, 2022","16,717.0","16,777.0","16,797.3","16,666.5","124.18K","-0.36%"]
# validate(data1) = "'Bitcoin','Dec 18, 2022','16717.0','16777.0','16797.3','16666.5','124180.0','-0.0036'"
# data2 = ["Bitcoin", "Dec 18, 2022", "16,717.0","16,777.0", "-", "16,666.5", "-", "-"]
# validate(data2) = "'Bitcoin','Dec 18, 2022','16717.0','16777.0','null','16666.5','null','null'"


def validate(input):
    for i in range(2, 6):
        input[i] = remove_comma(input[i])     # Price, Open, High, Low
    input[6] = to_number(input[6])            # Vol.
    input[7] = remove_percent(input[7])       # Change
    return list_to_string(input)
