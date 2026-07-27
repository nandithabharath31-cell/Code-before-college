#include<stdio.h>
 
int main() { 
    int num; 
    printf("Enter an integer : ");
    scanf("%d", &num);
    switch(num){
        case 1 : printf("monday \n");
        break;
        case 2 : printf("tuesday \n");
        break;
        case 3 : printf("wednesday  \n");
        break;
        case 4 : printf("thursday \n");
        break;
        case 5 : printf("friday \n");
        break;
        case 6 : printf("saturday \n");
        break;
        case 7 : printf("sunday \n");
        break;
        default : printf("invalid number \n");
    }
    return 0;
}