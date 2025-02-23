import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

# First, let's verify the equation
# 34,900,000 / 13 = 2,684,615.3846153846

def objective(vars):
    x, y, z = vars
    return x/98 + y/142.5 + z/94.5

def constraint_eq(vars):
    x, y, z = vars
    return 98*x + 142.5*y + 94.5*z - 2684615.3846153846

# Set bounds for x, y, z
bounds = [(9593, 14593), (5000, 10000), (0, 3500)]

# Initial guess
x0 = np.array([10000, 7500, 1750])

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
print(f"\nObjective value (x/98 + y/142.5 + z/94.5) = {result.fun:.4f}")
print(f"\nVerification:")
print(f"98x + 142.5y + 94.5z = {98*x + 142.5*y + 94.5*z:.2f}")
print(f"Target value = {2684615.3846153846:.2f}")
print(f"Constraint satisfied within {abs(98*x + 142.5*y + 94.5*z - 2684615.3846153846):.10f}")