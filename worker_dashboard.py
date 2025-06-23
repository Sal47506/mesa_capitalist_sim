#!/usr/bin/env python3
"""
Worker-level dashboard for debt-enhanced capitalist simulation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

class WorkerDashboard:
    def __init__(self, simulation_model):
        self.model = simulation_model
        self.workers = simulation_model.get_workers()
        self.firms = simulation_model.get_firms()
        self.output_dir = "debt_simulation_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_palette("viridis")
        
    def create_worker_analysis(self):
        """Create comprehensive worker-level analysis."""
        fig, axes = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Individual Worker Analysis - Debt & Economic Status', 
                    fontsize=16, fontweight='bold')
        
        # Extract worker data
        worker_data = self._extract_worker_data()
        
        # 1. Wealth Distribution
        axes[0, 0].hist(worker_data['wealth'], bins=50, alpha=0.7, color='green')
        axes[0, 0].set_title('Worker Wealth Distribution')
        axes[0, 0].set_xlabel('Wealth ($)')
        axes[0, 0].set_ylabel('Number of Workers')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Debt Distribution
        debt_data = worker_data[worker_data['debt'] > 0]['debt']
        if len(debt_data) > 0:
            axes[0, 1].hist(debt_data, bins=30, alpha=0.7, color='red')
            axes[0, 1].set_title(f'Debt Distribution ({len(debt_data)} workers in debt)')
        else:
            axes[0, 1].text(0.5, 0.5, 'No Workers in Debt', ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('Debt Distribution')
        axes[0, 1].set_xlabel('Debt ($)')
        axes[0, 1].set_ylabel('Number of Workers')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Employment Status
        employment_counts = worker_data['employed'].value_counts()
        axes[0, 2].pie([employment_counts.get(True, 0), employment_counts.get(False, 0)],
                      labels=['Employed', 'Unemployed'], autopct='%1.1f%%',
                      colors=['lightgreen', 'lightcoral'])
        axes[0, 2].set_title('Employment Status')
        
        # 4. Wage Distribution (for employed workers)
        employed_workers = worker_data[worker_data['employed'] == True]
        if len(employed_workers) > 0:
            axes[1, 0].hist(employed_workers['wage'], bins=30, alpha=0.7, color='blue')
            axes[1, 0].set_title(f'Wage Distribution ({len(employed_workers)} employed)')
        else:
            axes[1, 0].text(0.5, 0.5, 'No Employed Workers', ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Wage Distribution')
        axes[1, 0].set_xlabel('Weekly Wage ($)')
        axes[1, 0].set_ylabel('Number of Workers')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Debt-to-Income Ratio (for employed workers with debt)
        employed_with_debt = employed_workers[employed_workers['debt'] > 0]
        if len(employed_with_debt) > 0:
            debt_to_income = employed_with_debt['debt'] / (employed_with_debt['wage'] * 52)
            axes[1, 1].hist(debt_to_income, bins=20, alpha=0.7, color='purple')
            axes[1, 1].axvline(x=1.0, color='orange', linestyle='--', label='1x Income (High Risk)')
            axes[1, 1].axvline(x=2.0, color='red', linestyle='--', label='2x Income (Crisis)')
            axes[1, 1].set_title(f'Debt-to-Income Ratios ({len(employed_with_debt)} workers)')
            axes[1, 1].legend()
        else:
            axes[1, 1].text(0.5, 0.5, 'No Employed Workers\nwith Debt', ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Debt-to-Income Ratios')
        axes[1, 1].set_xlabel('Debt/Annual Income Ratio')
        axes[1, 1].set_ylabel('Number of Workers')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Financial Stress Distribution
        stress_data = [w.calculate_financial_stress() for w in self.workers]
        axes[1, 2].hist(stress_data, bins=30, alpha=0.7, color='orange')
        axes[1, 2].set_title('Financial Stress Levels')
        axes[1, 2].set_xlabel('Financial Stress (0-1)')
        axes[1, 2].set_ylabel('Number of Workers')
        axes[1, 2].grid(True, alpha=0.3)
        
        # 7. Unmet Needs Distribution
        unmet_needs = worker_data[worker_data['unmet_needs'] > 0]['unmet_needs']
        if len(unmet_needs) > 0:
            axes[2, 0].hist(unmet_needs, bins=30, alpha=0.7, color='crimson')
            axes[2, 0].set_title(f'Unmet Basic Needs ({len(unmet_needs)} workers affected)')
        else:
            axes[2, 0].text(0.5, 0.5, 'No Unmet Needs', ha='center', va='center', transform=axes[2, 0].transAxes)
            axes[2, 0].set_title('Unmet Basic Needs')
        axes[2, 0].set_xlabel('Unmet Needs ($)')
        axes[2, 0].set_ylabel('Number of Workers')
        axes[2, 0].grid(True, alpha=0.3)
        
        # 8. Bankruptcy Analysis
        bankrupt_count = sum(1 for w in self.workers if w.is_bankrupt)
        debt_count = sum(1 for w in self.workers if w.debt > 0)
        solvent_count = len(self.workers) - debt_count
        
        bankruptcy_data = [solvent_count, debt_count - bankrupt_count, bankrupt_count]
        bankruptcy_labels = [f'Debt-Free\n({solvent_count})', f'In Debt\n({debt_count - bankrupt_count})', f'Bankrupt\n({bankrupt_count})']
        
        axes[2, 1].pie(bankruptcy_data, labels=bankruptcy_labels, autopct='%1.1f%%',
                      colors=['lightgreen', 'orange', 'darkred'])
        axes[2, 1].set_title('Financial Health Status')
        
        # 9. Wealth vs Debt Scatter
        axes[2, 2].scatter(worker_data['wealth'], worker_data['debt'], alpha=0.6, s=30)
        axes[2, 2].set_xlabel('Wealth ($)')
        axes[2, 2].set_ylabel('Debt ($)')
        axes[2, 2].set_title('Wealth vs Debt Relationship')
        axes[2, 2].grid(True, alpha=0.3)
        
        # Add diagonal line for reference
        max_val = max(worker_data['wealth'].max(), worker_data['debt'].max())
        axes[2, 2].plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Equal Wealth/Debt')
        axes[2, 2].legend()
        
        plt.tight_layout()
        
        # Save dashboard
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"worker_analysis_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"👥 Worker Analysis Dashboard saved: {filepath}")
        return filepath
    
    def create_firm_analysis(self):
        """Create firm-level analysis."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Firm Analysis - Capitalist Perspectives', fontsize=16, fontweight='bold')
        
        # Extract firm data
        firm_data = self._extract_firm_data()
        
        # 1. Firm Profit Distribution
        axes[0, 0].hist(firm_data['profit'], bins=15, alpha=0.7, color='green')
        axes[0, 0].set_title('Firm Profit Distribution')
        axes[0, 0].set_xlabel('Weekly Profit ($)')
        axes[0, 0].set_ylabel('Number of Firms')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Worker Count per Firm
        axes[0, 1].hist(firm_data['worker_count'], bins=15, alpha=0.7, color='blue')
        axes[0, 1].set_title('Workers per Firm')
        axes[0, 1].set_xlabel('Number of Workers')
        axes[0, 1].set_ylabel('Number of Firms')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Capital Distribution
        axes[1, 0].hist(firm_data['capital'], bins=15, alpha=0.7, color='gold')
        axes[1, 0].set_title('Firm Capital Distribution')
        axes[1, 0].set_xlabel('Capital ($)')
        axes[1, 0].set_ylabel('Number of Firms')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Exploitation Rate Distribution
        exploitation_rates = [f.get_exploitation_rate() for f in self.firms]
        axes[1, 1].hist(exploitation_rates, bins=15, alpha=0.7, color='red')
        axes[1, 1].set_title('Exploitation Rate by Firm')
        axes[1, 1].set_xlabel('Average Exploitation Rate')
        axes[1, 1].set_ylabel('Number of Firms')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save analysis
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"firm_analysis_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"🏭 Firm Analysis Dashboard saved: {filepath}")
        return filepath
    
    def _extract_worker_data(self):
        """Extract worker data into a pandas DataFrame."""
        data = []
        for worker in self.workers:
            data.append({
                'wealth': worker.wealth,
                'debt': worker.debt,
                'employed': worker.is_employed,
                'wage': worker.wage if worker.is_employed else 0,
                'unmet_needs': worker.get_unmet_needs(),
                'basic_needs': worker.basic_needs,
                'weeks_unemployed': worker.weeks_unemployed,
                'weeks_employed': getattr(worker, 'weeks_employed', 0),
                'financial_stress': worker.calculate_financial_stress(),
                'is_bankrupt': worker.is_bankrupt,
                'debt_payments': getattr(worker, 'debt_payments', 0)
            })
        return pd.DataFrame(data)
    
    def _extract_firm_data(self):
        """Extract firm data into a pandas DataFrame."""
        data = []
        for firm in self.firms:
            data.append({
                'profit': firm.profit,
                'capital': firm.capital,
                'worker_count': len(firm.workers),
                'max_workers': firm.max_workers,
                'wage_share': firm.wage_share,
                'surplus_value_rate': firm.surplus_value_rate,
                'taxes_paid': firm.taxes_paid,
                'exploitation_rate': firm.get_exploitation_rate()
            })
        return pd.DataFrame(data)
    
    def print_worker_summary(self):
        """Print comprehensive worker statistics."""
        worker_data = self._extract_worker_data()
        
        print("\n" + "="*60)
        print("INDIVIDUAL WORKER ANALYSIS")
        print("="*60)
        
        print(f"👥 EMPLOYMENT STATISTICS:")
        employed_count = worker_data['employed'].sum()
        unemployed_count = len(worker_data) - employed_count
        print(f"   Employed Workers: {employed_count} ({employed_count/len(worker_data)*100:.1f}%)")
        print(f"   Unemployed Workers: {unemployed_count} ({unemployed_count/len(worker_data)*100:.1f}%)")
        
        print(f"\n💰 FINANCIAL STATISTICS:")
        print(f"   Average Wealth: ${worker_data['wealth'].mean():,.0f}")
        print(f"   Median Wealth: ${worker_data['wealth'].median():,.0f}")
        print(f"   Wealth Std Dev: ${worker_data['wealth'].std():,.0f}")
        
        debt_workers = worker_data[worker_data['debt'] > 0]
        if len(debt_workers) > 0:
            print(f"\n💳 DEBT STATISTICS:")
            print(f"   Workers with Debt: {len(debt_workers)} ({len(debt_workers)/len(worker_data)*100:.1f}%)")
            print(f"   Average Debt: ${debt_workers['debt'].mean():,.0f}")
            print(f"   Median Debt: ${debt_workers['debt'].median():,.0f}")
            print(f"   Maximum Debt: ${debt_workers['debt'].max():,.0f}")
        
        if employed_count > 0:
            employed_data = worker_data[worker_data['employed'] == True]
            print(f"\n💼 WAGE STATISTICS (Employed Workers):")
            print(f"   Average Wage: ${employed_data['wage'].mean():,.0f}/week")
            print(f"   Median Wage: ${employed_data['wage'].median():,.0f}/week")
            print(f"   Wage Range: ${employed_data['wage'].min():,.0f} - ${employed_data['wage'].max():,.0f}")
        
        bankrupt_count = worker_data['is_bankrupt'].sum()
        print(f"\n🚨 CRISIS INDICATORS:")
        print(f"   Bankrupt Workers: {bankrupt_count} ({bankrupt_count/len(worker_data)*100:.1f}%)")
        print(f"   Workers with Unmet Needs: {(worker_data['unmet_needs'] > 0).sum()}")
        print(f"   Total Unmet Needs: ${worker_data['unmet_needs'].sum():,.0f}")
        print(f"   Average Financial Stress: {worker_data['financial_stress'].mean():.3f}")
        
        print("="*60)

def main():
    """Load the model and create worker dashboard."""
    # This needs to be run after a simulation
    print("Worker dashboard requires a completed simulation model.")
    print("Run this from within your simulation script or load a saved model.")

if __name__ == "__main__":
    main() 