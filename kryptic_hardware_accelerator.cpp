#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

extern "C" double matrix_accelerator_pass(double alpha, double beta) {
    const double normalized = std::clamp((alpha + beta) / 2.0, 0.0, 1.0);
    return normalized;
}

int main(int argc, char** argv) {
    const double alpha = (argc > 1) ? std::stod(argv[1]) : 0.75;
    const double beta = (argc > 2) ? std::stod(argv[2]) : 0.20;
    const double result = matrix_accelerator_pass(alpha, beta);
    std::cout << result << std::endl;
    return 0;
}
