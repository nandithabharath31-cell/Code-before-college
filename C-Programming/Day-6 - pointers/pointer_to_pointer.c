# include <stdio.h>

int main() {
    int age = 18 ;
    int *ptr = &age ;
    int **pptr = &ptr ;
    printf("%d", **pptr);
    return 0;

}