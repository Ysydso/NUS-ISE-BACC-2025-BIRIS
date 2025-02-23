import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

# First, let's verify the equation
# 44,700,000 / 13 = 3,428,461.5384615385

def objective(vars):
    x, y, z = vars
    return x/98 + y/147 + z/175.5

def constraint_eq(vars):
    x, y, z = vars
    return 98*x + 147*y + 175.5*z - 3428461.5384615385

# Set bounds for x, y, z
bounds = [(5676, 10676), (9313, 14313), (923, 5923)]

# Initial guess
x0 = np.array([10000, 10000, 2378.5])

# Setup constraint
constraint = {'type': 'eq', 'fun': constraint_eq}

# Solve
result = minimize(objective, x0, method='SLSQP', 
                 bounds=bounds, 
                 constraints=constraint)

x, y, z = result.x

print(f"Optimal solution found:")
print(f"x = {x:.2f}")
print(f"y = {y:.2f}")
print(f"z = {z:.2f}")
print(f"\nObjective value (x/98 + y/147 + z/175.5) = {result.fun:.4f}")
print(f"\nVerification:")
print(f"98x + 147y + 175.5z = {98*x + 147*y + 175.5*z:.2f}")
print(f"Target value = {3428461.5384615385:.2f}")
print(f"Constraint satisfied within {abs(98*x + 147*y + 175.5*z - 3428461.5384615385):.10f}")