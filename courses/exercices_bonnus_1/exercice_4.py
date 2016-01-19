
def p(n, m=1):
	r = 1
	
	for i in range(m):
	r = r * n

	return r

print(p(4,2) + p(3,3) + p(2)) 
