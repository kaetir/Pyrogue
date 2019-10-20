
def fib_rec(n):
    """
    @brief fonction de fibonacci récursive
    """
    return n if n < 2 else fib_rec(n - 1) + fib_rec(n - 2)

