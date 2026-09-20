/*
 * gosip — intersec's least trustworthy diary.
 *
 * built with:
 *   gcc gosip.c -o chall -fstack-protector-all -fPIE -pie \
 *        -Wl,-z,relro,-z,now -z noexecstack
 *
 * it just really, REALLY likes to talk.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NAME_LEN   23
#define SECRET_LEN 31
#define SEAT_LEN   55

static void setup(void)
{
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

static void banner(void)
{
    puts("=== gosip: intersec's least trustworthy diary ===");
    puts("   (tell it anything. it tells everyone.)");
}

int main(void)
{
    char name[NAME_LEN + 1];
    char secret[SECRET_LEN + 1];
    char seat[SEAT_LEN];
    int n;

    setup();
    banner();

    puts("\n[gosip] before you sit down... who are you?");
    n = read(0, name, NAME_LEN);
    if (n < 0) n = 0;
    name[n] = '\0';

    puts("[gosip] hehe... hi,");
    printf(name);
    putchar('\n');

    puts("\n[gosip] so... tell me a secret. i PROMISE i won't tell anyone.");
    n = read(0, secret, SECRET_LEN);
    if (n < 0) n = 0;
    secret[n] = '\0';

    puts("[gosip] wow. okay. well:");
    printf(secret);
    putchar('\n');

    puts("\n[gosip] curiosity killed the cat, and gosip killed the diary.");
    puts("[gosip] last words before it all burns?");
    read(0, seat, 0x200);

    puts("[gosip] ...it's all gone now.");
    return 0;
}
