# include <stdio.h>
# include <string.h>

struct student {
    char name[100];
    int roll;
    float cgpa;
};

int main() {
    struct student s1;
    strcpy(s1.name,"nanditha");
    s1.roll=101;
    s1.cgpa=9.8;

    printf("student name : %s \n" , s1.name);
    printf("student rollno. :%d \n" , s1.roll);
    printf("student cgpa : %f \n" , s1.cgpa);

    struct student s2;
    strcpy(s2.name,"nisha");
    s2.roll=102;
    s2.cgpa=9.7;

    printf("student name : %s \n" , s2.name);
    printf("student rollno. :%d \n" , s2.roll);
    printf("student cgpa : %f \n" , s2.cgpa);

    struct student s3;
    strcpy(s3.name,"neha");
    s1.roll=103;
    s1.cgpa=9.6;

    printf("student name : %s \n" , s3.name);
    printf("student rollno. :%d \n" , s3.roll);
    printf("student cgpa : %f \n" , s3.cgpa);

    return 0;

}