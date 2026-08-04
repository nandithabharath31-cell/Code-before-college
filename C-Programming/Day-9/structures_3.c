#include <stdio.h>

struct student {
    char rollno[20];
    char name[50];
    int marks;
};

void average(struct student s[]); //always define the function (having structure passed ) after defining the structur

int main() {

    struct student s[3] = {
        {"cs101", "Nanditha", 91},
        {"cs102", "Bharath", 90},
        {"cs103", "Anjali", 78}
    };

    // print all data in one line per student
    for (int i = 0; i < 3; i++) {
        printf("%s %s %d\n", s[i].rollno, s[i].name, s[i].marks);
    }

    //accessing only one of the data 
    printf("Bharath scored : %d \n" , s[1].marks);

    //using pointers in stuctures
    //don't declare struct student s[1] here again
    struct student *ptr;
    ptr = &s[1];
    printf("the roll no. of Bharath : %s \n" , ((*ptr).rollno));

    // using arrow operator
    //don't define struct student *ptr; again
    ptr = &s[0];
    printf("Nanditha scored : %d \n" , ptr -> marks);

    // call average for all students
    average(s);
    
    return 0;
}
 //passing structure to the function
void average(struct student s[]) {
        int avg=(s[0].marks+s[1].marks+s[2].marks)/3;
        printf("the average marks scored : %d" , avg);
    }