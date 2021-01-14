#include <stdio.h>
#include <stdlib.h>

int a;

void proc()
{
    a = 10;
}

int main()
{
    proc();

    return a;
}