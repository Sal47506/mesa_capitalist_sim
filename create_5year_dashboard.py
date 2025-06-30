#!/usr/bin/env python3
"""
Comprehensive 5-Year Simulation Dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def create_comprehensive_dashboard():
    """Create comprehensive dashboard for 5-year simulation."""
    
    # Load the 5-year simulation data
    df = pd.read_csv('enhanced_simulation_results_20250630_130937.csv')
    weeks = np.arange(len(df))
    years = weeks / 52

    print('🔥 5-YEAR SIMULATION - COMPREHENSIVE ANALYSIS')
    print('=' * 60)

    # Create comprehensive dashboard
    fig, axes = plt.subplots(4, 4, figsize=(24, 20))
    fig.suptitle('5-Year Capitalist Economy Simulation - Comprehensive Analysis', 
                fontsize=18, fontweight='bold')

    # 1. INFLATION & PRICE INDEX
    axes[0,0].plot(years, df['Price Index'], 'red', linewidth=3, label='Price Index')
    axes[0,0].fill_between(years, df['Price Index'], alpha=0.3, color='red')
    axes[0,0].set_title('Inflation Over 5 Years', fontweight='bold')
    axes[0,0].set_xlabel('Years')
    axes[0,0].set_ylabel('Price Index (Base=1.0)')
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].legend()

    # 2. NOMINAL vs REAL WAGES
    axes[0,1].plot(years, df['Total Wages'], 'blue', linewidth=3, label='Nominal Wages')
    axes[0,1].plot(years, df['Real Wage Total'], 'green', linewidth=3, label='Real Wages')
    axes[0,1].set_title('Nominal vs Real Wages', fontweight='bold')
    axes[0,1].set_xlabel('Years')
    axes[0,1].set_ylabel('Total Wages ($)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)

    # 3. WAGES BY SKILL LEVEL (NOMINAL)
    axes[0,2].plot(years, df['High Skill Average Wage'], 'gold', linewidth=3, label='High')
    axes[0,2].plot(years, df['Medium Skill Average Wage'], 'orange', linewidth=3, label='Medium')
    axes[0,2].plot(years, df['Low Skill Average Wage'], 'red', linewidth=3, label='Low')
    axes[0,2].set_title('Average Wages by Skill Level', fontweight='bold')
    axes[0,2].set_xlabel('Years')
    axes[0,2].set_ylabel('Weekly Wage ($)')
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)

    # 4. REAL WAGES BY SKILL LEVEL
    axes[0,3].plot(years, df['High Skill Real Wage'], 'gold', linewidth=3, label='High Real')
    axes[0,3].plot(years, df['Medium Skill Real Wage'], 'orange', linewidth=3, label='Med Real')
    axes[0,3].plot(years, df['Low Skill Real Wage'], 'red', linewidth=3, label='Low Real')
    axes[0,3].set_title('Real Wages by Skill Level', fontweight='bold')
    axes[0,3].set_xlabel('Years')
    axes[0,3].set_ylabel('Real Weekly Wage ($)')
    axes[0,3].legend()
    axes[0,3].grid(True, alpha=0.3)

    # 5. EXPLOITATION RATES BY SKILL LEVEL
    axes[1,0].plot(years, df['High Skill Exploitation'] * 100, 'darkred', linewidth=3, label='High')
    axes[1,0].plot(years, df['Medium Skill Exploitation'] * 100, 'red', linewidth=3, label='Med')
    axes[1,0].plot(years, df['Low Skill Exploitation'] * 100, 'orange', linewidth=3, label='Low')
    axes[1,0].set_title('Exploitation Rates by Skill Level', fontweight='bold')
    axes[1,0].set_xlabel('Years')
    axes[1,0].set_ylabel('Exploitation Rate (%)')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)

    # 6. FIRM PROFITS vs WORKER DEBT
    axes[1,1].plot(years, df['Total Profit'], 'green', linewidth=3, label='Profits')
    ax_twin = axes[1,1].twinx()
    ax_twin.plot(years, df['Total Worker Debt'], 'darkred', linewidth=3, label='Debt')
    axes[1,1].set_title('Firm Profits vs Worker Debt', fontweight='bold')
    axes[1,1].set_xlabel('Years')
    axes[1,1].set_ylabel('Weekly Profit ($)', color='green')
    ax_twin.set_ylabel('Total Debt ($)', color='darkred')
    axes[1,1].grid(True, alpha=0.3)

    # 7. UNEMPLOYMENT RATE
    axes[1,2].plot(years, df['Unemployment Rate'] * 100, 'purple', linewidth=3)
    axes[1,2].fill_between(years, df['Unemployment Rate'] * 100, alpha=0.3, color='purple')
    axes[1,2].set_title('Unemployment Rate', fontweight='bold')
    axes[1,2].set_xlabel('Years')
    axes[1,2].set_ylabel('Unemployment Rate (%)')
    axes[1,2].grid(True, alpha=0.3)

    # 8. GINI COEFFICIENT
    axes[1,3].plot(years, df['Gini Coefficient'], 'purple', linewidth=3)
    axes[1,3].fill_between(years, df['Gini Coefficient'], alpha=0.3, color='purple')
    axes[1,3].axhline(y=0.4, color='orange', linestyle='--', alpha=0.7, label='High')
    axes[1,3].axhline(y=0.6, color='red', linestyle='--', alpha=0.7, label='Extreme')
    axes[1,3].set_title('Wealth Inequality (Gini)', fontweight='bold')
    axes[1,3].set_xlabel('Years')
    axes[1,3].set_ylabel('Gini Coefficient')
    axes[1,3].legend()
    axes[1,3].grid(True, alpha=0.3)

    # 9. CUMULATIVE SURPLUS VALUE
    cumulative_surplus = df['Total Surplus Value'].cumsum()
    axes[2,0].plot(years, cumulative_surplus, 'darkred', linewidth=3)
    axes[2,0].fill_between(years, cumulative_surplus, alpha=0.3, color='darkred')
    axes[2,0].set_title('Cumulative Surplus Value Extracted', fontweight='bold')
    axes[2,0].set_xlabel('Years')
    axes[2,0].set_ylabel('Cumulative Surplus ($)')
    axes[2,0].grid(True, alpha=0.3)

    # 10. WAGE SHARE
    axes[2,1].plot(years, df['Wage Share'] * 100, 'blue', linewidth=3)
    axes[2,1].fill_between(years, df['Wage Share'] * 100, alpha=0.3, color='blue')
    axes[2,1].set_title('Wage Share of Output', fontweight='bold')
    axes[2,1].set_xlabel('Years')
    axes[2,1].set_ylabel('Wage Share (%)')
    axes[2,1].grid(True, alpha=0.3)

    # 11. FINANCIAL STRESS & UNMET NEEDS
    axes[2,2].plot(years, df['Average Financial Stress'], 'orange', linewidth=3)
    ax_twin2 = axes[2,2].twinx()
    ax_twin2.plot(years, df['Total Unmet Needs'], 'crimson', linewidth=3)
    axes[2,2].set_title('Financial Stress & Unmet Needs', fontweight='bold')
    axes[2,2].set_xlabel('Years')
    axes[2,2].set_ylabel('Avg Financial Stress', color='orange')
    ax_twin2.set_ylabel('Total Unmet Needs ($)', color='crimson')
    axes[2,2].grid(True, alpha=0.3)

    # 12. WORKERS IN DEBT
    axes[2,3].plot(years, df['Workers in Debt'], 'darkred', linewidth=3)
    axes[2,3].fill_between(years, df['Workers in Debt'], alpha=0.3, color='darkred')
    axes[2,3].set_title('Workers in Debt Crisis', fontweight='bold')
    axes[2,3].set_xlabel('Years')
    axes[2,3].set_ylabel('Workers in Debt')
    axes[2,3].grid(True, alpha=0.3)

    # 13. SKILL WAGE GAPS
    safe_low = df['Low Skill Average Wage'].replace(0, 1)  # Avoid division by zero
    skill_premium_med = df['Medium Skill Average Wage'] / safe_low
    skill_premium_high = df['High Skill Average Wage'] / safe_low
    axes[3,0].plot(years, skill_premium_med, 'orange', linewidth=3, label='Med/Low')
    axes[3,0].plot(years, skill_premium_high, 'gold', linewidth=3, label='High/Low')
    axes[3,0].set_title('Skill-Based Wage Inequality', fontweight='bold')
    axes[3,0].set_xlabel('Years')
    axes[3,0].set_ylabel('Wage Ratio')
    axes[3,0].legend()
    axes[3,0].grid(True, alpha=0.3)

    # 14. INFLATION RATE
    if len(df) > 52:
        annual_inflation = (df['Price Index'] / df['Price Index'].shift(52) - 1) * 100
        axes[3,1].plot(years[52:], annual_inflation[52:], 'red', linewidth=3)
        axes[3,1].axhline(y=2, color='green', linestyle='--', alpha=0.7, label='Target 2%')
    axes[3,1].set_title('Annual Inflation Rate', fontweight='bold')
    axes[3,1].set_xlabel('Years')
    axes[3,1].set_ylabel('Annual Inflation (%)')
    axes[3,1].legend()
    axes[3,1].grid(True, alpha=0.3)

    # 15. NET WEALTH vs PROFITS
    cumulative_profits = df['Total Profit'].cumsum()
    axes[3,2].plot(years, df['Net Worker Wealth'], 'blue', linewidth=3, label='Net Worker Wealth')
    axes[3,2].plot(years, cumulative_profits, 'green', linewidth=3, label='Cumulative Profits')
    axes[3,2].axhline(y=0, color='black', linestyle='-', alpha=0.5)
    axes[3,2].set_title('Net Worker Wealth vs Firm Profits', fontweight='bold')
    axes[3,2].set_xlabel('Years')
    axes[3,2].set_ylabel('Amount ($)')
    axes[3,2].legend()
    axes[3,2].grid(True, alpha=0.3)

    # 16. ECONOMIC SUMMARY
    final_data = df.iloc[-1]
    categories = ['Unemployment\n(%)', 'Workers in\nDebt (%)', 'Gini\nCoeff', 'Avg Exploit\n(%)']
    values = [
        final_data['Unemployment Rate'] * 100,
        final_data['Workers in Debt'] / 1500 * 100,
        final_data['Gini Coefficient'] * 100,
        final_data['Average Exploitation Rate'] * 100
    ]
    colors = ['purple', 'red', 'darkred', 'orange']
    bars = axes[3,3].bar(categories, values, color=colors, alpha=0.7)
    axes[3,3].set_title('Final Crisis Indicators', fontweight='bold')
    axes[3,3].set_ylabel('Percentage')
    for bar, value in zip(bars, values):
        height = bar.get_height()
        axes[3,3].text(bar.get_x() + bar.get_width()/2., height + 1,
                     f'{value:.1f}%', ha='center', va='bottom')

    plt.tight_layout()

    # Save comprehensive dashboard
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'comprehensive_5year_dashboard_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f'📊 Comprehensive 5-Year Dashboard saved: {filename}')
    
    # Print analysis
    print_analysis(df)
    
    return filename

def print_analysis(df):
    """Print comprehensive analysis of results."""
    print()
    print('🔥 5-YEAR SIMULATION SUMMARY:')
    print('=' * 50)
    final_data = df.iloc[-1]
    total_profit = df['Total Profit'].sum()
    total_surplus = df['Total Surplus Value'].sum()
    total_wages = df['Total Wages'].sum()

    print(f'💰 Total Firm Profits (5 years): ${total_profit:,.0f}')
    print(f'🔥 Total Surplus Value Extracted: ${total_surplus:,.0f}')
    print(f'💸 Total Wages Paid: ${total_wages:,.0f}')
    print(f'📈 Final Unemployment Rate: {final_data["Unemployment Rate"]*100:.1f}%')
    print(f'💳 Workers in Debt: {final_data["Workers in Debt"]:.0f} ({final_data["Workers in Debt"]/1500*100:.1f}%)')
    print(f'💰 Total Worker Debt: ${final_data["Total Worker Debt"]:,.0f}')
    print(f'📊 Final Gini Coefficient: {final_data["Gini Coefficient"]:.3f}')
    print(f'🔥 Final Inflation: {(final_data["Price Index"]-1)*100:.1f}% over 5 years')
    print()
    print('SKILL-BASED WAGE ANALYSIS:')
    print(f'High Skill Final Wage: ${final_data["High Skill Average Wage"]:,.0f}/week')
    print(f'Medium Skill Final Wage: ${final_data["Medium Skill Average Wage"]:,.0f}/week')  
    print(f'Low Skill Final Wage: ${final_data["Low Skill Average Wage"]:,.0f}/week')
    print(f'High/Low Skill Wage Ratio: {final_data["High Skill Average Wage"]/final_data["Low Skill Average Wage"]:.2f}x')

if __name__ == "__main__":
    create_comprehensive_dashboard() 