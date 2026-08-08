# include <stdio.h>

// to check if a no. is prime

int main() {
    int n;
    printf("enter a no");
    scanf("%d",&n);
    int f=0;

    for (int i=1;i<=n;i++){
        if (n%i==0){
            f++;
        }
    }
    if (f==2){
        printf("%d is a prime no.", n);
    }
    else {
        printf("%d is not prime no.",n);
    }
    return 0;
}