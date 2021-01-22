#include <stdio.h>

int n;

int fact(n)
{
    if (n <= 0)
    {
        return 1;
    }
    else
    {
        return fact(n - 1) * n;
    }
}

int main()
{
    scanf("%d", &n);
    printf("%d", fact(n));

    return 0;
}