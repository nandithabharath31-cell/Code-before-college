#include<stdio.h>

int main() { 
    char day; 
    printf("Enter day character (m/t/w/T/f/s/S) : ");
    scanf("%s", &day);
    switch(day){
        case 'm' : printf("monday \n");
        break;
        case 't' : printf("tuesday \n");
        break;
        case 'w' : printf("wednesday \n");
        break;
        case 'T' : printf("thursday \n");
        break;
        case 'f' : printf("friday \n");
        break;
        case 's' : printf("saturday \n");
        break;
        case 'S' : printf("sunday \n");
        break;
        default : printf("invalid day \n");
    }
    return 0;
}