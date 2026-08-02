# include <stdio.h>
# include <string.h>

// func to count the occurrence of vowel in the string

void vowel(char str[]);

int main(){
    char str[100];
    printf("enter a string");;
    scanf("%s",str);
    vowel(str);
    return 0;
}

void vowel(char str[]){
    int count=0;
    char *v="aeiou";
    for (int i=0 ; str[i]!='\0';i++){
        char ch = str[i];
        if (strchr(v,ch) != NULL){
            count++;
        }

    }
    printf("%d",count);
}