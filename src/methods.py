import ctypes
import numpy as np
import os

lib_path = os.path.join(os.path.dirname(__file__), 'libfourier_series.so')
fourier_lib = ctypes.cdll.LoadLibrary(lib_path)

calculate_fourier_coefficients_cpp = fourier_lib.calculateFourierCoefficients
calculate_fourier_coefficients_cpp.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
calculate_fourier_coefficients_cpp.restype = ctypes.POINTER(ctypes.c_double)

generate_fourier_series_cpp = fourier_lib.generateFourierSeries
generate_fourier_series_cpp.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
generate_fourier_series_cpp.restype = ctypes.POINTER(ctypes.c_double)


def calculate_fourier_coefficients(signal, num_coefficients):
    signal_size = len(signal)
    signal_ptr = np.ascontiguousarray(signal, dtype=np.float64)
    coeffs_ptr = calculate_fourier_coefficients_cpp(signal_ptr, signal_size, num_coefficients)
    coeffs = np.ctypeslib.as_array(coeffs_ptr, shape=(num_coefficients * 2,))
    return coeffs


def generate_fourier_series(coefficients, num_samples):
    num_coeffs = len(coefficients) // 2
    coeffs_ptr = np.ctypeslib.as_ctypes(coefficients)
    series_ptr = generate_fourier_series_cpp(coeffs_ptr, num_coeffs, num_samples)
    series = np.ctypeslib.as_array(series_ptr, shape=(num_samples,))
    return series

