# include<stdio.h>

int main() {
    int a = 10;
    float b = 5.5;
    double c = 20.0;

    // Implicit type conversion
    double result1 = a + b; // 'a' is converted to float
    printf("Result of a + b: %lf\n", result1);

    // Explicit type conversion (type casting)
    int result2 = (int)c + a; // 'c' is explicitly cast to int
    printf("Result of (int)c + a: %d\n", result2);

    return 0;
}