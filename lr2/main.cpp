#include "funcs.h"
#include <clocale>
#include <iostream>
using namespace std;


int main()
{
    int choice;
    cout << "prepare to choose the function\n";
    cout << "1 - calculate average of intehers\n";
    cout << "2 - calculate standard deviation (sigma) of floats\n";
    cout << "3 - calculate atmosphere density\n";
    cout << "4 - calculate fibonacci numbers\n";
    cout << "type your choice: ";
    cin >> choice;

    int n;
    switch(choice)
    {
        case 1: 
        {
            cout << "enter the number of integers: ";
            cin >> n;
            if (n<=0)
            {
                cout << "error, n must be >0\n";
                break;
            }

            // dinamic array for integers
            int* int_arr = new int[n];
            cout << "enter " << n << " integers divided by space:\n";
            for (int i=0; i<n; ++i)
            {
                cin >> int_arr[i];
            }

            double avg_res = average(n, int_arr);
            cout << "aripmetic average: "<<avg_res<<endl;

            delete[] int_arr; 
            break;        
        }

        case 2:
        {
            cout << "enter the number of floats: ";
            cin >> n;
            if (n<=0)
            {
                cout <<"error: number should be >0\n";
                break;
            }

            // dinamic array for floats
            double* d_arr = new double[n];
            cout << "enter " << n << " floats divided by space:\n";
            for (int i=0; i<n; ++i)
            {
                cin >> d_arr[i];
            }

            double sig_res = sigma(n, d_arr);
            cout << "standard deviation: "<<sig_res<<endl;

            delete[] d_arr; 
            break;
        }

        case 3: {
            double h;
            cout << "enter the hight (in meters, 0-10000): ";
            cin >> h;

            if (h < 0 || h > 10000) {
                cout << "attention: height outside the table (0-10000 m).\n";
            }

            double density_res = get_density(h);
            cout << "atmosphere density at height " << h << " m: " << density_res << " kg/m^3\n";
            break;
        }

        case 4: {
            int num, nBegin;
            cout << "enter the number of integers (num): ";
            cin >> num;
            cout << "enter the number of integer, that begins the output (nBegin): ";
            cin >> nBegin;

            fibonacci(num, nBegin);
            break;
        }

        default:
        {
            cout<<"error: incorrect choice :<"<<endl;
            break;
        }
    }
    return 0;
}