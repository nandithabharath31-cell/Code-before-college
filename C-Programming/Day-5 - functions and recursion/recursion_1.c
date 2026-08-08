# include <stdio.h>
// sum of first n natural no.
int sum(int n);

int main () {
    int n;
    printf("enter a no.");
    scanf("%d",&n);
    printf("sum is : %d",sum(n));
    return 0;
}

int sum (int n){
    if (n==1){
        return 1;
    }
    int sumNM1 = sum(n-1);
    int sumN = sumNM1 + n ;
    return sumN ;
}