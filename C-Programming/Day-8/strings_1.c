# include <stdio.h>

void printstring(char arr[]);

int main() {
    char firstname[] = "Nanditha";
    char lastname[] = "Bharath";

    printstring(firstname);
    printstring(lastname);

    //printing using format specifier 
    printf("%s", firstname);

    // input of a string
    char place[50];
    printf("enter place of birth");
    scanf(" %s" , place);
    printf("your birth place is %s\n" , place);

    return 0;
}

// printing strings charater by character
void printstring(char arr[]) {
    for (int i=0 ; arr[i] != '\0' ; i++) {
        printf("%c" , arr[i]);
    }
    printf("\n");
}

