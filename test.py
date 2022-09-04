def sum_range(a,b):
    c,d = a,b
    if b > a:
        c,d = b,a
    return (a+b)*(c-d+1)//2

print(sum_range(1,100))