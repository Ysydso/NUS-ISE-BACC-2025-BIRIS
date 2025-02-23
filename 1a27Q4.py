import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

# First, let's verify the equation
# 53,500,000 / 13 = 4115384.615384615

def objective(vars):
    x, y, z = vars
    return x/98 + y/147 + z/264.6

def constraint_eq(vars):
    x, y, z = vars
    return 98*x + 147*y + 264.6*z - 4115384.615384615

# Set bounds for x, y, z
bounds = [(0, 3176), (6681, 11681), (7723, 12723)]

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
print(f"98x + 147y + 175.5z = {98*x + 147*y + 264.6*z:.2f}")
print(f"Target value = {4115384.615384615:.2f}")
print(f"Constraint satisfied within {abs(98*x + 147*y + 264.6*z - 4115384.615384615):.10f}")