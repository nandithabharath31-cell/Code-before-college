# include <stdio.h>

// to print the real and imgno. usinf arrow(pointer)

struct complex {
    int real;
    int img;
};

int main() {
    struct complex num1 = {5,10};
    struct complex *ptr = &num1;
    printf("real part : %d \n" , ptr -> real);
    printf("img part : %d" , ptr -> img);

    return 0;
}