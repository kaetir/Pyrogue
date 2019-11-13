
fibo_const = [0, 1]

def fib_rec(n):
    """
    @summary fonction de fibonacci NON recursive
    @param n: int le nombre dont on veut la valeur dans la suite
    """
    if len(fibo_const) - 1 < n:
        a, b, cpt = fibo_const[len(fibo_const) - 2], fibo_const[len(fibo_const) - 1], len(fibo_const) - 1
        c = 0
        while cpt <= n:
            if cpt < 2:
                c = cpt
            else:
                c = a + b
                fibo_const.append(c)
                a = b
                b = c
            cpt += 1
        return c
    # else:
    return fibo_const[n]
    #return n if n < 2 else fib_rec(n - 1) + fib_rec(n - 2)

