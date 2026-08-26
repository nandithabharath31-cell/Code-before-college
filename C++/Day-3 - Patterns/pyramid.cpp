#include <iostream>
using namespace std;

//    1
//   121
//  12321
// 1234321

// METHOD 1 :
int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    int col = 1;
    for (int i = 1; i <= n; i++)
    {
        int spot = i;
        for (int s = 1; s <= n - i; s++)
        {
            cout << " ";
        }
        for (int j = 1; j <= col; j++)
        {
            if (j <= spot)
            {
                cout << j;
            }
            else
            {
                cout << (--spot);
            }
        }
        cout << endl;
        col = col + 2;
    }

    return 0;
}

// METHOD 2 : 3 loops : MAIN LOOP - for (i=1  ; i<=n ; i+=)
/*                          1] spaces : n-i times
                            2] first half trianle: 1 to i
                            3] second half triangle: i-1 to 1
*/

int main()
{
    int n;
    cout << "Enter a number : ";
    cin >> n;
    for (int i = 1; i <= n; i ++)
    {
        for (int s = 1; s <= n - i; s++)
        {
            cout << " ";
        }

        for (int j = 1; j <= i; j++)
        {
            cout << j;
        }

        for (int j = (i - 1); j >= 1; j--)
        {
            cout << j;
        }
        cout << endl;
    }
    return 0;
}