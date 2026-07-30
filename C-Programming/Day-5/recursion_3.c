# include <stdio.h>
// to print the 4th no. in the fibonacci series
int fib(int n);

int main () {
    int n;
    printf("4th term in fibonacci series  is : %d",fib(4));
    return 0;
}

int fib (int n){
    if (n==0){
        return 0;
    }
    if (n==1){
        return 1;
    }
    int fibNM1 = fib(n-1);
    int fibNM2 = fib(n-2);
    int fibN = fibNM1 + fibNM2 ;
    return fibN ;
}