# include <stdio.h>

int main() {
    FILE *fptr;
    fptr = fopen ("fruits.txt" ,"w");
    fputc('m',fptr);
    fputc('a',fptr);
    fputc('n',fptr);
    fputc('g',fptr);
    fputc('o',fptr);

    fputc('\n',fptr);

    fputc('a',fptr);
    fputc('p',fptr);
    fputc('p',fptr);
    fputc('l',fptr);
    fputc('e',fptr);

    fclose(fptr);

    fptr = fopen("fruits.txt","r");
    char ch;
    while (ch != EOF){
        ch = fgetc(fptr);
        printf("%c",ch);
        
    }
   


    fclose(fptr);
    return 0;
}