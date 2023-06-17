#include <stdio.h>
#include <cs50.h>
int main()
{
    int n;
    do
    {
        n = get_int("Height: ");
    } while (n < 1);
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= n - i; j++)
        {
            printf("·");
        }
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
