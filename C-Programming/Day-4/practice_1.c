# include <stdio.h>

//  program to check if the given number is a natural number. 

int main() {
    int a;
    printf("enter a no.:");
    scanf("%d",&a);
    if (a>0){
        printf("%d is a natural no.",a); }
    else {
        printf("%d is not a natural no.",a);
    }

    return 0;
    }