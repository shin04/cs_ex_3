#include <stdarg.h>
#include <stdio.h>

int sumf(int nfirst, ...)
{
    int r = 0, n;
    va_list args;

    va_start(args, nfirst);
    for (n = nfirst; n != 0; n = va_arg(args, int))
        r += n;
    va_end(args);

    return r;
}

int main()
{
    int r = sumf(1, 2, 3, 4, 5, 6);
    printf("%d", r);

    return 0;
}