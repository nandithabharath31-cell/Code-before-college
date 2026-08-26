#include <iostream>
using namespace std;

int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;

    //TOP
    for (int i=1 ; i<=n ; i++){

        for (int s=1 ; s<=n-i ; s++){
            cout << " ";
        }

        cout << "*";

        if(i != 1){
            //spaces
            for(int j=1 ; j<=2*i-1 ; j++){
                cout << " ";;
            }

            cout << "*";
        }
        cout << endl;
    }
    return 0;
}