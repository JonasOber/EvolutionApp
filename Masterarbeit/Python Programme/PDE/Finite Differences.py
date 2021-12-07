"""
Solving the poisson equation with finite differences.
T. Wick: p. 78

-u''(x) = f
"""
# libraries
from re import L
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

left_boundary = 0
right_boundary = 1
# analytic solution
@np.vectorize
def sol_u(x):
    return -(-x**2 + x)/2
    
def calc_poisson(steps):
    # Number of Grid points N
    N = int(steps)
    
    step_size = (right_boundary - left_boundary)/N
    # boundary conditions
    u_0 = 3
    u_1 = 2
    f = -1
    

    # u''(x) = (u(xj-1) + u(xj+1) - 2u(j) ) /h**2

    # set Au=b
    diag_element = 2*(1/step_size)**2
    A = np.zeros((N,N))
    # fill diagonal elements
    np.fill_diagonal(A, diag_element)
    # pad elements to all sides
    A = np.pad(A, ((1,1), (1,1)), mode='constant', constant_values = 0)
    #print(A)
    # fill boundary conditions
    A[0][0] = 1
    A[N+1][N+1] = 1
    #print(A)
    # fill next to diagonal elements
    next_diagonal_element = -1/step_size**2
    for i in range(1, N+1):
        A[i][i-1] = next_diagonal_element
        A[i] [i+1] = next_diagonal_element

    # set b
    b = np.zeros(N)
    b = b + f
    
    # add boundary conditions to b
    b = np.pad(b, (1,1), mode='constant', constant_values=0)
    b[0] = u_0
    b[N+1] = u_1
    #print(b)

    # solution with scipy.linalg.solve
    u = solve(A, b)
    print("-----------------")
    print(f"Completed u with {N} steps!")
    print("-----------------")
    return u

plt.figure()
steps_log = np.logspace(1,4, 5)
steps_log = [3]
for N in steps_log:
    x_discrete = np.linspace(left_boundary, right_boundary, N+2)
    u = calc_poisson(N)
    print(u)
    plt.plot(x_discrete, u, label=f"Numerical with {int(N)} steps")
x_analytic = np.linspace(left_boundary, right_boundary, 10000)
y_analytic = sol_u(x_analytic)
#plt.plot(x_analytic, y_analytic, label="Analytic solution")
plt.legend()
plt.savefig("poisson.png")