#include <stdio.h>
#include <cs50.h>
int main()
{
    int n;
    do
    {
        n = get_int("Start size: ");
    } while (n > 1300);
    int n2;
    do
    {
        n2 = get_int("End size: ");
    } while (n2 < n);
    int i = 0;
    while (n < n2)
    {
        n = n + (n / 3) - (n / 4);
        i++;
    }
    printf("Year: %i\n", i);
}