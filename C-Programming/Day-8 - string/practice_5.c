# include <stdio.h>

//to check whether a character is in the string or not

void checkchar(char str[],char ch);

int main(){
    char str[] = "Nanditha";
    char ch='d';
    checkchar(str,ch);
}

void checkchar(char str[],char ch){
    for(int i=0;str[i] != '\0';i++){
        if(str[i]==ch){
            printf("character is present");
            return;
        }
    }
    printf("character is not present");
}