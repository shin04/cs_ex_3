#include <stdio.h>
#include <stdlib.h>

int a;

void proc()
{
    int b;
    b = 10;
    a = b;
}

int main()
{
    proc();

    return a;
}