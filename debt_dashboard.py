#!/usr/bin/env python3
"""
Comprehensive dashboard for debt-enhanced capitalist simulation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

class DebtCapitalistDashboard:
    def __init__(self, model_data: pd.DataFrame):
        self.model_data = model_data
        self.output_dir = "debt_simulation_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_comprehensive_dashboard(self):
        """Create comprehensive dashboard with debt mechanics."""
        fig, axes = plt.subplots(4, 3, figsize=(20, 16))
        fig.suptitle('Capitalist Economy with Debt Mechanics - Comprehensive Analysis', 
                    fontsize=16, fontweight='bold')
        
        # Convert steps to years
        years = self.model_data.index / 52
        
        # 1. Surplus Value Extraction
        ax1 = axes[0, 0]
        ax1.plot(years, self.model_data['Total Surplus Value'], 'r-', linewidth=2, label='Surplus Value')
        ax1.plot(years, self.model_data['Total Wages'], 'b-', linewidth=2, label='Total Wages')
        ax1.set_title('Surplus Value vs. Wages', fontweight='bold')
        ax1.set_xlabel('Years')
        ax1.set_ylabel('Amount ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Unemployment and Wage Share
        ax2 = axes[0, 1]
        ax2_twin = ax2.twinx()
        line1 = ax2.plot(years, self.model_data['Unemployment Rate'] * 100, 'orange', linewidth=2, label='Unemployment %')
        line2 = ax2_twin.plot(years, self.model_data['Wage Share'] * 100, 'green', linewidth=2, label='Wage Share %')
        ax2.set_title('Unemployment vs Wage Share', fontweight='bold')
        ax2.set_xlabel('Years')
        ax2.set_ylabel('Unemployment Rate (%)', color='orange')
        ax2_twin.set_ylabel('Wage Share (%)', color='green')
        ax2.grid(True, alpha=0.3)
        
        # 3. GINI COEFFICIENT - Wealth Inequality
        ax3 = axes[0, 2]
        if 'Gini Coefficient' in self.model_data.columns:
            ax3.plot(years, self.model_data['Gini Coefficient'], 'purple', linewidth=3)
            ax3.fill_between(years, self.model_data['Gini Coefficient'], alpha=0.3, color='purple')
            ax3.axhline(y=0.4, color='orange', linestyle='--', alpha=0.7, label='High Inequality (0.4)')
            ax3.axhline(y=0.6, color='red', linestyle='--', alpha=0.7, label='Extreme Inequality (0.6)')
            ax3.set_title('Gini Coefficient (Wealth Inequality)', fontweight='bold')
            ax3.set_ylabel('Gini Coefficient')
            ax3.legend()
        else:
            # Fallback: Total Worker Debt Crisis
            ax3.plot(years, self.model_data['Total Worker Debt'], 'darkred', linewidth=3)
            ax3.fill_between(years, self.model_data['Total Worker Debt'], alpha=0.3, color='darkred')
            ax3.set_title('Total Worker Debt Crisis', fontweight='bold')
            ax3.set_ylabel('Total Debt ($)')
        ax3.set_xlabel('Years')
        ax3.grid(True, alpha=0.3)
        
        # 4. Workers in Debt vs Bankrupt Workers
        ax4 = axes[1, 0]
        ax4.plot(years, self.model_data['Workers in Debt'], 'red', linewidth=2, label='Workers in Debt')
        ax4.plot(years, self.model_data['Bankrupt Workers'], 'darkred', linewidth=2, label='Bankrupt Workers')
        if 'Long-term Unemployed' in self.model_data.columns:
            ax4.plot(years, self.model_data['Long-term Unemployed'], 'orange', linewidth=2, label='Long-term Unemployed')
        ax4.set_title('Financial Crisis Progression', fontweight='bold')
        ax4.set_xlabel('Years')
        ax4.set_ylabel('Number of Workers')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Debt-to-Income Ratio
        ax5 = axes[1, 1]
        ax5.plot(years, self.model_data['Debt to Income Ratio'], 'purple', linewidth=2)
        ax5.axhline(y=1.0, color='orange', linestyle='--', alpha=0.7, label='1x Income (High Risk)')
        ax5.axhline(y=2.0, color='red', linestyle='--', alpha=0.7, label='2x Income (Crisis)')
        ax5.set_title('Debt-to-Income Ratio', fontweight='bold')
        ax5.set_xlabel('Years')
        ax5.set_ylabel('Debt/Income Ratio')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Debt Payments vs Wages
        ax6 = axes[1, 2]
        debt_payment_ratio = (self.model_data['Total Debt Payments'] / self.model_data['Total Wages']) * 100
        ax6.plot(years, debt_payment_ratio, 'brown', linewidth=2)
        ax6.set_title('Debt Payments as % of Total Wages', fontweight='bold')
        ax6.set_xlabel('Years')
        ax6.set_ylabel('Debt Payments (% of Wages)')
        ax6.grid(True, alpha=0.3)
        
        # 7. Net Wealth vs Gross Wealth
        ax7 = axes[2, 0]
        ax7.plot(years, self.model_data['Total Worker Wealth'], 'green', linewidth=2, label='Gross Wealth')
        if 'Net Worker Wealth' in self.model_data.columns:
            ax7.plot(years, self.model_data['Net Worker Wealth'], 'blue', linewidth=2, label='Net Wealth (Wealth - Debt)')
        ax7.plot(years, -self.model_data['Total Worker Debt'], 'red', linewidth=2, label='Total Debt (negative)')
        ax7.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax7.set_title('Worker Wealth Analysis', fontweight='bold')
        ax7.set_xlabel('Years')
        ax7.set_ylabel('Amount ($)')
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        # 8. Exploitation Rate vs Financial Stress
        ax8 = axes[2, 1]
        ax8_twin = ax8.twinx()
        line1 = ax8.plot(years, self.model_data['Average Exploitation Rate'] * 100, 'darkred', linewidth=2, label='Exploitation %')
        line2 = ax8_twin.plot(years, self.model_data['Average Financial Stress'], 'orange', linewidth=2, label='Financial Stress')
        ax8.set_title('Exploitation vs Financial Stress', fontweight='bold')
        ax8.set_xlabel('Years')
        ax8.set_ylabel('Exploitation Rate (%)', color='darkred')
        ax8_twin.set_ylabel('Financial Stress Level', color='orange')
        ax8.grid(True, alpha=0.3)
        
        # 9. Economic Growth - Profits vs Wages vs Debt
        ax9 = axes[2, 2]
        # Calculate cumulative growth
        profit_growth = (self.model_data['Total Profit'] / self.model_data['Total Profit'].iloc[0] - 1) * 100
        wage_growth = (self.model_data['Total Wages'] / self.model_data['Total Wages'].iloc[0] - 1) * 100
        debt_growth = (self.model_data['Total Worker Debt'] / max(1, self.model_data['Total Worker Debt'].iloc[0]) - 1) * 100
        
        ax9.plot(years, profit_growth, 'red', linewidth=2, label='Profit Growth')
        ax9.plot(years, wage_growth, 'blue', linewidth=2, label='Wage Growth')
        ax9.plot(years, debt_growth, 'darkred', linewidth=2, label='Debt Growth')
        ax9.set_title('Cumulative Growth Rates', fontweight='bold')
        ax9.set_xlabel('Years')
        ax9.set_ylabel('Growth (%)')
        ax9.legend()
        ax9.grid(True, alpha=0.3)
        
        # 10. Unmet Needs Crisis
        ax10 = axes[3, 0]
        ax10.plot(years, self.model_data['Total Unmet Needs'], 'crimson', linewidth=2)
        ax10.fill_between(years, self.model_data['Total Unmet Needs'], alpha=0.3, color='crimson')
        ax10.set_title('Unmet Basic Needs Crisis', fontweight='bold')
        ax10.set_xlabel('Years')
        ax10.set_ylabel('Total Unmet Needs ($)')
        ax10.grid(True, alpha=0.3)
        
        # 11. Inflation Impact
        ax11 = axes[3, 1]
        real_wages = self.model_data['Total Wages'] / self.model_data['Price Index']
        ax11.plot(years, self.model_data['Total Wages'], 'blue', linewidth=2, label='Nominal Wages')
        ax11.plot(years, real_wages, 'green', linewidth=2, label='Real Wages')
        ax11.plot(years, self.model_data['Price Index'] * 100000, 'red', linewidth=2, label='Price Index (scaled)')
        ax11.set_title('Inflation Impact on Wages', fontweight='bold')
        ax11.set_xlabel('Years')
        ax11.set_ylabel('Amount ($)')
        ax11.legend()
        ax11.grid(True, alpha=0.3)
        
        # 12. Crisis Summary with Gini Coefficient
        ax12 = axes[3, 2]
        # Create a summary chart showing crisis indicators
        final_data = self.model_data.iloc[-1]
        
        categories = ['Unemployment\n(%)', 'Workers\nin Debt\n(%)', 'Bankrupt\nWorkers\n(%)', 'Gini\nCoefficient']
        values = [
            final_data['Unemployment Rate'] * 100,
            final_data['Workers in Debt'] / 1500 * 100,  # Assuming 1500 workers
            final_data['Bankrupt Workers'] / 1500 * 100,
            final_data.get('Gini Coefficient', 0) * 100  # Scale Gini to percentage
        ]
        
        colors = ['orange', 'red', 'darkred', 'purple']
        bars = ax12.bar(categories, values, color=colors, alpha=0.7)
        ax12.set_title('Final Crisis Indicators', fontweight='bold')
        ax12.set_ylabel('Percentage')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax12.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                     f'{value:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save dashboard
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debt_capitalist_dashboard_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Debt Crisis Dashboard saved: {filepath}")
        return filepath
    
    def create_debt_analysis(self):
        """Create detailed debt crisis analysis."""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Debt Crisis Analysis', fontsize=16, fontweight='bold')
            
            years = self.model_data.index / 52
            
            # 1. Debt accumulation over time
            axes[0, 0].plot(years, self.model_data['Total Worker Debt'], linewidth=3, color='darkred')
            axes[0, 0].fill_between(years, self.model_data['Total Worker Debt'], alpha=0.3, color='darkred')
            axes[0, 0].set_title('Total Worker Debt Accumulation')
            axes[0, 0].set_xlabel('Years')
            axes[0, 0].set_ylabel('Total Debt ($)')
            axes[0, 0].grid(True, alpha=0.3)
            
            # 2. Debt distribution - simplified
            final_data = self.model_data.iloc[-1]
            debt_categories = ['Workers\nin Debt', 'Bankrupt\nWorkers']
            debt_values = [final_data['Workers in Debt'] - final_data['Bankrupt Workers'], final_data['Bankrupt Workers']]
            
            # Only show if we have non-zero values
            if sum(debt_values) > 0:
                axes[0, 1].pie([v for v in debt_values if v > 0], 
                              labels=[debt_categories[i] for i, v in enumerate(debt_values) if v > 0],
                              autopct='%1.1f%%', colors=['orange', 'red'])
                axes[0, 1].set_title('Final Debt Distribution')
            else:
                axes[0, 1].text(0.5, 0.5, 'No Debt Data', ha='center', va='center', transform=axes[0, 1].transAxes)
                axes[0, 1].set_title('Final Debt Distribution')
            
            # 3. Debt-to-income evolution
            axes[1, 0].plot(years, self.model_data['Debt to Income Ratio'], linewidth=2, color='purple')
            axes[1, 0].axhline(y=1.0, color='orange', linestyle='--', label='High Risk (1x)')
            axes[1, 0].axhline(y=2.0, color='red', linestyle='--', label='Crisis (2x)')
            axes[1, 0].set_title('Debt-to-Income Ratio Evolution')
            axes[1, 0].set_xlabel('Years')
            axes[1, 0].set_ylabel('Debt/Income Ratio')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
            
            # 4. Debt service burden
            debt_service_ratio = (self.model_data['Total Debt Payments'] / 
                                 self.model_data['Total Wages'].replace(0, 1)) * 100  # Avoid div by zero
            axes[1, 1].plot(years, debt_service_ratio, linewidth=2, color='brown')
            axes[1, 1].set_title('Debt Service Burden')
            axes[1, 1].set_xlabel('Years')
            axes[1, 1].set_ylabel('Debt Payments (% of Total Wages)')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save analysis
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debt_crisis_analysis_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 Debt Crisis Analysis saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error creating debt analysis: {e}")
            return None
    
    def print_debt_summary(self):
        """Print comprehensive debt crisis summary."""
        final_data = self.model_data.iloc[-1]
        initial_data = self.model_data.iloc[0]
        
        print("\n" + "="*60)
        print("COMPREHENSIVE ECONOMIC CRISIS ANALYSIS")
        print("="*60)
        
        print(f"🏭 UNEMPLOYMENT CRISIS:")
        print(f"   Unemployment Rate: {final_data['Unemployment Rate']*100:.1f}%")
        if 'Long-term Unemployment Rate' in final_data:
            print(f"   Long-term Unemployment: {final_data['Long-term Unemployment Rate']*100:.1f}%")
        print(f"   Employed Workers: {final_data.get('Employed Workers', 0):.0f}")
        
        print(f"\n📊 WEALTH INEQUALITY:")
        if 'Gini Coefficient' in final_data:
            gini = final_data['Gini Coefficient']
            print(f"   Gini Coefficient: {gini:.3f}")
            if gini > 0.6:
                print(f"   🚨 EXTREME wealth inequality (Gini > 0.6)!")
            elif gini > 0.4:
                print(f"   ⚠️ HIGH wealth inequality (Gini > 0.4)")
        print(f"   Net Worker Wealth: ${final_data.get('Net Worker Wealth', 0):,.0f}")
        
        print(f"\n📊 DEBT STATISTICS:")
        print(f"   Total Worker Debt: ${final_data['Total Worker Debt']:,.0f}")
        print(f"   Average Debt per Worker: ${final_data['Average Debt per Worker']:,.0f}")
        print(f"   Workers in Debt: {final_data['Workers in Debt']:.0f} ({final_data['Workers in Debt']/1500*100:.1f}%)")
        print(f"   Bankrupt Workers: {final_data['Bankrupt Workers']:.0f} ({final_data['Bankrupt Workers']/1500*100:.1f}%)")

        print(f"\n💰 DEBT BURDEN:")
        print(f"   Average Debt-to-Income Ratio: {final_data['Debt to Income Ratio']:.2f}x")
        debt_service = (final_data['Total Debt Payments'] / final_data['Total Wages']) * 100
        print(f"   Debt Service Burden: {debt_service:.1f}% of total wages")

        print(f"\n📈 TRENDS:")
        if initial_data['Total Worker Debt'] > 0:
            debt_growth = ((final_data['Total Worker Debt'] / initial_data['Total Worker Debt']) - 1) * 100
            print(f"   Total Debt Growth: {debt_growth:+.1f}%")
        else:
            print(f"   Total Debt Growth: Started from $0")
        
        if 'Gini Coefficient' in final_data and 'Gini Coefficient' in initial_data:
            gini_change = final_data['Gini Coefficient'] - initial_data['Gini Coefficient']
            print(f"   Gini Coefficient Change: {gini_change:+.3f}")

        print(f"\n⚠️ CRISIS INDICATORS:")
        if final_data['Bankrupt Workers'] > 0:
            print(f"   🚨 {final_data['Bankrupt Workers']:.0f} workers are bankrupt!")
        if final_data.get('Gini Coefficient', 0) > 0.6:
            print(f"   🚨 Extreme wealth inequality (Gini = {final_data['Gini Coefficient']:.3f})!")
        if final_data['Unemployment Rate'] > 0.5:
            print(f"   🚨 Mass unemployment exceeds 50%!")
        if debt_service > 25:
            print(f"   🚨 Debt service burden exceeds 25% of wages!")

        print("="*60)

def main():
    """Load data and create dashboard."""
    import glob
    
    # Find the most recent simulation results
    csv_files = glob.glob("simple_simulation_results_*.csv")
    if not csv_files:
        print("No simulation results found. Run the simulation first!")
        return
    
    latest_file = max(csv_files, key=os.path.getctime)
    print(f"Loading data from: {latest_file}")
    
    # Load data
    data = pd.read_csv(latest_file, index_col=0)
    
    # Create dashboard
    dashboard = DebtCapitalistDashboard(data)
    dashboard.create_comprehensive_dashboard()
    dashboard.create_debt_analysis()
    dashboard.print_debt_summary()
    
    print(f"\n✅ All visualizations saved in: {dashboard.output_dir}/")

if __name__ == "__main__":
    main() 