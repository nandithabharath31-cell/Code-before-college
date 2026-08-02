# include <stdio.h>
# include <string.h>

int main() {

    // strlen  func
    char name[] = "nanditha";
    printf("length is : %d \n" ,strlen(name));

    //strcpy func
    char oldstr[] = "oldstr";
    char newstr[] = "newstr";
    strcpy(newstr,oldstr);
    puts(newstr);

    //strcat
    char firststr[100] = "hello";
    char secstr[] = "world";
    strcat(firststr,secstr);
    puts(firststr);

    //strcmp
    char s1[] = "APPLE"; //ascii value of A=65 , B=66
    char s2[] = "BANANA";
    char s3[] = "APPLE";
    int lesser=strcmp(s1,s2);
    int greater = strcmp(s2,s1);
    int equal = strcmp(s1,s3);
    printf("%d %d %d",lesser,greater,equal);

    return 0;

}