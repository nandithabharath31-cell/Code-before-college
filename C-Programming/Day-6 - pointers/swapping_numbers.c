# include <stdio.h>
void swap(int *a , int *b);

int main(){
    int x=3 , y=5 ;
    printf("original no. : x = %d , y = %d \n" , x ,y);
    swap(&x ,&y);
    printf("swaped no. : x = %d , y = %d" , x ,y);
    return 0;
}

void swap(int *a , int *b){
   int t= *a;
    *a = *b ;
    *b = t;
}