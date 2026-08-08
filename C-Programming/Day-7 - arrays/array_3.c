# include <stdio.h>

void storetable(int arr[][10] , int n , int m , int number);

int main() {
    int tables[2][10];
    storetable(tables , 0 , 10 , 2);
    storetable(tables ,1 ,10 , 3);

    for (int i=0 ; i<10 ; i++){
        printf("%d \t" , tables[0][i]);
    }
    printf("\n");

    for (int i=0 ; i<10 ; i++){
        printf("%d \t" , tables[1][i]);
    }
    printf("\n");
    return 0;


}

void storetable(int arr[][10] , int n , int m , int number) {
    for (int i = 0 ; i<m ; i++){
        arr[n][i]=number * (i+1) ;

    }
}