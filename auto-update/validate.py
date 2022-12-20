def remove_percent(str):
    return float(str[:-1]) / 100


def to_number(str):
    magnitude = ['K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if (str[-1] not in magnitude):
        return float(str)
    return float(str[:-1]) * pow(1e3, magnitude.index(str[-1]) + 1)


def remove_comma(str):
    ans = ''
    for i in str:
        if i != ',':
            ans += i
    return ans


# turn a list into valid form
# data = ["Dec 18, 2022","16,717.0","16,777.0","16,797.3","16,666.5","124.18K","-0.36%"]
# line_validation(data) = ['Dec 18, 2022', '16717.0', '16777.0', '16797.3', '16666.5', 124180.0, -0.0036]
def validate(list):
    for i in range(1, 5):
        list[i] = remove_comma(list[i]) # Price, Open, High, Low
    list[5] = to_number(list[5])        # Vol.
    list[6] = remove_percent(list[6])   # Change
    return list
