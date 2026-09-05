#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
    char buf[20];
    puts("could you get the shell?\n");
    gets(buf);
}

int main() {
    puts("Hi, welcome to easy challs");
    puts("i bet you can solve this one under 5 minutes");
    puts("Try: ");
    vuln();
    printf("Okay byeee!!");
    return 0;
}