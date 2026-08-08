# include <stdio.h>

int main () {
    
float num1, num2, result;
char opp;

printf("Enter first number: ");
scanf("%f", &num1);

printf("Enter operator (+, -, *, /): ");
scanf(" %c", &opp);   // note: space before %c to skip leftover newline

printf("Enter second number: ");
scanf("%f", &num2);

switch (opp) {
    case '+': result = num1 + num2; printf("%f", result); break;
    case '-': result = num1 - num2; printf("%f", result); break;
    case '*': result = num1 * num2; printf("%f", result); break;
    case '/': 
        if (num2 != 0) { result = num1 / num2; printf("%f", result); }
        else printf("Error: division by zero\n");
        break;
    default: printf("Invalid operator\n");
}  
}

