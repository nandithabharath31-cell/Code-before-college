#include <iostream>
using namespace std;

// square pattern in numbers
// 1 2 3 
// 4 5 6 
// 7 8 9 
int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    int num=1;
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= n; j++)
        {
            cout << num << " ";
            num++;
    
        }
        cout << endl;
    }
}