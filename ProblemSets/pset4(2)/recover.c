#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    // Open the memory card image file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    uint8_t buffer[BLOCK_SIZE];
    int count = 0;
    FILE *jpeg = NULL;
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the previous JPEG file, if open
            if (jpeg != NULL)
            {
                fclose(jpeg);
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", count);
            jpeg = fopen(filename, "w");
            if (jpeg == NULL)
            {
                printf("Could not create JPEG file.\n");
                fclose(file);
                return 1;
            }
            count++;
        }
        // Write the block to the JPEG file
        if (jpeg != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, jpeg);
        }
    }
    // Close the last JPEG file
    if (jpeg != NULL)
    {
        fclose(jpeg);
    }
    fclose(file);
    return 0;
}