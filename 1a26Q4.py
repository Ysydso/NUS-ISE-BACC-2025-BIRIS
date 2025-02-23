import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

# First, let's verify the equation
# 39,000,000 / 13 = 3,000,000

def objective(vars):
    x, y, z = vars
    return x/98 + y/147 + z/135

def constraint_eq(vars):
    x, y, z = vars
    return 98*x + 147*y + 135*z - 3000000

# Set bounds for x, y, z
bounds = [(8176, 13176), (7500, 12500), (0, 4757)]

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
print(f"\nObjective value (x/98 + y/147 + z/135) = {result.fun:.4f}")
print(f"\nVerification:")
print(f"98x + 147y + 135z = {98*x + 147*y + 135*z:.2f}")
print(f"Target value = {3000000:.2f}")
print(f"Constraint satisfied within {abs(98*x + 147*y + 135*z - 3000000):.10f}")