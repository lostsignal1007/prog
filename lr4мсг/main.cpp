#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

std::ofstream fs;

typedef double (*Function)(vector<double>);

// =================================================================
// MATHEMATICAL OPERATORS FOR VECTOR OPERATIONS
// =================================================================
template <typename T>
T innerProd(const std::vector<T> &lhs, const std::vector<T> &rhs){
   T result = 0;
   auto rhs_it = rhs.cbegin();
   for (auto& i : lhs){
       result += i * *(rhs_it++);
   }
   return result;
}

template <typename T>
std::vector<T> operator *(const std::vector<T> &lhs, const T& rhs){
   std::vector<T> result;
   result.resize(lhs.size());
   std::copy(lhs.cbegin(), lhs.cend(), result.begin());
   for (auto &t : result)
       t *= rhs;
   return result;
}

template <typename T>
std::vector<T> operator +(const std::vector<T> &lhs, const std::vector<T> &rhs) {
   std::vector<T> result;
   if (lhs.size() != rhs.size())
       return result;
   result.resize(lhs.size());
   auto lhs_it = lhs.cbegin(), rhs_it = rhs.cbegin();
   std::for_each(result.begin(), result.end(), [&lhs_it, &rhs_it](T &t)->void{
       t = (*(lhs_it++)) + (*(rhs_it++));
   });
   return result;
}

template <typename T>
std::vector<T> operator -(const std::vector<T> &v) {
   std::vector<T> result;
   result.resize(v.size());
   auto v_it = v.cbegin();
   std::for_each(result.begin(), result.end(), [&v_it](T &t)->void{
       t = -(*(v_it++));
   });
   return result;
}

// =================================================================
// TARGET FUNCTIONS FROM ASSIGNMENT (VARIANT 3)
// =================================================================

double F_variant_A(vector<double> x) {
    double term1 = (x[0] - 5.0) * (x[0] - 5.0);
    double term2 = (x[1] - 4.0) * (x[1] - 4.0);
    double term3 = (x[0] - 15.0) * (x[0] - 15.0);
    double term4 = (x[1] - 4.0) * (x[1] - 4.0);
    return (term1 * term2) + term3 + term4;
}

double F_variant_B(vector<double> x) {
    double term1 = (x[0] - 5.0) * (x[0] - 5.0);
    double term2 = (x[1] - 4.0) * (x[1] - 4.0);
    double denominator = (term1 * term2) + 10.0 * term1 + 50.0 * term2 + 1.0;
    return -1.0 / denominator;
}

Function current_F = F_variant_A;

vector<double> GradF1(Function F, vector<double> x){
   vector<double> dv(x.size()), res(x.size());
   const double dx = 1e-9;
   for (int i = 0; i < int(x.size()); i++){
       dv[i] = dx;
       res[i] = (F(x + dv) - F(x)) / dx;
       dv[i] = 0;
   }
   return res;
}

// =================================================================
// STABLE OPTIMIZATION METHODS
// =================================================================

double FindMin(Function F, vector<double> s, vector<double> p, double eps) {
    double a = 0.0;
    double b = 0.1; 
    
    double f_start = F(s);
    double step = 0.01;
    
    for (int i = 0; i < 100; ++i) {
        vector<double> current_point = s + p * b;
        
        if (std::abs(current_point[0]) > 1e4 || std::abs(current_point[1]) > 1e4) {
            break; 
        }
        
        if (F(current_point) > f_start) {
            break;
        }
        a = b;
        b += step;
        step *= 2.0; 
    }

    if (a >= b || b > 10.0) {
        a = 0.0;
        b = 0.5; 
    }

    double d;
    do {
        d = b - a;
        if (F(s + (p * (a + d / 4.0))) < F(s + (p * (a + d / 2.0)))) {
            b = a + d / 2.0;
        }
        else if (F(s + (p * (a + 3.0 * d / 4.0))) < F(s + (p * (a + d / 2.0)))) {
            a = a + d / 2.0;
        }
        else {
            a = a + d / 4.0;
            b = b - d / 4.0;
        }
    } while (std::abs(a - b) >= eps);

    return (a + b) / 2.0;
}

void PrintSolution(vector<double> x, double val, int numIter){
  std::cout << "\n==========================================" << std::endl;
  std::cout << "CALCULATION RESULTS:" << std::endl;
  std::cout << "Number of iterations: " << numIter << std::endl;
  std::cout << "Computed minimum coordinates: X0 = " << x[0] << ", X1 = " << x[1] << std::endl;
  std::cout << "Function value at minimum: " << val << std::endl;
  std::cout << "==========================================" << std::endl;
}

vector<double> FletcherRievesMethod(int spaceSize, Function F, vector<double> (*GradF)(Function F, vector<double>), 
                                    double eps_one_dim, double EPS_end, vector<double> start_point) 
{
   vector<double> x = start_point; 
   vector<double> p = -GradF(F, x);
   double gradSquare = innerProd(p, p);
   
   if (fs.is_open()) {
       fs << x[0] << ';' << x[1] << ';' << F(x) << "\n";
   }
   
   int numIter = 0;
   
   do {
       numIter++;
       double alpha, beta, newGradSquare;
       vector<double> newGrad;

       alpha = FindMin(F, x, p, eps_one_dim);
       x = x + p * alpha;
       
       if (std::abs(x[0]) > 1000.0 || std::abs(x[1]) > 1000.0) {
            std::cout << "[Error] Divergence detected! Coordinates grew too large." << std::endl;
            break;
       }

       if (fs.is_open()) {
           fs << x[0] << ';' << x[1] << ';' << F(x) << "\n";
       }

       newGrad = -GradF(F, x);
       newGradSquare = innerProd(newGrad, newGrad);

       if (numIter % (2 * spaceSize) == 0)
           beta = 0; 
       else
           beta = newGradSquare / gradSquare;

       p = newGrad + p * beta;
       gradSquare = newGradSquare;
       
       if (numIter > 5000) {
           std::cout << "[Warning] Maximum number of iterations exceeded (5000)!" << std::endl;
           break;
       }
   } while (gradSquare > EPS_end); // <-- Исправленная строка (цикл теперь закрывается корректно)
   
   PrintSolution(x, F(x), numIter);
   return x;
}

// =================================================================
// MAIN PROGRAM ENTRY POINT
// =================================================================
int main() {
   int choice = 1;
   double eps_one_dim, EPS_end;
   string filename;
   vector<double> start_point(2);

   std::cout << "=== FLETCHER-RIEVES CONJUGATE GRADIENT METHOD ===" << std::endl;
   std::cout << "Select function to minimize (Variant 3):" << std::endl;
   std::cout << "1) f(x) = ((x0-5)^2 * (x1-4)^2) + (x0-15)^2 + (x1-4)^2" << std::endl;
   std::cout << "2) f(x) = -1 / ((x0-5)^2 * (x1-4)^2 + 10*(x0-5)^2 + 50*(x1-4)^2 + 1)" << std::endl;
   std::cout << "Your choice (1 or 2): ";
   std::cin >> choice;

   if (choice == 2) {
       current_F = F_variant_B;
   } else {
       current_F = F_variant_A;
   }

   std::cout << "\nEnter calculation parameters:" << std::endl;
   std::cout << "Accuracy for 1D optimization (e.g., 1e-6): ";
   std::cin >> eps_one_dim;
   
   std::cout << "Accuracy for algorithm termination (e.g., 1e-9): ";
   std::cin >> EPS_end;
   
   std::cout << "Output filename for saving results (e.g., out.csv): ";
   std::cin >> filename;
   
   std::cout << "Initial point coordinate X0: ";
   std::cin >> start_point[0];
   std::cout << "Initial point coordinate X1: ";
   std::cin >> start_point[1];

   fs.open(filename);

   std::cout << "\n==========================================" << std::endl;
   std::cout << "INPUT CALCULATION DATA:" << std::endl;
   std::cout << "Selected Function: Variant 3 (" << (choice == 1 ? "A" : "B") << ")" << std::endl;
   std::cout << "1D Search Tolerance: " << eps_one_dim << std::endl;
   std::cout << "Termination Tolerance: " << EPS_end << std::endl;
   std::cout << "Trajectory File: " << filename << std::endl;
   std::cout << "Starting Point: [" << start_point[0] << "; " << start_point[1] << "]" << std::endl;
   std::cout << "==========================================" << std::endl;

   FletcherRievesMethod(2, current_F, &GradF1, eps_one_dim, EPS_end, start_point);

   if (fs.is_open()) {
       fs.close();
       std::cout << "Trajectory successfully saved to: " << filename << std::endl;
   }

   return 0;
}
