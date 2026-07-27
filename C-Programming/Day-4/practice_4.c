# include <stdio.h>
// to print factorial of n

int main(){
    int p=1,n;
    printf("enter a no.");
    scanf("%d",&n);
    for (int j=1;j<=n;j++){
        p=p*j;
    }
printf("the factorial of %d is %d" , n , p);
return 0;


}