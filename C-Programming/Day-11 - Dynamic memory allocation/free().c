# include <stdio.h>
# include <stdlib.h>


int main() {
    int *ptr;
    int n;
    printf("enter the size");
    scanf("%d" , &n);

    ptr = (int *) calloc(n , sizeof(int));

    for (int i=0 ; i<n ; i++){         // initializes o value to all 
        printf("%d \n" , ptr[i]);
    }

    free (ptr);  // frees the memory allocated to ptr so that we can allocate it newly again

    printf("-------------- \n");

    ptr = (int *) calloc(3 , sizeof(int));

    for (int i=0 ; i<3 ; i++){         // initializes o value to all 
        printf("%d \n" , ptr[i]);
    }

    return 0;
}