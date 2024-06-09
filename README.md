# Fourier Series

## Overview
`fourier_series` is a Python package with a C++ extension for computing Fourier Series coefficients and generating Fourier Series.

## Installation
To install the package, run:
```sh
pip install .
```

## Usage
Here's a simple example of how to use the fourier_series package:
```python
import numpy as np
from fourier_series import calculate_fourier_coefficients, generate_fourier_series

# Example signal
signal = np.random.rand(1000)
num_coefficients = 100

# Calculate Fourier coefficients
coeffs = calculate_fourier_coefficients(signal, num_coefficients)

# Generate Fourier series
num_samples = 1000
series = generate_fourier_series(coeffs, num_samples)

print(series)
```

## Running Tests
To run the tests, use the following command:
```sh
python -m unittest discover -s tests
```
