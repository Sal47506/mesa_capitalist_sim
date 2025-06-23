#!/usr/bin/env python3
"""
Create dashboard using the correct enhanced simulation results.
"""

import pandas as pd
from debt_dashboard import DebtCapitalistDashboard

def main():
    print("=" * 60)
    print("CREATING DASHBOARD WITH CORRECT DATA")
    print("=" * 60)
    
    # Load the correct enhanced simulation results
    filename = "enhanced_simulation_results_20250623_125144.csv"
    print(f"Loading data from: {filename}")
    
    try:
        data = pd.read_csv(filename, index_col=0)
        print(f"✅ Data loaded successfully!")
        print(f"📊 Data shape: {data.shape}")
        print(f"📊 Final unemployment rate: {data['Unemployment Rate'].iloc[-1]*100:.1f}%")
        print(f"📊 Final Gini coefficient: {data['Gini Coefficient'].iloc[-1]:.3f}")
        
        # Create dashboard
        dashboard = DebtCapitalistDashboard(data)
        dashboard.create_comprehensive_dashboard()
        dashboard.create_debt_analysis()
        dashboard.print_debt_summary()
        
        print(f"\n✅ Correct dashboards created!")
        
    except FileNotFoundError:
        print(f"❌ File {filename} not found!")
        print("Available CSV files:")
        import glob
        csv_files = glob.glob("*simulation_results_*.csv")
        for f in csv_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main() 