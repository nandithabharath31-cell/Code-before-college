#include <stdio.h>

#define MAX_CUSTOMERS 100

typedef struct customer_details
{
    int accountnumber;
    char name[50];
    int pin;
    float balance;
} user;

int totalcustomers = 0;
user accounts[MAX_CUSTOMERS];
int current_user = -1; // shows no user logged in currently

int displayMenu();

void createAccount();
int login();
void searchAccount();

void bankingMenu(int index);

void deposit(int index);
void withdraw(int index);
void checkBalance(int index);

int main()
{
    int choice;

    while (1)
    {
        choice = displayMenu();

        switch (choice)
        {
        case 1:
            createAccount();
            break;
        case 2:
            current_user = login();

            if (current_user != -1)
            {
                bankingMenu(current_user);
            }
            break;
        case 3:
            searchAccount();
            break;
        case 4:
            return 0;
        default:
            printf("INVALID CHOICE .... try again !");
        }
    }
}

int displayMenu()
{
    printf("\n ================================ \n");
    printf("         MINI BANKING SYSTEM \n");
    printf(" ================================ \n");

    printf("      1. Create Account \n");
    printf("      2. Login \n");
    printf("      3. Account Details \n");
    printf("      4. Exit \n");

    printf("Enter choice : ");
    int choice;
    scanf("%d", &choice);

    return choice;
}

void createAccount()
{
    printf("\n-----------CREATE ACCOUNT-------------\n");
    if (totalcustomers >= MAX_CUSTOMERS)
    {
        printf("Bank storage full.\n");
        return;
    }
    while (1)
    {

        printf("Enter account number : ");
        scanf("%d", &accounts[totalcustomers].accountnumber);

        //--------------checking for duplication---------------
        int found = 0;
        for (int i = 0; i < totalcustomers; i++)
        {
            if (accounts[totalcustomers].accountnumber == accounts[i].accountnumber)
            {
                printf("!! ACCOUNT NUMBER ALREADY EXISTS !! \n");
                found = 1;
                break;
            }
        }
        if (found == 0)
        {
            break;
        }
    }

    printf("Enter user Name : ");
    getchar(); // take \n character
    fgets(accounts[totalcustomers].name, 50, stdin);
    printf("Create PIN : ");
    scanf("%d", &accounts[totalcustomers].pin);
    printf("Enter initial balance : ");
    scanf("%f", &accounts[totalcustomers].balance);

    printf("\n~~~~~~~~~~~~~~~~~~~~~~~\n");
    printf("    ACCOUNT CREATED \n");
    printf("~~~~~~~~~~~~~~~~~~~~~~~\n");

    printf(" Account Number : %d \n", accounts[totalcustomers].accountnumber);
    printf(" Customer Name : %s ", accounts[totalcustomers].name);
    printf("Balance : %.2f \n", accounts[totalcustomers].balance);

    totalcustomers++;
}

int login()
{
    printf("\n-------------------------------------------\n");
    printf("                LOGIN");
    printf("\n-------------------------------------------\n");

    int accnum;
    int pin;
    printf("Enter Account Number : ");
    scanf("%d", &accnum);
    for (int i = 0; i < totalcustomers; i++)
    {
        if (accnum == accounts[i].accountnumber)
        {
            printf("Enter PIN : ");
            scanf("%d", &pin);
            if (pin == accounts[i].pin)
            {
                printf("LOGIN SUCCESSFUL ! \n");
                printf("WELCOME %s", accounts[i].name);
                return i;
            }
            else
            {
                printf("INCORRECT PIN");
                return -1;
            }
        }
    }
    printf("ACCOUNT NOT FOUND \n");
    return -1;
}

void searchAccount()
{
    printf("\n ---------------ACCOUNT DETAILS---------------------- \n");
    int accnum;
    int found = 0;
    printf("Enter your account number : ");
    scanf("%d", &accnum);
    for (int i = 0; i < totalcustomers; i++)
    {
        if (accnum == accounts[i].accountnumber)
        {
            printf(" \n Account Number : %d \n", accounts[i].accountnumber);
            printf(" Customer Name : %s", accounts[i].name);
            printf(" Balance : %.2f \n", accounts[i].balance);
            found = 1;
            break;
        }
    }
    if (found == 0)
    {
        printf("ACCOUNT NOT FOUND \n");
    }
}

void bankingMenu(int index)
{
}
