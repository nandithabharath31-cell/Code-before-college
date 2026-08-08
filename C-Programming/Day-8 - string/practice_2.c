# include <stdio.h>

//take a string input from th user using %c

int main() {
    char str[100];
    int i=0;
    char ch;

    while (ch != '\n'){
        scanf("%c" , &ch);
        str[i]=ch;
        i++;
    }
    str[i]='\0';
    puts(str);
    return 0;
}
