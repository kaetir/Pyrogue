
def fib_rec(n):
    """
    @brief fonction de fibonacci récursive
    @param n: int le nombre dont on veut la valeur dans la suite
    """
    return n if n < 2 else fib_rec(n - 1) + fib_rec(n - 2)

