def print_integer_sum(number):
    result = 0
    for i in range(number+1):
        result = result + i
    print(result)


n = input("Entrez un nombre : ")
print_integer_sum(int(n))
