# include <stdio.h>

// to take the two nums from sum.txt and overwrite their sum in the same file

int main() {
    FILE *fptr;
    fptr = fopen("sum.txt","r");

    int a,b;
    fscanf(fptr,"%d",&a);
    fscanf(fptr,"%d",&b);
    fclose(fptr);

    fptr = fopen("sum.txt","w");

    int sum = a+b;
    fprintf(fptr,"%d",sum);
    fclose(fptr);

    return 0;
}