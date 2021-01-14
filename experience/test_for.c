#include <stdio.h>
#include <stdlib.h>

int sum;

int main()
{
    sum = 0;

    for (int i = 1; i < 11; i++)
    {
        sum += i;
    }

    return 0;
}