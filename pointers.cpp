#include<iostream>
#include<vector>
using namespace std;

int main(){
    vector<int> n = {1,2,3};
    cout << *(n.begin()) << endl; // prints the first element
    cout << *(n.end() - 1) << endl; // prints the last element
    cout << &*n.begin() << endl; // prints the address of the first element
    cout << &*(n.end() - 1) << endl; // prints the address of the last element
    cout << n.back() << endl; // prints the last element
    cout << *&n.back() << endl; // prints the last element
    vector<int> next(n.begin() + 1, n.end());
    cout<<n[0]<<endl<<n[1];
}