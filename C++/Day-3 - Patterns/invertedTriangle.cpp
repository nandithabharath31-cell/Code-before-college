#include <iostream>
using namespace std;

// 1 2 3 4 
// 1 2 3 
// 1 2 
// 1 

int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    for (int i = n; i >= 1; i--)
    {
        for (int j=1; j<=i ; j++)
        {
            cout << j << " ";
        }
        cout << endl;
    }
    return 0;
}
