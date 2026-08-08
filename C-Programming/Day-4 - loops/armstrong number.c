# include <stdio.h>
# include <math.h>

int main() {
    int num , sum=0 , len=0 , cnum;
    printf("Enter a number : ");
    scanf("%d", &num);

    cnum=num;

    while (cnum%10!=0){
        len++;
        cnum=cnum/10;
    }

    cnum = num;

    for (int i=1;i<=len;i++){
        sum=sum + round(pow(cnum%10,len));
        cnum = cnum/10;

    }
    if ((int)sum== num){
        printf("%d is an Armstrong number.\n", num);
    }
    else {
        printf("%d is not an Armstrong number.\n", num);}

    return 0;
}
    