#include <stdio.h>

int i, j, n, a[100];

void initialize(n)
{
    int i;
    for (i = 1; i <= n; i++)
    {
        scanf("%d", &a[i]);
    }
}

void swap(j)
{
    int temp;
    temp = a[j];
    a[j] = a[j + 1];
    a[j + 1] = temp;
}

int main()
{
    scanf("%d", &n);
    if (n <= 100)
    {
        initialize(n);
        i = n;
        while (1 <= i)
        {
            j = 1;
            while (j < i)
            {
                if (a[j] > a[j + 1])
                {
                    swap(j);
                }
                j = j + 1;
            }
            printf("%d", a[i]);
            i = i - 1;
        }
    }
}