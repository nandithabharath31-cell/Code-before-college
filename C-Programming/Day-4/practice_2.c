# include <stdio.h>

/* multiplication table of n*/

int main() {
    int num;
    printf("enter a no.");
    scanf("%d",&num);

    for (int i=1;i<=10;i++){
        printf("%d X %d = %d \n" , num , i , num*i);
    }
}