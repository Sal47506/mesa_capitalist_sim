#!/usr/bin/env python3
"""
Create all dashboards for the debt-enhanced capitalist simulation.
"""

import os
from run_simple_simulation import SimpleCapitalistModel
from worker_dashboard import WorkerDashboard
from debt_dashboard import main as debt_dashboard_main

def main():
    print("=" * 60)
    print("COMPREHENSIVE DASHBOARD CREATION")
    print("=" * 60)
    
    print("📊 Creating debt crisis dashboard from latest simulation...")
    debt_dashboard_main()
    
    print("\n👥 Creating worker-level analysis...")
    # Create a small model for worker analysis
    model = SimpleCapitalistModel(num_workers=200, num_firms=10)  # Fixed: only 2 parameters
    
    print("Running short simulation for worker analysis...")
    for step in range(104):  # 2 years
        model.step()
        if step % 26 == 0:  # Progress every 6 months
            print(f"  Step {step}/104 ({step/104*100:.0f}%)")
    
    # Create worker dashboard
    worker_dash = WorkerDashboard(model)
    worker_dash.create_worker_analysis()
    worker_dash.create_firm_analysis()
    worker_dash.print_worker_summary()
    
    print(f"\n✅ All dashboards created! Check debt_simulation_results/ folder")
    
    # List all files
    result_dir = "debt_simulation_results"
    if os.path.exists(result_dir):
        files = os.listdir(result_dir)
        print(f"\n📁 Generated files ({len(files)} total):")
        for f in sorted(files):
            if f.endswith('.png'):
                print(f"  📊 {f}")

if __name__ == "__main__":
    main() 