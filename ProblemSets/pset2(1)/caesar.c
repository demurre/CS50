#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
void caesar_cipher(string text, int key);
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");
    caesar_cipher(plaintext, key);
    return 0;
}
void caesar_cipher(string text, int key)
{
    printf("ciphertext: ");

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isupper(text[i]))
        {
            char ciphertext = ((text[i] - 'A') + key) % 26 + 'A';
            printf("%c", ciphertext);
        }
        else if (islower(text[i]))
        {
            char ciphertext = ((text[i] - 'a') + key) % 26 + 'a';
            printf("%c", ciphertext);
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
}