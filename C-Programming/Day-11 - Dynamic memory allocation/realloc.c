// allocate memory to store first 5 ODD no.s then reallocate it to store first 6 EVEn no.s

# include <stdio.h>
# include <stdlib.h>


int main() {
    int *ptr;
    ptr = (int *) calloc(5 , sizeof(int));
    
    ptr[0]=1;
    ptr[1]=3;
    ptr[2]=5;
    ptr[3]=7;
    ptr[4]=9;

    for (int i=0 ; i<5 ; i++){
        printf("%d \n" , ptr[i]);
    }

    ptr = realloc(ptr , 6);

    printf("---------------- \n");
    
    ptr[0]=0;
    ptr[1]=2;
    ptr[2]=4;
    ptr[3]=6;
    ptr[4]=8;
    ptr[5]=10;

    for (int i=0 ; i<6 ; i++){
        printf("%d \n" , ptr[i]);
    }

    free(ptr);
    
    return 0; 
    

}

