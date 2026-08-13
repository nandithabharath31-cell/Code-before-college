#include <stdio.h>
#include <string.h>

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
void transfer(int index);
void changePassword(int index);

void saveData();
void loadData();

int main()
{
    int choice;
    loadData();

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
            saveData();
            printf("\nThank you for using Mini Banking System! \n");
            return 0;
        default:
            printf("INVALID CHOICE .... try again !");
        }
    }
}

void saveData()
{
    FILE *fptr;
    fptr = fopen("../data/accounts.dat", "wb");
    if (fptr == NULL)
    {
        printf("Error opening file.\n");
        return;
    }
    fwrite(&totalcustomers, sizeof(int), 1, fptr);
    fwrite(accounts, sizeof(user), totalcustomers, fptr);
    fclose(fptr);
}

void loadData()
{
    FILE *fptr;

    fptr = fopen("../data/accounts.dat", "rb");

    if (fptr == NULL)
    {
        return;
    }

    fread(&totalcustomers, sizeof(int), 1, fptr);
    if (totalcustomers < 0 || totalcustomers > MAX_CUSTOMERS)
    {
        printf("Invalid data file.\n");
        totalcustomers = 0;
        fclose(fptr);
        return;
    }

    fread(accounts, sizeof(user), totalcustomers, fptr);

    fclose(fptr);
}

int displayMenu()
{
    printf("\n ================================ \n");
    printf("        MINI BANKING SYSTEM \n");
    printf(" ================================ \n");

    printf("      1. Create Account \n");
    printf("      2. Login \n");
    printf("      3. Search Account \n");
    printf("      4. Exit \n");

    // printf("Enter choice : ");
    int choice;
    // scanf("%d", &choice);
    printf("Enter choice : ");

    if (scanf("%d", &choice) != 1)
    {
        while (getchar() != '\n')
            ;
        return -1;
    }

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
    accounts[totalcustomers].name[strcspn(accounts[totalcustomers].name, "\n")] = '\0'; // to avoid \n

    do
    {
        printf("Create PIN : ");
        scanf("%d", &accounts[totalcustomers].pin);
        if (accounts[totalcustomers].pin < 1000 ||
            accounts[totalcustomers].pin > 9999)
        {
            printf("PIN must contain exactly 4 digits.\n");
        }
    } while (accounts[totalcustomers].pin < 1000 ||
             accounts[totalcustomers].pin > 9999);

    do
    {
        printf("Enter initial balance : ");
        scanf("%f", &accounts[totalcustomers].balance);
        if (accounts[totalcustomers].balance < 0)
        {
            printf("Balance cannot be negative.\n");
        }

    } while (accounts[totalcustomers].balance < 0);

    printf("\n~~~~~~~~~~~~~~~~~~~~~~~\n");
    printf("    ACCOUNT CREATED \n");
    printf("~~~~~~~~~~~~~~~~~~~~~~~\n");

    printf(" Account Number : %d \n", accounts[totalcustomers].accountnumber);
    printf(" Customer Name : %s \n", accounts[totalcustomers].name);
    printf("Balance : %.2f \n", accounts[totalcustomers].balance);
    printf("Please remember your account number and PIN.\n");

    totalcustomers++;
    saveData();
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
            printf(" Customer Name : %s\n", accounts[i].name);
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
    while (1)
    {
        printf("\n================================\n");
        printf("      BANKING DASHBOARD   \n");
        printf("  Logged in as : %s \n", accounts[index].name);
        printf("================================\n");
        printf("\n");

        printf("   1. Deposit \n");
        printf("   2. Withdraw \n");
        printf("   3. Balance \n");
        printf("   4. Transfer \n");
        printf("   5. Change Password \n");
        printf("   6. Logout \n");
        printf("\n");
        int choice;
        printf("Enter Choice :");
        if (scanf("%d", &choice) != 1)
        {
            while (getchar() != '\n')
                ;
            printf("Invalid input. Please enter a number.\n");
            continue;
        }

        switch (choice)
        {
        case 1:
            deposit(index);
            break;
        case 2:
            withdraw(index);
            break;
        case 3:
            checkBalance(index);
            break;
        case 4:
            transfer(index);
            break;
        case 5:
            changePassword(index);
            break;
        case 6:
            current_user = -1;
            printf("Logged out successfully ! \n");
            return;
        default:
            printf("INVALID CHOICE ....try again !! \n");
        }
    }
}

void deposit(int index)
{
    printf("\n-------------------------------------------\n");
    printf("                DEPOSIT");
    printf("\n-------------------------------------------\n");
    printf("Current Balance : %.2f \n", accounts[index].balance);
    float depositamt;
    printf("Enter amount to deposit : ");
    scanf("%f", &depositamt);
    if (depositamt > 0)
    {
        accounts[index].balance += depositamt;
        saveData();
        printf("Deposit Successful ! \n");
        printf("\n");
        printf("Amount Deposited : %.2f\n", depositamt);
        printf("Updated Balance : %.2f\n", accounts[index].balance);
    }
    else
    {
        printf("Invalid Amount\n");
    }
}

void withdraw(int index)
{
    printf("\n-------------------------------------------\n");
    printf("                WITHDRAW");
    printf("\n-------------------------------------------\n");
    printf("Current Balance : %.2f \n", accounts[index].balance);
    float withdrawamt;
    printf("Enter amount to withdraw : ");
    scanf("%f", &withdrawamt);
    if (withdrawamt > 0 && withdrawamt <= accounts[index].balance)
    {
        accounts[index].balance -= withdrawamt;
        saveData();
        printf("Withdrawal Successful ! \n");
        printf("\n");
        printf("Remaining Balance : %.2f\n", accounts[index].balance);
    }
    else if (withdrawamt <= 0)
    {
        printf("Invalid Amount\n");
    }
    else if (withdrawamt > accounts[index].balance)
    {
        printf("Insufficient Funds\n");
    }
}

void checkBalance(int index)
{
    printf("\n-------------------------------------------\n");
    printf("                ACCOUNT SUMMARY");
    printf("\n-------------------------------------------\n");
    printf(" \n Account Number : %d \n", accounts[index].accountnumber);
    printf(" Customer Name : %s\n", accounts[index].name);
    printf(" Current Available Balance : %.2f \n", accounts[index].balance);
}

void transfer(int index)
{
    printf("\n-------------------------------------------\n");
    printf("                TRANSFER");
    printf("\n-------------------------------------------\n");
    int receiver_account;
    float amount;
    printf("Enter Receiver Account Number : ");
    scanf("%d", &receiver_account);
    if (receiver_account == accounts[index].accountnumber)
    {
        printf("You cannot transfer to your own account.\n");
        return;
    }
    for (int i = 0; i < totalcustomers; i++)
    {
        if (receiver_account == accounts[i].accountnumber)
        {
            printf("Enter Amount to Transfer : ");
            scanf("%f", &amount);
            if (amount > 0 && amount <= accounts[index].balance)
            {
                accounts[index].balance -= amount;
                accounts[i].balance += amount;
                saveData();

                printf("Transfer Successful !\n");
                printf("Receiver Account : %d \n", receiver_account);
                printf("Receiver Name : %s\n", accounts[i].name);
                printf("Transferred : %.2f \n", amount);
                printf("Available Balance : %.2f\n", accounts[index].balance);
                return;
            }
            else if (amount > accounts[index].balance)
            {
                printf("Insufficient Funds\n");
                return;
            }
            else if (amount <= 0)
            {
                printf("Invalid Amount\n");
                return;
            }
        }
    }
    printf("ACCOUNT NOT FOUND \n");
}

void changePassword(int index)
{
    printf("Enter Current PIN : ");
    int pin;
    scanf("%d", &pin);
    if (pin == accounts[index].pin)
    {
        printf("Enter New PIN : ");
        int NewPIN;
        scanf("%d", &NewPIN);
        printf("Confirm New PIN : ");
        int confpin;
        scanf("%d", &confpin);
        if (confpin == NewPIN)
        {
            accounts[index].pin = NewPIN;
            saveData();
            printf("\n Password Updated Successfully! \n");
            return;
        }
        else
        {
            printf("\n Mismatch Error \n");
            return;
        }
    }
    else
    {
        printf("Wrong PIN entered\n");
    }
}
