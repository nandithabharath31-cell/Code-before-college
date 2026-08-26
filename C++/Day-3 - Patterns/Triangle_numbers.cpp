#include <iostream>
using namespace std;

    // A 
    // B B 
    // C C C 
    // D D D D 

int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    char ch='A';
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= i; j++)
        {
            cout << ch << " ";
    
        }
        ch++;
        cout << endl;
    }
}