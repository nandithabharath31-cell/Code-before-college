# include <stdio.h>
# include <string.h>


int count(char word[]);

int main() {
    char word[100];
    puts("enter a word");
    fgets(word , 100 , stdin);
    word[strcspn(word, "\n")] = '\0';
    printf("the length of the word is %d",count(word));
}

int count(char word[]){
    int n=0;
    for (int i=0 ; word[i] != '\0' ; i++){
        printf("%c \n" , word[i]);
        n++;
    }
    return n;
}