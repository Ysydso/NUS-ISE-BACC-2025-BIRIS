import numpy as np
from itertools import product

# Data from Tables
quarters = ['Q1_26', 'Q2_26', 'Q3_26', 'Q4_26', 'Q1_27', 'Q2_27', 'Q3_27', 'Q4_27']
TAM = [21.8e9, 27.4e9, 34.9e9, 39.0e9, 44.7e9, 51.5e9, 52.5e9, 53.5e9]  # in GB

# Node data: GB per wafer and Yield (from Table 2)
node_data = {
    'Node1': {
        'GBpW': [100000] * 8,
        'Yield': [0.98] * 8
    },
    'Node2': {
        'GBpW': [150000] * 8,
        'Yield': [0.60, 0.82, 0.95, 0.98, 0.98, 0.98, 0.98, 0.98]
    },
    'Node3': {
        'GBpW': [270000] * 8,
        'Yield': [0.20, 0.25, 0.35, 0.50, 0.65, 0.85, 0.95, 0.98]
    }
}

# Workstation data (Table 4)
workstations = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
initial_tools = [10, 18, 5, 11, 15, 2, 23, 3, 4, 1]
utilization = [0.78, 0.76, 0.80, 0.80, 0.76, 0.80, 0.70, 0.85, 0.75, 0.60]
capex_per_tool = [3.0e6, 6.0e6, 2.2e6, 3.0e6, 3.5e6, 6.0e6, 2.1e6, 1.8e6, 3.0e6, 8.0e6]

minute_loads = {
    'Node1': {
        'A':4.0, 'B':6.0, 'C':2.0, 'D':5.0, 'E':5.0, 'F':0, 'G':12.0, 'H':2.1, 'I':0, 'J':0
    },
    'Node2': {
        'A':4.0, 'B':9.0, 'C':2.0, 'D':5.0, 'E':10.0, 'F':1.8, 'G':0, 'H':0, 'I':6.0, 'J':0
    },
    'Node3': {
        'A':4.0, 'B':15.0, 'C':5.4, 'D':0, 'E':0, 'F':5.8, 'G':16.0, 'H':0, 'I':0, 'J':2.1
    }
}

# Initial loading for Q1_26 (from Table 3)
initial_load = {
    'Node1': 12000,
    'Node2': 5000,
    'Node3': 1000
}

# Precompute for each quarter and node the GB per wafer * Yield
gb_per_wafer = {}
for q in range(8):
    gb_per_wafer[q] = {
        'Node1': node_data['Node1']['GBpW'][q] * node_data['Node1']['Yield'][q],
        'Node2': node_data['Node2']['GBpW'][q] * node_data['Node2']['Yield'][q],
        'Node3': node_data['Node3']['GBpW'][q] * node_data['Node3']['Yield'][q]
    }

def calculate_gb_output(loads, q):
    total = 0
    for node in ['Node1', 'Node2', 'Node3']:
        total += loads[node] * gb_per_wafer[q][node]
    return total * 13  # 13 weeks

def compute_tool_requirements(loads, q):
    tool_req = np.zeros(len(workstations))
    for node in ['Node1', 'Node2', 'Node3']:
        load = loads[node]
        for i, ws in enumerate(workstations):
            ml = minute_loads[node].get(ws, 0)
            if ml == 0:
                continue
            util = utilization[i]
            req = (load * ml) / (7 * 24 * 60 * util)
            tool_req[i] += req
    return np.ceil(tool_req)

def compute_capex(tool_req, prev_tools, ws_idx):
    required = tool_req[ws_idx]
    prev = prev_tools[ws_idx]
    additional = max(0, required - prev)
    return additional * capex_per_tool[ws_idx]

# Initialize variables
current_load = initial_load.copy()
prev_tools = initial_tools.copy()
total_capex = 0
loading_profile = [current_load.copy()]

# Iterate through each quarter starting from Q2_26 (index 1)
for q_idx in range(1, 8):
    q = q_idx  # current quarter index (0-based)
    best_load = None
    min_capex = float('inf')
    
    # Determine possible loading ranges for each node
    ranges = {}
    for node in ['Node1', 'Node2', 'Node3']:
        prev_load = current_load[node]
        lower = max(0, prev_load - 2500)
        upper = prev_load + 2500
        ranges[node] = np.arange(lower, upper + 1, 100)  # step of 500 for simplification
        
    # Generate possible combinations
    for loads in product(ranges['Node1'], ranges['Node2'], ranges['Node3']):
        candidate = {
            'Node1': loads[0],
            'Node2': loads[1],
            'Node3': loads[2]
        }
        # Check GB output matches TAM within ±2e9
        gb_out = calculate_gb_output(candidate, q)
        if abs(gb_out - TAM[q]) > 2e9:  # allow ±2B GB tolerance
            continue
        
        # Compute tool requirements and CAPEX
        tool_req = compute_tool_requirements(candidate, q)
        capex = 0
        for i in range(len(workstations)):
            req = tool_req[i]
            additional = max(0, req - prev_tools[i])
            capex += additional * capex_per_tool[i]
        
        if capex < min_capex:
            min_capex = capex
            best_load = candidate
            best_tool_req = tool_req
    
    if best_load is None:
        raise ValueError(f"No valid load found for quarter {q_idx + 1}")
    
    # Update for next quarter
    total_capex += min_capex
    prev_tools = best_tool_req
    current_load = best_load
    loading_profile.append(current_load.copy())

# Calculate total contribution margin
total_contribution = sum(TAM) * 0.002  # $0.002 per GB
net_profit = total_contribution - total_capex

# Output results
print("Optimal Loading Profile:")
for q, load in enumerate(loading_profile):
    print(f"{quarters[q]}: Node1={load['Node1']}, Node2={load['Node2']}, Node3={load['Node3']}")
print(f"\nTotal CAPEX: ${total_capex / 1e6:.2f}M")
print(f"Net Profit: ${net_profit / 1e6:.2f}M")