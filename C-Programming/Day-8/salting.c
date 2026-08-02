# include <stdio.h>
# include <string.h>

// finding the salted form of the password entered by user if the salt is "123" and added at the end
// salting - add a set of text(salt) to protect the original password from being hacked

void salting(char password[]);;

int main() {
    char password[100];
    scanf("%s",password);
    salting(password);
    return 0;
}

void salting(char password[]){
    char salt[] = "123";
    char newpass[200];
    strcpy(newpass,password);
    strcat(newpass,salt);
    puts(newpass);
}