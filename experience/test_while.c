#include <stdio.h>
#include <stdlib.h>

int n, sum;

int main()
{
   n = 10;
   sum = 0;

   while (n > 0)
   {
      sum += n;
      n -= 1;
   }

   return 0;
}
