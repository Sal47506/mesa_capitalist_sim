#!/usr/bin/env python3
"""
Create simplified dashboard using the enhanced simulation results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

def create_enhanced_dashboard(data):
    """Create comprehensive dashboard with available data."""
    
    # Create output directory
    output_dir = "debt_simulation_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    fig, axes = plt.subplots(4, 3, figsize=(20, 16))
    fig.suptitle('Enhanced Capitalist Economy - Comprehensive Analysis\n0% Unemployment with High Inequality', 
                fontsize=16, fontweight='bold')
    
    # Convert steps to years
    years = data.index / 52
    
    # 1. Surplus Value Extraction
    ax1 = axes[0, 0]
    ax1.plot(years, data['Total Surplus Value'], 'r-', linewidth=2, label='Surplus Value')
    ax1.plot(years, data['Total Wages'], 'b-', linewidth=2, label='Total Wages')
    ax1.set_title('Surplus Value vs. Wages', fontweight='bold')
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Amount ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Unemployment and Wage Share
    ax2 = axes[0, 1]
    ax2_twin = ax2.twinx()
    line1 = ax2.plot(years, data['Unemployment Rate'] * 100, 'orange', linewidth=2, label='Unemployment %')
    line2 = ax2_twin.plot(years, data['Wage Share'] * 100, 'green', linewidth=2, label='Wage Share %')
    ax2.set_title('Unemployment vs Wage Share', fontweight='bold')
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Unemployment Rate (%)', color='orange')
    ax2_twin.set_ylabel('Wage Share (%)', color='green')
    ax2.grid(True, alpha=0.3)
    
    # 3. GINI COEFFICIENT - Wealth Inequality
    ax3 = axes[0, 2]
    ax3.plot(years, data['Gini Coefficient'], 'purple', linewidth=3)
    ax3.fill_between(years, data['Gini Coefficient'], alpha=0.3, color='purple')
    ax3.axhline(y=0.4, color='orange', linestyle='--', alpha=0.7, label='High Inequality (0.4)')
    ax3.axhline(y=0.6, color='red', linestyle='--', alpha=0.7, label='Extreme Inequality (0.6)')
    ax3.set_title('Gini Coefficient (Wealth Inequality)', fontweight='bold')
    ax3.set_ylabel('Gini Coefficient')
    ax3.set_xlabel('Years')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Workers in Debt vs Bankrupt Workers
    ax4 = axes[1, 0]
    ax4.plot(years, data['Workers in Debt'], 'red', linewidth=2, label='Workers in Debt')
    ax4.plot(years, data['Bankrupt Workers'], 'darkred', linewidth=2, label='Bankrupt Workers')
    ax4.plot(years, data['Employed Workers'], 'green', linewidth=2, label='Employed Workers')
    ax4.set_title('Employment vs Debt Crisis', fontweight='bold')
    ax4.set_xlabel('Years')
    ax4.set_ylabel('Number of Workers')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Debt-to-Income Ratio
    ax5 = axes[1, 1]
    ax5.plot(years, data['Debt to Income Ratio'], 'purple', linewidth=2)
    ax5.axhline(y=1.0, color='orange', linestyle='--', alpha=0.7, label='1x Income (High Risk)')
    ax5.axhline(y=2.0, color='red', linestyle='--', alpha=0.7, label='2x Income (Crisis)')
    ax5.set_title('Debt-to-Income Ratio', fontweight='bold')
    ax5.set_xlabel('Years')
    ax5.set_ylabel('Debt/Income Ratio')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Total Worker Debt Growth
    ax6 = axes[1, 2]
    ax6.plot(years, data['Total Worker Debt'], 'brown', linewidth=2)
    ax6.fill_between(years, data['Total Worker Debt'], alpha=0.3, color='brown')
    ax6.set_title('Total Worker Debt Accumulation', fontweight='bold')
    ax6.set_xlabel('Years')
    ax6.set_ylabel('Total Debt ($)')
    ax6.grid(True, alpha=0.3)
    
    # 7. Net Wealth vs Gross Wealth
    ax7 = axes[2, 0]
    ax7.plot(years, data['Total Worker Wealth'], 'green', linewidth=2, label='Gross Wealth')
    ax7.plot(years, data['Net Worker Wealth'], 'blue', linewidth=2, label='Net Wealth (Wealth - Debt)')
    ax7.plot(years, -data['Total Worker Debt'], 'red', linewidth=2, label='Total Debt (negative)')
    ax7.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax7.set_title('Worker Wealth Analysis', fontweight='bold')
    ax7.set_xlabel('Years')
    ax7.set_ylabel('Amount ($)')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    
    # 8. Exploitation Rate vs Financial Stress
    ax8 = axes[2, 1]
    ax8_twin = ax8.twinx()
    line1 = ax8.plot(years, data['Average Exploitation Rate'] * 100, 'darkred', linewidth=2, label='Exploitation %')
    line2 = ax8_twin.plot(years, data['Average Financial Stress'], 'orange', linewidth=2, label='Financial Stress')
    ax8.set_title('Exploitation vs Financial Stress', fontweight='bold')
    ax8.set_xlabel('Years')
    ax8.set_ylabel('Exploitation Rate (%)', color='darkred')
    ax8_twin.set_ylabel('Financial Stress Level', color='orange')
    ax8.grid(True, alpha=0.3)
    
    # 9. Skill Distribution Over Time
    ax9 = axes[2, 2]
    ax9.plot(years, data['High Skill Workers'], 'blue', linewidth=2, label='High Skill')
    ax9.plot(years, data['Medium Skill Workers'], 'green', linewidth=2, label='Medium Skill')
    ax9.plot(years, data['Low Skill Workers'], 'red', linewidth=2, label='Low Skill')
    ax9.set_title('Skill Distribution Over Time', fontweight='bold')
    ax9.set_xlabel('Years')
    ax9.set_ylabel('Number of Workers')
    ax9.legend()
    ax9.grid(True, alpha=0.3)
    
    # 10. Unmet Needs Crisis
    ax10 = axes[3, 0]
    ax10.plot(years, data['Total Unmet Needs'], 'crimson', linewidth=2)
    ax10.fill_between(years, data['Total Unmet Needs'], alpha=0.3, color='crimson')
    ax10.set_title('Unmet Basic Needs Crisis', fontweight='bold')
    ax10.set_xlabel('Years')
    ax10.set_ylabel('Total Unmet Needs ($)')
    ax10.grid(True, alpha=0.3)
    
    # 11. Inflation Impact
    ax11 = axes[3, 1]
    real_wages = data['Total Wages'] / data['Price Index']
    ax11.plot(years, data['Total Wages'], 'blue', linewidth=2, label='Nominal Wages')
    ax11.plot(years, real_wages, 'green', linewidth=2, label='Real Wages')
    ax11.plot(years, data['Price Index'] * 100000, 'red', linewidth=2, label='Price Index (scaled)')
    ax11.set_title('Inflation Impact on Wages', fontweight='bold')
    ax11.set_xlabel('Years')
    ax11.set_ylabel('Amount ($)')
    ax11.legend()
    ax11.grid(True, alpha=0.3)
    
    # 12. Final Crisis Summary
    ax12 = axes[3, 2]
    final_data = data.iloc[-1]
    
    categories = ['Unemployment\n(%)', 'Workers\nin Debt\n(%)', 'Gini\nCoefficient\n(x100)', 'Exploitation\n(%)']
    values = [
        final_data['Unemployment Rate'] * 100,
        final_data['Workers in Debt'] / 1500 * 100,  # Assuming 1500 workers
        final_data['Gini Coefficient'] * 100,  # Scale Gini to percentage
        final_data['Average Exploitation Rate'] * 100
    ]
    
    colors = ['orange', 'red', 'purple', 'darkred']
    bars = ax12.bar(categories, values, color=colors, alpha=0.7)
    ax12.set_title('Final Economic Indicators', fontweight='bold')
    ax12.set_ylabel('Percentage')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax12.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{value:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save dashboard
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_capitalist_dashboard_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Enhanced Dashboard saved: {filepath}")
    return filepath

def print_enhanced_summary(data):
    """Print comprehensive summary."""
    final_data = data.iloc[-1]
    
    print("\n" + "="*60)
    print("ENHANCED CAPITALIST ECONOMY ANALYSIS")
    print("="*60)
    
    print(f"🏭 EMPLOYMENT SUCCESS:")
    print(f"   Unemployment Rate: {final_data['Unemployment Rate']*100:.1f}%")
    print(f"   Employed Workers: {final_data['Employed Workers']:.0f}")
    print(f"   ✅ FULL EMPLOYMENT ACHIEVED!")
    
    print(f"\n📊 WEALTH INEQUALITY:")
    gini = final_data['Gini Coefficient']
    print(f"   Gini Coefficient: {gini:.3f}")
    if gini > 0.6:
        print(f"   🚨 EXTREME wealth inequality (Gini > 0.6)!")
    elif gini > 0.4:
        print(f"   ⚠️ HIGH wealth inequality (Gini > 0.4)")
    print(f"   Net Worker Wealth: ${final_data['Net Worker Wealth']:,.0f}")
    
    print(f"\n💰 EXPLOITATION METRICS:")
    print(f"   Wage Share: {final_data['Wage Share']*100:.1f}%")
    print(f"   Exploitation Rate: {final_data['Average Exploitation Rate']*100:.1f}%")
    print(f"   Total Profit: ${final_data['Total Profit']:,.0f}")
    print(f"   Total Wages: ${final_data['Total Wages']:,.0f}")
    
    print(f"\n📊 DEBT STATISTICS:")
    print(f"   Total Worker Debt: ${final_data['Total Worker Debt']:,.0f}")
    print(f"   Average Debt per Worker: ${final_data['Average Debt per Worker']:,.0f}")
    print(f"   Workers in Debt: {final_data['Workers in Debt']:.0f} ({final_data['Workers in Debt']/1500*100:.1f}%)")
    print(f"   Debt-to-Income Ratio: {final_data['Debt to Income Ratio']:.2f}x")
    
    print(f"\n🎯 SKILL DISTRIBUTION:")
    print(f"   High-skill Workers: {final_data['High Skill Workers']:.0f} ({final_data['High Skill Workers']/1500*100:.1f}%)")
    print(f"   Medium-skill Workers: {final_data['Medium Skill Workers']:.0f} ({final_data['Medium Skill Workers']/1500*100:.1f}%)")
    print(f"   Low-skill Workers: {final_data['Low Skill Workers']:.0f} ({final_data['Low Skill Workers']/1500*100:.1f}%)")
    print(f"   Firm Owners: {final_data['Firm Owners']:.0f} ({final_data['Firm Owners']/1500*100:.1f}%)")
    
    print(f"\n📈 ECONOMIC DYNAMICS:")
    print(f"   Inflation (Price Index): {final_data['Price Index']:.3f}")
    print(f"   Financial Stress: {final_data['Average Financial Stress']:.3f}")
    print(f"   Unmet Needs: ${final_data['Total Unmet Needs']:,.0f}")

    print("="*60)

def main():
    print("=" * 60)
    print("ENHANCED SIMULATION DASHBOARD CREATION")
    print("=" * 60)
    
    # Load the enhanced simulation results
    filename = "enhanced_simulation_results_20250623_125144.csv"
    print(f"Loading data from: {filename}")
    
    try:
        data = pd.read_csv(filename)
        print(f"✅ Data loaded successfully!")
        print(f"📊 Data shape: {data.shape}")
        print(f"📊 Final unemployment rate: {data['Unemployment Rate'].iloc[-1]*100:.1f}%")
        print(f"📊 Final Gini coefficient: {data['Gini Coefficient'].iloc[-1]:.3f}")
        
        # Create dashboard
        create_enhanced_dashboard(data)
        print_enhanced_summary(data)
        
        print(f"\n✅ Enhanced dashboard created with correct data!")
        
    except FileNotFoundError:
        print(f"❌ File {filename} not found!")
        print("Available CSV files:")
        import glob
        csv_files = glob.glob("*simulation_results_*.csv")
        for f in csv_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main() 