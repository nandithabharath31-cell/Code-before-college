# include<iostream>
using namespace std;

int main() {

    // implicit type casting
    char grade='A';
    int value=grade;
    cout << value << endl;

    // explicit type casting
    float num=100.55678;
    int rounded=(int)num;
    cout << "rounded value of " << num << " is " << rounded << endl ;

    return 0;
}
