import unittest
import numpy as np
from fourier_series import calculate_fourier_coefficients, generate_fourier_series


def fourier_series_python(coefficients, num_samples):
    num_coefficients = len(coefficients) // 2
    series = np.zeros(num_samples, dtype=np.float64)
    for i in range(num_samples):
        for n in range(num_coefficients):
            real = coefficients[2 * n]
            imag = coefficients[2 * n + 1]
            series[i] += real * np.cos(2 * np.pi * i * n / num_samples) - imag * np.sin(2 * np.pi * i * n / num_samples)
    return series


def calculate_fourier_coefficients_python(signal, num_coefficients):
    signal_size = len(signal)
    coefficients = np.zeros(num_coefficients * 2, dtype=np.float64)

    for n in range(num_coefficients):
        real = 0.0
        imag = 0.0
        for t in range(signal_size):
            real += signal[t] * np.cos(2 * np.pi * n * t / signal_size)
            imag -= signal[t] * np.sin(2 * np.pi * n * t / signal_size)
        real /= signal_size
        imag /= signal_size
        coefficients[2 * n] = real
        coefficients[2 * n + 1] = imag

    return coefficients


class TestFourierSeries(unittest.TestCase):

    def test_calculate_fourier_coefficients(self):
        signals = [
            (np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64), 3),
            (np.zeros(10, dtype=np.float64), 5),
            (np.random.rand(10), 5),
            (np.linspace(0, 1, 100), 10),
            (np.sin(np.linspace(0, 2 * np.pi, 100)), 10)
        ]

        for signal, num_coefficients in signals:
            coefficients_cpp = calculate_fourier_coefficients(signal, num_coefficients)
            coefficients_python = calculate_fourier_coefficients_python(signal, num_coefficients)
            np.testing.assert_allclose(coefficients_cpp, coefficients_python, rtol=1e-5)

    def test_generate_fourier_series(self):
        test_cases = [
            (np.array([1.0, 0.0, 2.0, 0.0, 3.0, 0.0], dtype=np.float64), 100),
            (np.zeros(10, dtype=np.float64), 100),
            (np.random.rand(10), 100),
            (np.linspace(0, 1, 20), 100),
            (np.array([0.0, 1.0] * 5, dtype=np.float64), 100)
        ]

        for coefficients, num_samples in test_cases:
            series_cpp = generate_fourier_series(coefficients, num_samples)
            series_python = fourier_series_python(coefficients, num_samples)
            np.testing.assert_allclose(series_cpp, series_python, rtol=1e-5)

    def test_calculate_fourier_coefficients_with_numpy(self):
        signals = [
            (np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64), 3),
            (np.random.rand(50), 10),
            (np.linspace(-1, 1, 200), 20),
            (np.sin(np.linspace(0, 4 * np.pi, 50)), 5)
        ]

        for signal, num_coefficients in signals:
            coefficients_cpp = calculate_fourier_coefficients(signal, num_coefficients)
            coefficients_np = np.fft.fft(signal)[:num_coefficients] / len(signal)
            coefficients_np_real = np.zeros(num_coefficients * 2)
            coefficients_np_real[0::2] = coefficients_np.real
            coefficients_np_real[1::2] = coefficients_np.imag
            np.testing.assert_allclose(coefficients_cpp, coefficients_np_real, rtol=1e-5, atol=1e-10)

    def test_generate_fourier_series_with_numpy(self):
        test_cases = [
            (np.array([1.0, 0.0, 2.0, 0.0, 3.0, 0.0], dtype=np.float64), 100),
            (np.array([0.5, 1.5, 1.0, 0.0, 2.5, 3.5], dtype=np.float64), 100),
            (np.random.rand(20), 100),
            (np.linspace(-1, 1, 20), 100),
            (np.array([0.0, 1.0] * 5, dtype=np.float64), 100)
        ]

        for coefficients, num_samples in test_cases:
            series_cpp = generate_fourier_series(coefficients, num_samples)
            complex_coefficients = coefficients[0::2] + 1j * coefficients[1::2]
            complex_coefficients = np.concatenate(
                (complex_coefficients, np.zeros(num_samples - len(complex_coefficients))))
            series_np = np.fft.ifft(complex_coefficients).real * len(complex_coefficients)
            np.testing.assert_allclose(series_cpp, series_np, rtol=1e-3, atol=1e-10)


if __name__ == '__main__':
    unittest.main()
