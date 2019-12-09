# Cholesky Decomposition

```python
# import Numerical Python Library
import numpy as np

# Generate Example Matrix A(3X3), Lower Triangle Matrix L(3X3)
A = np.array(
    [[  6,  15,  55],
     [ 15,  55, 225],
     [ 55, 225, 979]], dtype=np.float32)
L = np.zeros_like(A)

# Do Cholesky Decomposition
L[0, 0] = np.sqrt(A[0, 0])
L[1, 0] = A[1, 0] / L[0, 0]
L[1, 1] = np.sqrt(A[1, 1] - L[1, 0] ** 2)
L[2, 0] = A[2, 0] / L[0, 0]
L[2, 1] = (A[2, 1] - L[1, 0] * L[2, 0]) / L[1, 1]
L[2, 2] = np.sqrt(A[2, 2] - L[2, 0] ** 2 - L[2, 1] ** 2)

# Check Result
np.all(A - L.dot(L.T) < 1e-7) # True
```
