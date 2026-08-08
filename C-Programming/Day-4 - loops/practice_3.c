# include <stdio.h>

/* to take no.s from user until odd no. is enterd*/

int main(){
    int n;
    while(1){
        printf("enter a no.\n");
        scanf("%d",&n);
        if (n%2!=0){
            printf("odd no.");
            break;
        }
    }
    return 0;

}