# include <stdio.h>
//reading from student.txt file

int main() {
    FILE *fptr;
    fptr = fopen("student.txt","r");
    char str[100];

    if (fptr == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    //while (fscanf(fptr, "%s", str) != EOF) {
    //   printf("%s", str);
    //}

    char ch;

    while(ch != EOF){
        printf("%c" , ch);
        ch=fgetc(fptr);

    }

        
    
    fclose(fptr);
    return 0;
    

}