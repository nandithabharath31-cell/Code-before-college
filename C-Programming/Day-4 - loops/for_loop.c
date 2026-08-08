# include <stdio.h>

/* print sum of no. from 1-n and print the no.s in reverse order*/
int main() {
    int sum=0,num;
    printf("enter a no.");
    scanf("%d", &num);
    for (int i=1,j=num ; i<=num && j>=1 ; i++,j-- ) {
        sum=sum+i;
        printf("%d \n",j);


    }
    printf("sum is %d \n",sum);
    return 0;

}