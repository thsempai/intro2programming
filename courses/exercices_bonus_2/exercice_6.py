def integer_sum_1(number):
    result = 0
    if number > 0:
        for i in range(number+1):
            result = result + i
    else:
        for i in range(number, 0):
            result = result + i
    return result


def integer_sum_2(number):
    result = 0
    for i in range(min(number, 0), max(0, number+1)):
        result = result + i
    return result


n = input("Entrez un nombre : ")

res1 = integer_sum_1(int(n))
print(res1)

res2 = integer_sum_2(int(n))
print(res2)
