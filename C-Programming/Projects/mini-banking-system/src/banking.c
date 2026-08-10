#include <stdio.h>

#define MAX_CUSTOMERS 100

typedef struct customer_details
{
    int accountnumber;
    char name[50];
    int pin;
    float balance;
} user;

int main()
{
    int totalcustomers = 0;
    int current_user = -1;  //shows no user logged in currently
    user accounts[MAX_CUSTOMERS];
    //-------------------------MENU--------------------------------------
    while (1)
    {
        printf("\n ================================ \n");
        printf("         MINI BANKING SYSTEM \n");
        printf(" ================================ \n");

        printf("      1. Create Account \n");
        printf("      2. Login \n");
        printf("      3. Account Details \n");
        printf("      4. Exit \n");

        printf("Enter choice : ");
        int ch;
        scanf("%d", &ch);
        if (ch != 1 && ch != 2 && ch != 3 && ch != 4)
        {
            printf("INVALID ENTRY , Try again ! ");
        }

        //--------------------CREATE ACCOUNT------------------------
        if (ch == 1)
        {
            printf("\n-----------CREATE ACCOUNT-------------\n");
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

        //-------------------------LOGIN----------------------------------------
        else if (ch == 2)
        {
            printf("\n-------------------------------------------\n");
            printf("                LOGIN");
            printf("\n-------------------------------------------\n");

            int accnum;
            int pin;
            printf("Enter Account Number : ");
            scanf("%d", &accnum);
            int found = 0;
            for (int i = 0; i < totalcustomers; i++)
            {
                if (accnum == accounts[i].accountnumber)
                {
                    current_user = i;
                    printf("Enter PIN : ");
                    scanf("%d", &pin);
                    if (pin == accounts[current_user].pin)
                    {
                        printf("LOGIN SUCCESSFUL ! \n");
                        printf("WELCOME %s", accounts[current_user].name);
                        found = 1;
                        break;
                    }
                    else
                    {
                        printf("INCORRECT PIN");
                        found = 1;
                        break;
                    }
                }
            }
            if (found == 0)
            {
                printf("ACCOUNT NOT FOUND");
            }
        }

        //-------------------------ACCOUNT LOOKUP--------------------------------
        else if (ch == 3)
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
                printf("ACCOUNT NOT FOUND");
            }
        }
        //----------------------EXIT-----------------------------------
        else if (ch == 4)
        {
            break;
        }
    }

    return 0;
}