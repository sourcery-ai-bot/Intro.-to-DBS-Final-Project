def remove_percent(str):
    if (str == '-'):
        return 'null'
    return float(str[:-1]) / 100


def to_number(str):
    if (str == '-'):
        return 'null'
    magnitude = ['K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if (str[-1] not in magnitude):
        return float(str)
    return float(str[:-1]) * pow(1e3, magnitude.index(str[-1]) + 1)


def remove_comma(str):
    if (str == '-'):
        return 'null'
    result = ''
    for i in str:
        if i != ',':
            result += i
    return result


# turn a list into valid form
# data1 = ["Bitcoin","Dec 18, 2022","16,717.0","16,777.0","16,797.3","16,666.5","124.18K","-0.36%"]
# validate(data1) = ['Bitcoin', 'Dec 18, 2022', '16717.0', '16777.0', '16797.3', '16666.5', 124180.0, -0.0036]
# data2 = ["Bitcoin", "Dec 18, 2022", "16,717.0","16,777.0", "-", "16,666.5", "-", "-"]
# validate(data2) = ['Bitcoin', 'Dec 18, 2022', '16717.0', '16777.0', 'null', '16666.5', 'null', 'null']


def validate(list):
    for i in range(2, 6):
        list[i] = remove_comma(list[i])     # Price, Open, High, Low
    list[6] = to_number(list[6])            # Vol.
    list[7] = remove_percent(list[7])       # Change
    return list
