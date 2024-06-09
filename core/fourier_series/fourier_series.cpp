#include "fourier_series.h"
#include <cmath>

double* calculateFourierCoefficients(const double* signal, int signalSize, int numCoefficients) {
    double* coefficients = new double[numCoefficients * 2];
    std::memset(coefficients, 0, numCoefficients * 2 * sizeof(double));

    std::vector<std::vector<double>> cos_values(numCoefficients, std::vector<double>(signalSize));
    std::vector<std::vector<double>> sin_values(numCoefficients, std::vector<double>(signalSize));

    for (int n = 0; n < numCoefficients; ++n) {
        for (int t = 0; t < signalSize; ++t) {
            double angle = 2 * M_PI * n * t / signalSize;
            cos_values[n][t] = cos(angle);
            sin_values[n][t] = sin(angle);
        }
    }

    for (int n = 0; n < numCoefficients; ++n) {
        double real = 0.0;
        double imag = 0.0;
        for (int t = 0; t < signalSize; ++t) {
            real += signal[t] * cos_values[n][t];
            imag -= signal[t] * sin_values[n][t];
        }
        real /= signalSize;
        imag /= signalSize;
        coefficients[2 * n] = real;
        coefficients[2 * n + 1] = imag;
    }

    return coefficients;
}

double* generateFourierSeries(const double* coefficients, int numCoefficients, int numSamples) {
    double* series = new double[numSamples];
    std::memset(series, 0, numSamples * sizeof(double));

    std::vector<std::vector<double>> cos_values(numCoefficients, std::vector<double>(numSamples));
    std::vector<std::vector<double>> sin_values(numCoefficients, std::vector<double>(numSamples));

    for (int n = 0; n < numCoefficients; ++n) {
        for (int i = 0; i < numSamples; ++i) {
            double angle = 2 * M_PI * i * n / numSamples;
            cos_values[n][i] = cos(angle);
            sin_values[n][i] = sin(angle);
        }
    }

    for (int i = 0; i < numSamples; ++i) {
        for (int n = 0; n < numCoefficients; ++n) {
            double real = coefficients[2 * n];
            double imag = coefficients[2 * n + 1];
            series[i] += real * cos_values[n][i] - imag * sin_values[n][i];
        }
    }

    return series;
}
