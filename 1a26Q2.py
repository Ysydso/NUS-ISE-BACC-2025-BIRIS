import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

# 27,400,000 / 13 = 2,107,692.3076923077

def objective(vars):
    x, y, z = vars
    return x/98 + y/123 + z/67.5

def constraint_eq(vars):
    x, y, z = vars
    return 98*x + 123*y + 67.5*z - 2107692.3076923077

# Set bounds for x, y, z
bounds = [(9500, 14500), (2500, 7500), (0, 3500)]

# Initial guess
x0 = np.array([10000, 5000, 1750])

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
print(f"\nObjective value (x/98 + y/123 + z/67.5) = {result.fun:.4f}")
print(f"\nVerification:")
print(f"98x + 123y + 67z = {98*x + 123*y + 67.5*z:.2f}")
print(f"Target value = {2107692.3076923077:.2f}")
print(f"Constraint satisfied within {abs(98*x + 123*y + 67.5*z - 2107692.3076923077):.10f}")