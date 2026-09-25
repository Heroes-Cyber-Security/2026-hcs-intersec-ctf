#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NAME_LEN 32

static void setup(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(void)
{
    char flag[128];
    FILE *f = fopen("flag.txt", "r");

    if (f == NULL) {
        puts("flag.txt not found, contact admin!");
        exit(1);
    }

    if (fgets(flag, sizeof(flag), f) == NULL) {
        puts("failed to read flag, contact admin!");
        fclose(f);
        exit(1);
    }

    fclose(f);

    printf("Congratulations, welcome to HCS!\n%s", flag);
}

static void vuln(void)
{
    char name[NAME_LEN];

    puts("Welcome to HCS! Before we let you in, what's your name?");
    printf("> ");
    gets(name); /* the vuln: no bounds checking */

    printf("Nice to meet you, %s! See you around.\n", name);
}

int main(void)
{
    setup();
    puts("=== Welcome to HCS ===");
    vuln();
    return 0;
}
