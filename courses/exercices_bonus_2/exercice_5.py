def integer_sum(number):
    result = 0
    for i in range(number+1):
        result = result + i
    return result


n = input("Entrez un nombre : ")
res = integer_sum(int(n))
print(res)
