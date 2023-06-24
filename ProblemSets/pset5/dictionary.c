// Implements a dictionary's functionality
#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;
// Choose number of buckets in hash table
const unsigned int N = 26;
// Hash table
node *table[N];
// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Convert word to lowercase
    char lowercase_word[LENGTH + 1];
    int i = 0;
    while (word[i] != '\0')
    {
        lowercase_word[i] = tolower(word[i]);
        i++;
    }
    lowercase_word[i] = '\0';
    // Compute hash value
    int index = hash(lowercase_word);
    // Traverse the linked list at the hash index
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // Compare lowercase word with dictionary word
        if (strcmp(lowercase_word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    // Word not found in dictionary
    return false;
}
// Hashes word to a number
unsigned int hash(const char *word)
{
    // Simple hash function based on the sum of ASCII values of characters
    unsigned int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value += word[i];
    }
    return hash_value % N;
}
// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", dictionary);
        return false;
    }

    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    // Buffer for reading words from file
    char word[LENGTH + 1];
    // Read words from dictionary and insert into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            unload();
            return false;
        }
        // Copy word into node
        strcpy(new_node->word, word);
        // Compute hash value
        int index = hash(word);
        // Insert new node into hash table
        new_node->next = table[index];
        table[index] = new_node;
    }
    // Close dictionary file
    fclose(file);
    // Dictionary successfully loaded
    return true;
}
// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Traverse the hash table to count the number of words
    unsigned int word_count = 0;
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            word_count++;
            cursor = cursor->next;
        }
    }
    return word_count;
}
// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Traverse the hash table and free memory for each node
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}