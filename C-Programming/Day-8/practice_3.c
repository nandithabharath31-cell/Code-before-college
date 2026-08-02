# include <stdio.h>

// write a func named slice that takes a string and returns a sliced string from from n to m

void slice(char str[] , int n , int m);

int main() {
    char str[100];
    printf("enter a string");
    scanf("%s",str);
    int n=3 , m=6 ;
    slice(str,n,m);
    return 0;

}

void slice(char str[] ,int n , int m){
    char newstr[200];
    int j=0;
    for (int i=n; i<=m ;i++ , j++){
        newstr[j]=str[i];
    }
    newstr[j]='\0';
    puts(newstr);
    printf("slice string is %s" ,newstr);
}

