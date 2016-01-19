
def mix(m1, m2):
	m3 = ""
	for index in range(len(m1)):
		if index < len(m2):
			m3 = m3 + m1[index] + m2(index)
	return m3
	
a = "Al ean rcan"
b = " asmiepohie"
print(mix(a, b)) 	

