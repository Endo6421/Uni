import math
import matplotlib.pyplot as plt
import numpy as np

cost_r1 = 15000 * 4133.33
cost_r2 = 30000 * 3000.00

vol_cap = 225
r1_mass_cap = 15000
r2_mass_cap = 30000

densities = {
    'LOX': 1141,
    'LCH4': 422,
    'LH2': 71
}

tot_meth = 2053181
mass_lox_methalox = tot_meth * (6 / 7)
mass_lch4_methalox = tot_meth * (1 / 7)

tot_hy = 1489518
mass_lox_hydrolox = tot_hy * (39 / 50)
mass_lh2_hydrolox = tot_hy * (11 / 50)

components = {
    "Metanuppdrag - LOX": {"mass": mass_lox_methalox, "density": densities['LOX'], "mission": "Metan/Syre"},
    "Metanuppdrag - LCH4": {"mass": mass_lch4_methalox, "density": densities['LCH4'], "mission": "Metan/Syre"},
    "Väteuppdrag - LOX": {"mass": mass_lox_hydrolox, "density": densities['LOX'], "mission": "Väte/Syre"},
    "Väteuppdrag - LH2": {"mass": mass_lh2_hydrolox, "density": densities['LH2'], "mission": "Väte/Syre"}
}

def optimize_launches(total_mass, density):
    r1_actual_cap = min(r1_mass_cap, vol_cap * density)
    r2_actual_cap = min(r2_mass_cap, vol_cap * density)
    
    min_cost = float('inf')
    best_r1 = 0
    best_r2 = 0
    
    max_r2 = math.ceil(total_mass / r2_actual_cap)
    
    for r2 in range(max_r2 + 1):
        mass_remaining = total_mass - (r2 * r2_actual_cap)
        if mass_remaining <= 0:
            r1 = 0
        else:
            r1 = math.ceil(mass_remaining / r1_actual_cap)
        
        cost = (r1 * cost_r1) + (r2 * cost_r2)
        
        if cost < min_cost:
            min_cost = cost
            best_r1 = r1
            best_r2 = r2
            
    return best_r1, best_r2, min_cost

results = []
mission_costs = {"Metan/Syre": 0, "Väte/Syre": 0}

for name, data in components.items():
    r1_count, r2_count, cost = optimize_launches(data["mass"], data["density"])
    results.append({
        "name": name,
        "r1_count": r1_count,
        "r2_count": r2_count
    })
    mission_costs[data["mission"]] += cost

names = [r["name"] for r in results]
r1_counts = [r["r1_count"] for r in results]
r2_counts = [r["r2_count"] for r in results]

x = np.arange(len(names))
width = 0.35

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

rects1 = ax1.bar(x - width/2, r1_counts, width, label='Raket 1', color='#1f77b4')
rects2 = ax1.bar(x + width/2, r2_counts, width, label='Raket 2', color='#ff7f0e')

ax1.set_ylabel('Antal uppskjutningar')
ax1.set_title('Optimala raketuppskjutningar per bränsle')
ax1.set_xticks(x)
ax1.set_xticklabels(names, rotation=15, ha="right")
ax1.legend()

ax1.bar_label(rects1, padding=3)
ax1.bar_label(rects2, padding=3)

missions = list(mission_costs.keys())
costs_in_billions = [cost / 1e9 for cost in mission_costs.values()]

colors = ['#2ca02c', '#d62728']
bars = ax2.bar(missions, costs_in_billions, color=colors, width=0.5)

ax2.set_ylabel('Kostnad (Miljarder USD)')
ax2.set_title('Totalkostnad per uppdrag')
ax2.bar_label(bars, fmt='%.2f B$', padding=3)

plt.tight_layout()
plt.show()
