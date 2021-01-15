#include <stdio.h>
#include <stdlib.h>

int a, b;

void func()
{
    a = 10;
    b = 1;
    if (a < b)
    {
        a++;
    }
    else
    {
        a--;
    }
}

int main()
{
    func();

    return 0;
}