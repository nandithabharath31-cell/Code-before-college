# include <stdio.h>
# include <string.h>

struct student {
    char name[100];
    int roll;
    float cgpa;
};

int main() {
    struct student CSE[100];
    struct student ECE[100];
    struct student IT[100];

    strcpy(CSE[0].name , "nanditha");
    CSE[0].roll = 101;
    CSE[0].cgpa = 9.8;

    strcpy(CSE[1].name , "sneha");
    CSE[1].roll = 102;
    CSE[1].cgpa = 9.1;

    strcpy(ECE[0].name , "deeksha");
    ECE[0].roll = 103;
    ECE[0].cgpa = 9.8;

    strcpy(ECE[1].name , "disha");
    ECE[1].roll = 104;
    ECE[1].cgpa = 9.0;

    strcpy(IT[0].name , "sima");
    IT[0].roll = 105;
    IT[0].cgpa = 9.2;

    for (int i = 0; CSE[i].roll != 0; i++) {
        printf("%s   |     %d    |   %f    |  CSE \n", CSE[i].name, CSE[i].roll, CSE[i].cgpa);
    }

        for (int i = 0; ECE[i].roll != 0; i++) {
        printf("%s   |     %d    |   %f    |  ECE \n", ECE[i].name, ECE[i].roll, ECE[i].cgpa);
    }

        for (int i = 0; IT[i].roll != 0; i++) {
        printf("%s   |     %d    |   %f    |  IT \n", IT[i].name, IT[i].roll, IT[i].cgpa);
    }
    return 0;


}