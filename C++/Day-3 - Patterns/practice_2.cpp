#include <iostream>
using namespace std;

// A B C D 
// E F G H 
// I J K L 
// M N O P 

int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    char ch = 'A';
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= n;j++)
        {
            cout << ch << " ";
            ch++;
        }
        cout << endl;
    }
}