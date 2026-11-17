// function description
#include "funcs.h"
#include <cmath>
#include <iostream>
using namespace std;



// average
double average(int n, const int arr[])
{
    if (n<=0) return 0.0;
    long long sum = 0;
    for (int i=0; i<n; ++i)
    {
        sum+=arr[i];
    }
    return static_cast<double>(sum)/n;
}



//sigma
double sigma(int n, const double arr[])
{
    if (n<=0) return 0.0;

    // среднее арифметическое (mean)
    double sum = 0.0;
    for (int i=0; i<n; ++i)
    {
        sum+=arr[i];
    }
    double mean = sum / n;

    // сумма квадратов разностей (sq_sum)
    double sq_sum = 0.0;
    for(int i=0; i<n; ++i)
    {
        sq_sum += (arr[i]-mean)*(arr[i]-mean);
    }

    return sqrt(sq_sum/n);
}



//density
double get_density(double h)
    {
        //arrays given (14 dots)
        const int SIZE = 14;
        const double heights[SIZE]={0,500,1000,1500,2000,2500,3000,4000,5000,6000,7000,8000,9000,10000};
        const double densities[SIZE]={1.2250, 1.1673, 1.1117, 1.0581, 1.0065, 0.9569, 0.9093, 0.8194, 0.7365, 0.6601, 0.5900, 0.5258, 0.4671, 0.4135};

        // checking boarders of the table
        if (h <= heights[0]) return densities[0];
        if (h >= heights[SIZE - 1]) return densities[SIZE - 1];

        // finding interpolation interval
        for (int i = 0; i < SIZE - 1; ++i) {
            if (h >= heights[i] && h <= heights[i + 1]) {
                //linear interpolation:
                // y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                double x1 = heights[i];
                double x2 = heights[i + 1];
                double y1 = densities[i];
                double y2 = densities[i + 1];
                
                return y1 + (h - x1) * (y2 - y1) / (x2 - x1);
            }
        }
        return 0.0;
    }



// fibonacci
void fibonacci(int num, int nBegin) {
    if (num <= 0 || nBegin <= 0) {
        cout << "number of integers and the beginners number must be >0.\n";
        return;
    }

    // Вычисляем максимальный порядковый номер числа Фибоначчи, который нам понадобится
    int max_needed = nBegin + num - 1;

    long long f1 = 1;
    long long f2 = 1;

    cout << "fibonacci numbers: ";
    
    for (int i = 1; i <= max_needed; ++i) {
        long long current;
        if (i == 1 || i == 2) {
            current = 1;
        } else {
            current = f1 + f2;
            f1 = f2;
            f2 = current;
        }

        // Если текущий номер числа попал в запрашиваемый диапазон, выводим его
        if (i >= nBegin) {
            cout << current << " ";
        }
    }
    cout << "\n";
}