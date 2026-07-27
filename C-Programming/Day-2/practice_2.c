# include<stdio.h>

int main() {
    char ch;
    printf("enter a character");
    scanf("%c", &ch);
    if(ch>='1' && ch<='9')
    {
        printf("the character is a digit");
    }
    else
    {
        printf("the character is not a digit");
    }
    return 0;
}