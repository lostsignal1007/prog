#include <iostream>
using namespace std;

//int task1()
//{
//     int first;
//     short int second;
//     long int third;
//     long long int fr;
//     float fv;
//     double sx;
//     long double sv;
//     bool et;
//     char nn;
//     wchar_t tn;

//     //1
//     int sz = sizeof(second);
//     cout << "size short int: " << sz << " byte" << endl;

//     //2
//     sz = sizeof(first);
//     cout << "size int: " << sz << " byte" << endl;

//     //3
//     sz = sizeof(third);
//     cout << "size long int: " << sz << " byte" << endl;

//     //4
//     sz = sizeof(fr);
//     cout << "size Long Long Int: " << sz << " byte" << endl;

//     //5.	float
//     sz = sizeof(fr);
//     cout << "size float: " << sz << " byte" << endl;

//     //6.	double
//     sz = sizeof(fr);
//     cout << "size double: " << sz << " byte" << endl;

//     //7.	long double
//     sz = sizeof(fr);
//     cout << "size Long double: " << sz << " byte" << endl;

//     //8.	bool
//     sz = sizeof(fr);
//     cout << "size bool: " << sz << " byte" << endl;

//     //9.	char
//     sz = sizeof(fr);
//     cout << "size char: " << sz << " byte" << endl;

//     //10.	wchar_t
//     sz = sizeof(fr);
//     cout << "size wchar_t: " << sz << " byte" << endl;


//     unsigned int ufirst;
//     unsigned short int usecond;
//     unsigned long int uthird;
//     unsigned long long int ufr;
//     //unsigned float ufv; error
//     //unsigned double usx; error
//     //unsigned long double usv; error
//     //unsigned bool uet; error
//     unsigned char unn;
//     //unsigned wchar_t utn; error

//     //1 unsigned
//     sz = sizeof(usecond);
//     cout << "size short int: " << sz << " byte" << endl;

//     //2
//     sz = sizeof(ufirst);
//     cout << "size int: " << sz << " byte" << endl;

//     //3
//     sz = sizeof(uthird);
//     cout << "size long int: " << sz << " byte" << endl;

//     //4
//     sz = sizeof(ufr);
//     cout << "size Long Long Int: " << sz << " byte" << endl;

//     //9.	char
//     sz = sizeof(unn);
//     cout << "size char: " << sz << " byte" << endl;

//     return 0;
// }

int main() //task2
{
    float f = -1.1;
    cout << "float: " << f << endl;
    int i;
    i = int(f);
    cout << "float to int: " <<  i << endl;
    
    cout << " " << endl;
    
    double d = -1.1;
    cout << "double: " << d << endl;
    int i2;
    i2 = int(f);
    cout << "double to int: " <<  i2 << endl;

    cout << " " << endl;

    bool b = true;
    cout << "bool: " << b << endl;
    int i3;
    i3= int(b);
    cout<<"bool -> int: "<<i3<<endl;

    cout << " " << endl;

    int i4 = 0;
    cout << "int: " << i4 << endl;
    bool b2;
    b2= bool(i4);
    cout<<"int->bool: "<<b2<<endl;

    cout << " " << endl;


    return 0;
}