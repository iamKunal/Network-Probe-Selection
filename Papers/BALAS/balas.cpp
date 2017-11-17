#include <iostream>
#include <vector>
#include <queue>
#include <tuple>
#include <fstream>
#include <sstream>
#include <functional>
 
using namespace std;
 
#define n 192 // # variables
#define m 240 // # constraints
 
 
string input_file = "scpcyc06.txt";
int A[m][n] ;//= {{-2, 6, -3, 4, 1, -2}, {-5, -3, 1, 3, -2, 1}, {5, -1, 4, -2, 2, -1}};
int B[m] ;//= {2, -2, 3};
int C[n] ;//= {3, 5, 6, 9, 10, 10};
 
int best_solution = -1;
bool is_inf = true;
vector<int> X;
queue<pair< vector<int>,int>> work_ques[2];
//priority_queue< pair< vector<int>, int >, vector<pair<vector<int>, int>>, Comparator> heap;
 
 
void print_vector(int* v) {
    for(int i = 0; i < n; ++i) {
        cout << v[i] << " ";
    }
}
void print_vector(vector<int> v) {
    for(int i = 0; i < v.size(); ++i) {
        cout << v[i] << " ";
    }
}
 
 
int eval(vector<int> arr, int to_substract, int to_add, double previous_value) {
    if(to_add == -1) {
        return 0.0;
    }
    int to_return = 0;
    for(int i = 0; i < n; ++i) {
        to_return += C[i] * arr[i];
    }
   
    return to_return;  
}
 
 
void read_data() {
    for(int i = 0; i < n; ++i) {
        X.push_back(0);
    }
    ifstream in(input_file.c_str());
    if(in.is_open()) {
        while(!in.eof()) {
            int a;
            in >> a;
            in >> a;
            // read costs
            for(int i = 0; i < n; ++i) {
                in >> a;
                C[i] = a;
            }
            // read constraints
            for(int i = 0; i < m; ++i) {
                int len;
                in >> len;
                for(int j = 0; j < len; ++j) {
                    in >> a;
                    A[i][a-1] = 1;
                }
                B[i] = 1;
            }
            break;
 
        }
        in.close();
    }
    else {
        cerr << "Cannot open file" << endl;
        exit(1);
    }
 
   
}
void read_data_fimi() {
    for(int i = 0; i < n; ++i) {
        X.push_back(0);
        C[i] = 1;
    }
    ifstream in(input_file.c_str());
    if(in.is_open()) {
        for(int i = 0; i < n; ++i) {
        }
        while(!in.eof()) {
            // read constraints
                int a, i = 0;
                string line;
                while(getline(in, line)) {
                    istringstream iss(line);
                    while(iss >> a) {
                        A[i][a-1] = 1;
                    }
                    B[i++] = 1;
                }
                break;
 
        }
        in.close();
    }
    else {
        cerr << "Cannot open file" << endl;
        exit(1);
    }
}
bool is_possible(vector<int> x, int current, int constraint) {
    for(int i = current+1; i < x.size(); ++i) {
        if(A[constraint][i] > 0) {
            x[i] = 1;
        }
        else {
            x[i] = 0;
        }
    }
    int temp = 0.0;
    for(int i = 0; i < n; ++i) {
        temp += A[constraint][i] * x[i];
    }
    if(temp < B[constraint]) {
        return false;
    }
    return true;
}
std::pair<bool,bool> is_feasable(vector<int> x, int current, bool debug) {
    std::pair<bool,bool> to_return(true, true);
    for(int i = 0; i < m;i++) {
        int temp = 0;
        for(int j = 0; j < n; j++) {
            temp += A[i][j] * x[j];
        }
        if(temp < B[i]) {
            to_return.first = false;
        }
        if(debug) {
            cout << temp << " " << B[i] << " " << endl;
        }
       
        if(!is_possible(x, current, i)) {
            to_return.second = false;
        }
    }
    return to_return;
}
 
void solve(vector<int> x, int current, bool debug) {
    int temp = 0;
    temp = eval(x, 1, 1, temp);
    if(debug) {
        cout << endl << "Temp, current = " << temp << ", " << current << "; ";
        print_vector(x);
        cout << endl;
    }
    pair<bool,bool> flags = is_feasable(x, current, false);
    if(flags.first) {
        if(temp < best_solution || is_inf) {
            X = x;
            best_solution = temp;
            is_inf = false;
            if(debug)
                cout << "better than previous best" << endl;
        }
    }
    bool test = (!is_inf && temp <= best_solution) || is_inf;
    if(!flags.first && flags.second) {
        if(debug) {
            cout << endl << "\t";
            if(!flags.first) {
                cout << "not feasable ";
            }
        }
        if(current <= n - 3 && test) {
 
        pair<vector<int>, int> el;
        el.second = current + 1;
//      if(newx[current+1] != 1) {
        if(true) {
            x[current+1] = 1;
            el.first= x;
            work_ques[0].push(el); 
        }
       
 
        x[current+1] = 0;
        x[current+2] = 1;
        el.first = x;
        if(debug) {
            cout << "\n\tAdded nodes " << endl << "\t";
        }
        work_ques[0].push(el);
        }
 
    }
    if(debug && !flags.second) {
        cout << "\timpossible\n";
    }
 
    if(work_ques[0].size() > 0) {
        pair<vector<int>, int> work = work_ques[0].front();
        work_ques[0].pop();
        cout  << "OPT = " << best_solution << endl;
        cout << work_ques[0].size() << endl;
        print_vector(work.first);
        cout << endl << "curent = " << current << endl;
        return solve(work.first, work.second, debug);
    }
    return;
 
}
 
 
int main() {
    read_data();
    solve(X, -1, 0);
    cout  << "OPT = " << best_solution << endl;
    return 0;
			}
