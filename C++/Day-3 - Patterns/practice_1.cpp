#include <iostream>
using namespace std;

// 1111
// 2222
// 3333
// 4444

int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= n; j++)
        {
            cout << i;
        }
        cout << endl;
    }
}