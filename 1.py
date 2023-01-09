def from12to10(n):
    a = list(n)
    c= []
    for i in a:
        if i == 'A':
            c.append(10)
        elif i == 'B':
            c.append(11)
        elif type(int(i)) == int:
            c.append(i)
        else:
            print('asd')
    return c

print(from12to10('12AB'))