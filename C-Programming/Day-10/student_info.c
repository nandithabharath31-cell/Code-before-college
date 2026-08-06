# include <stdio.h>

int main(){
    FILE *fptr;
    fptr = fopen("student.txt" , "w");
    char name[30];
    char dept[30];
    float marks;
    printf("enter student name");
    scanf("%s" , name);
    printf("enter course");
    scanf("%s", dept);
    printf("enter cgpa");
    scanf("%f",&marks);

    fprintf(fptr , " NAME OF THE STUDENT : %s \n" , name);
    fprintf(fptr , " COURSE : %s \n" , dept);
    fprintf(fptr , " CGPA : %f \n" , marks);

    fclose(fptr);

    return 0;


}

