# include <stdio.h>
// print factorial of no. using recursion
int fact(int n);

int main () {
    int n;
    printf("enter a no.");
    scanf("%d",&n);
    printf("factorial of %d is : %d",n , fact(n));
    return 0;
}

int fact (int n){
    if (n==0) {
        return 0;
    }
    int factNM1 = fact(n-1);
    int factN = factNM1 * n ;
    return factN ;
}