def algoritm(summ):
    # Добавление в список


    spis_n = []

    spis_a = []

    a = ''
    for i in summ:
        if i != ' ':
            if i == '-' or i == '+' or i == '/' or i == '*':
                spis_n.append(int(a))
                spis_a.append(i)
                a = ''
            else:
                a = a+i


    spis_n.append(int(a))

    #Вычисления


    summ_arifm = spis_n[0]

    i_spis_n = 1

    for i in spis_a:

        if i == '+':
            summ_arifm += spis_n[i_spis_n]

        if i == '-':
            summ_arifm -= spis_n[i_spis_n]

        if i == '/':
            try:
                summ_arifm /= spis_n[i_spis_n]
            except ZeroDivisionError:
                print("")

        if i == '*':
            summ_arifm *= spis_n[i_spis_n]

        i_spis_n += 1


    return summ_arifm






while True:
    print("\n",algoritm(input()))
    print(' ----------- \n')