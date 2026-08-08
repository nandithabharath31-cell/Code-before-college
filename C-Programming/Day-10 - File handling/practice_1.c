# include <stdio.h>

// if file doesnot exist NULL value is store in fptr

int main() {
    FILE *fptr;
    fptr = fopen ("text.txt" , "r");

    if (fptr == NULL){
        printf("file doesnot exist");
    }
    else{
        printf("file exist");
    }
    return 0;
}

