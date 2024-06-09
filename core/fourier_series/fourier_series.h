#ifndef FOURIER_SERIES_H
#define FOURIER_SERIES_H

#include <vector>
#include <cstring>

extern "C" {

double* calculateFourierCoefficients(const double* signal, int signalSize, int numCoefficients);

double* generateFourierSeries(const double* coefficients, int numCoefficients, int numSamples);

}

#endif // FOURIER_SERIES_H
