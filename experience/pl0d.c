#include <stdio.h>

int n, temp;

void fact()
{
    int m;
    if (n <= 1)
    {
        temp = 1;
    }
    else
    {
        m = n;
        n = n - 1;
        fact();
        temp = temp * m;
    }
}

int main()
{
    scanf("%d", &n);
    fact();
    printf("%d\n", temp);

    return 0;
}