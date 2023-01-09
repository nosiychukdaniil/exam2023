def from12to10(n):
    a = list(n)
    b = []
    for i in a:
        try:
            b.append(int(i))
        except:
            if i in 'Aa':
                b.append(10)
            elif i in 'Bb':
                b.append(11)
            else:
                print("Введите другое число")
                break
    return b
    print(b)
    
    # c= []
    # for i in a:
    #     try
    #         if type(int(i)) == int:
    #             if int(i) >
    #             if i in 'Aa':
    #                 c.append(10)
    #             elif i in 'Bb':
    #                 c.append(11)
    #             else:
    #                 print('Введите другое число')
    #                 break
    #             elif int(i) < 10:
    #                 c.append(i)
    #             else:
    #                  print('asd')
    # return c

print(from12to10('12AB89ab123346B'))



