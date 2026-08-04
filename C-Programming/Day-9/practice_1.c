# include <stdio.h>

// enter the address(house no , block , city ,state) of 5 ppl

typedef struct address {
    int housenum;
    char block[10];
    char city[30];
    char state[30];
}add;                  //aliasing - typedef keyword

void printadd(add a1);

int main() {
    add a1[5];
    //input
    printf("enter input of person 1 :");
    scanf("%d" , &a1[0].housenum);       // only int value needs & in scnaf
    scanf("%s",a1[0].block);
    scanf("%s",a1[0].city);
    scanf("%s",a1[0].state);

    printf("enter input of person 2 :");
    scanf("%d" , &a1[1].housenum);    
    scanf("%s",a1[1].block);     
    scanf("%s",a1[1].city);
    scanf("%s",a1[1].state);

    printf("enter input of person 3 :");
    scanf("%d" , &a1[2].housenum); 
    scanf("%s",a1[2].block);       
    scanf("%s",a1[2].city);
    scanf("%s",a1[2].state);

    printf("enter input of person 4 :");
    scanf("%d" , &a1[3].housenum); 
    scanf("%s",a1[3].block);        
    scanf("%s",a1[3].city);
    scanf("%s",a1[3].state);

    printf("enter input of person 5 :");
    scanf("%d" , &a1[4].housenum); 
    scanf("%s",a1[4].block);      
    scanf("%s",a1[4].city);
    scanf("%s",a1[4].state);

    printadd(a1[0]);
    printadd(a1[1]);
    printadd(a1[2]);
    printadd(a1[3]);
    printadd(a1[4]);

    return 0;

}

void printadd(add a1){
    printf("address : %d , %s ,%s ,%s \n" , a1.housenum , a1.block , a1.city, a1.state);
}