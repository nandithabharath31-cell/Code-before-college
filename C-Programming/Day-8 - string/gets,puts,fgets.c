# include <stdio.h>

int main(){
    //gets , fgets , puts
    char school[40];
    printf("enter school studied in");
    fgets(school , 40 , stdin);
    puts("u studied in");
    puts(school);
}