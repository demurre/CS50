#include <ctype.h>
#include <stdio.h>
#include <cs50.h>
#include <math.h>
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int main(void)
{
    string text = get_string("Text: ");
    int num_letters = count_letters(text);
    int num_words = count_words(text);
    int num_sentences = count_sentences(text);
    // Calculate the Coleman-Liau index
    float L = (float)num_letters / num_words * 100.0;
    float S = (float)num_sentences / num_words * 100.0;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    // Print the grade level
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", index);
    }
    return 0;
}
// Function to count the number of letters in the text
int count_letters(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}
// Function to count the number of words in the text
int count_words(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isspace(text[i]))
        {
            count++;
        }
    }
    return count + 1; // Add 1 for the last word
}
// Function to count the number of sentences in the text
int count_sentences(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}
