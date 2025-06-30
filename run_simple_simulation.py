#!/usr/bin/env python3
"""
Enhanced Capitalist Economy Simulation with Skill-Based Workers and Firm Ownership
Uses Mesa's proven Gini coefficient calculation for accurate inequality measurement.
"""

import os
import sys
import time
import logging
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Simple replacements for Mesa classes
class Model:
    def __init__(self):
        pass

class DataCollector:
    def __init__(self, model_reporters=None):
        self.model_reporters = model_reporters or {}
        self.model_vars = []
    
    def collect(self, model):
        data = {}
        for name, func in self.model_reporters.items():
            try:
                if callable(func):
                    data[name] = func(model)
                else:
                    data[name] = getattr(model, func)
            except:
                data[name] = 0
        self.model_vars.append(data)
    
    def get_model_vars_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.model_vars)
import random

# Import our enhanced agents
from worker_agent_simple import SimpleWorkerAgent
from firm_agent_simple import SimpleFirmAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleCapitalistModel(Model):
    """Enhanced capitalist economy model with skill-based workers and firm ownership."""
    
    def __init__(self, num_workers, num_firms, num_owners=0):
        # Properly initialize Mesa Model
        super().__init__()
        
        self.num_workers = num_workers
        self.num_firms = num_firms
        self.num_owners = num_owners
        self.price_index = 1.0  # Inflation tracking
        self.inflation_rate = 0.02  # 2% annual inflation
        
        # Employment tracking for efficiency
        self.employed_workers = []
        self.unemployed_workers = []
        
        # Agent storage for Mesa compatibility
        self.worker_agents = []
        self.firm_agents = []
        
        # Create workers with skill levels and potential firm ownership
        for i in range(num_workers):
            worker = SimpleWorkerAgent(i, self)
            self.worker_agents.append(worker)
            self.unemployed_workers.append(worker)
        
        # Create firms with skill-based hiring
        for i in range(num_firms):
            firm = SimpleFirmAgent(num_workers + i, self)
            self.firm_agents.append(firm)
        
        # Enhanced data collection with inequality metrics
        self.datacollector = DataCollector(
            model_reporters={
                "Total Profit": lambda m: sum(f.profit for f in m.get_firms()),
                "Total Wages": lambda m: sum(w.wage for w in m.get_workers()),
                "Total Surplus Value": lambda m: sum(f.get_total_surplus_value() for f in m.get_firms()),
                "Wage Share": lambda m: m.get_wage_share(),
                "Unemployment Rate": lambda m: len(m.unemployed_workers) / m.num_workers,
                "Price Index": "price_index",
                "Total Tax Revenue": lambda m: sum(f.taxes_paid for f in m.get_firms()) + sum(w.total_taxes_paid for w in m.get_workers()),
                "Total Unmet Needs": lambda m: sum(w.get_unmet_needs() for w in m.get_workers()),
                "Average Financial Stress": lambda m: sum(w.calculate_financial_stress() for w in m.get_workers()) / len(m.get_workers()),
                "Total Worker Wealth": lambda m: sum(w.wealth for w in m.get_workers()),
                "Average Exploitation Rate": lambda m: m.get_avg_exploitation_rate(),
                # DEBT METRICS
                "Total Worker Debt": lambda m: sum(w.debt for w in m.get_workers()),
                "Average Debt per Worker": lambda m: sum(w.debt for w in m.get_workers()) / len(m.get_workers()),
                "Workers in Debt": lambda m: sum(1 for w in m.get_workers() if w.debt > 0),
                "Debt to Income Ratio": lambda m: m.get_avg_debt_to_income(),
                "Bankrupt Workers": lambda m: sum(1 for w in m.get_workers() if w.is_bankrupt),
                "Total Debt Payments": lambda m: sum(max(w.debt * 0.02, 20) if w.debt > 0 else 0 for w in m.get_workers()),
                # INEQUALITY & UNEMPLOYMENT METRICS
                "Gini Coefficient": lambda m: m.compute_gini(),
                "Long-term Unemployed": lambda m: sum(1 for w in m.unemployed_workers if w.weeks_unemployed > 12),
                "Long-term Unemployment Rate": lambda m: sum(1 for w in m.unemployed_workers if w.weeks_unemployed > 12) / m.num_workers,
                "Employed Workers": lambda m: len(m.employed_workers),
                "Net Worker Wealth": lambda m: sum(w.wealth - w.debt for w in m.get_workers()),
                # SKILL-BASED METRICS
                "High Skill Workers": lambda m: sum(1 for w in m.get_workers() if w.skill_level == "high"),
                "Medium Skill Workers": lambda m: sum(1 for w in m.get_workers() if w.skill_level == "medium"),
                "Low Skill Workers": lambda m: sum(1 for w in m.get_workers() if w.skill_level == "low"),
                "Firm Owners": lambda m: sum(1 for w in m.get_workers() if w.owns_firm),
                # DETAILED SKILL-BASED INCOME METRICS
                "High Skill Average Wage": lambda m: sum(w.wage for w in m.get_workers() if w.skill_level == "high" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "high" and w.is_employed)),
                "Medium Skill Average Wage": lambda m: sum(w.wage for w in m.get_workers() if w.skill_level == "medium" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "medium" and w.is_employed)),
                "Low Skill Average Wage": lambda m: sum(w.wage for w in m.get_workers() if w.skill_level == "low" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "low" and w.is_employed)),
                # REAL WAGES (INFLATION ADJUSTED)
                "Real Wage Total": lambda m: sum(w.wage for w in m.get_workers()) / m.price_index,
                "High Skill Real Wage": lambda m: (sum(w.wage for w in m.get_workers() if w.skill_level == "high" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "high" and w.is_employed))) / m.price_index,
                "Medium Skill Real Wage": lambda m: (sum(w.wage for w in m.get_workers() if w.skill_level == "medium" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "medium" and w.is_employed))) / m.price_index,
                "Low Skill Real Wage": lambda m: (sum(w.wage for w in m.get_workers() if w.skill_level == "low" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "low" and w.is_employed))) / m.price_index,
                # INFLATION RATE
                "Weekly Inflation Rate": lambda m: ((m.price_index / 1.0) ** (1/52) - 1) if hasattr(m, 'price_index') else 0,
                "Annual Inflation Rate": lambda m: (m.price_index - 1.0) if hasattr(m, 'price_index') else 0,
                # EXPLOITATION BY SKILL LEVEL
                "High Skill Exploitation": lambda m: sum(w.get_exploitation_rate() for w in m.get_workers() if w.skill_level == "high" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "high" and w.is_employed)),
                "Medium Skill Exploitation": lambda m: sum(w.get_exploitation_rate() for w in m.get_workers() if w.skill_level == "medium" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "medium" and w.is_employed)),
                "Low Skill Exploitation": lambda m: sum(w.get_exploitation_rate() for w in m.get_workers() if w.skill_level == "low" and w.is_employed) / max(1, sum(1 for w in m.get_workers() if w.skill_level == "low" and w.is_employed))
            }
        )
        
        # Collect initial data
        self.datacollector.collect(self)
        
        logger.info(f"Created enhanced model: {num_workers} workers, {num_firms} firms")
        
        # Count initial skill distribution
        skill_counts = {"high": 0, "medium": 0, "low": 0}
        firm_owners = 0
        for worker in self.get_workers():
            skill_counts[worker.skill_level] += 1
            if worker.owns_firm:
                firm_owners += 1
        
        logger.info(f"Skill distribution: High: {skill_counts['high']}, Medium: {skill_counts['medium']}, Low: {skill_counts['low']}")
        logger.info(f"Firm owners: {firm_owners} ({firm_owners/num_workers*100:.1f}%)")
    
    def step(self):
        """Execute one step of the model."""
        # Update inflation
        weekly_inflation = (1 + self.inflation_rate) ** (1/52) - 1
        self.price_index *= (1 + weekly_inflation + random.uniform(-0.001, 0.001))
        
        # Step all workers first
        for worker in self.worker_agents:
            worker.step()
        
        # Then step all firms
        for firm in self.firm_agents:
            firm.step()
        
        # Collect data
        self.datacollector.collect(self)
    
    def get_workers(self):
        """Get all worker agents."""
        return self.worker_agents
    
    def get_firms(self):
        """Get all firm agents."""
        return self.firm_agents
    
    def get_wage_share(self):
        """Calculate wage share of total output."""
        total_wages = sum(w.wage for w in self.get_workers())
        total_surplus = sum(f.get_total_surplus_value() for f in self.get_firms())
        total_output = total_wages + total_surplus
        
        if total_output > 0:
            return total_wages / total_output
        return 0
    
    def get_avg_exploitation_rate(self):
        """Calculate average exploitation rate across all employed workers."""
        employed_workers = [w for w in self.get_workers() if w.is_employed]
        if not employed_workers:
            return 0
        
        total_exploitation = 0
        for worker in employed_workers:
            value_produced = worker.get_productive_value()
            if value_produced > 0:
                exploitation_rate = 1 - (worker.wage / value_produced)
                total_exploitation += exploitation_rate
        
        return total_exploitation / len(employed_workers)
    
    def get_avg_debt_to_income(self):
        """Calculate average debt-to-income ratio."""
        employed_workers = [w for w in self.get_workers() if w.is_employed and w.wage > 0]
        if not employed_workers:
            return 0
        
        ratios = []
        for worker in employed_workers:
            ratio = worker.get_debt_to_income_ratio()
            if ratio != float('inf'):
                ratios.append(ratio)
        
        return sum(ratios) / len(ratios) if ratios else 0
    
    def compute_gini(self):
        """Compute Gini coefficient for wealth inequality."""
        workers_wealth = [worker.wealth for worker in self.worker_agents]
        x = sorted(workers_wealth)        
        n = len(x)
        B = sum(xi * (n - i) for i, xi in enumerate(x)) / (n * sum(x))
        return 1 + (1 / n) - 2 * B

    def get_unemployment_stats(self):
        """Get detailed unemployment statistics."""
        total_workers = len(self.get_workers())
        unemployed_count = len(self.unemployed_workers)
        employed_count = len(self.employed_workers)
        
        # Long-term unemployment (>12 weeks)
        long_term_unemployed = sum(1 for w in self.unemployed_workers if w.weeks_unemployed > 12)
        
        return {
            'total_workers': total_workers,
            'unemployed_count': unemployed_count,
            'employed_count': employed_count,
            'unemployment_rate': unemployed_count / total_workers if total_workers > 0 else 0,
            'long_term_unemployed': long_term_unemployed,
            'long_term_unemployment_rate': long_term_unemployed / total_workers if total_workers > 0 else 0
        }
    
    def get_model_data(self):
        """Get collected data."""
        return self.datacollector.get_model_vars_dataframe()

def main():
    print("============================================================")
    print("ENHANCED CAPITALIST ECONOMY WITH SKILL-BASED INEQUALITY")
    print("============================================================")
    
    # ============================================================
    # SIMULATION PARAMETERS  
    # ============================================================
    num_workers = 1500  # Number of workers in the economy
    num_firms = 30      # Number of firms
    num_steps = 260     # Simulation length in weeks (260 weeks = 5 years)
    
    print(f"Workers: {num_workers:,}")
    print(f"Firms: {num_firms}")
    print(f"Simulation Steps: {num_steps} weeks ({num_steps/52:.0f} years)")
    print(f"Features: Skill levels, firm ownership, realistic wage gaps")
    print("============================================================")
    
    # Create and run model
    start_time = time.time()
    
    model = SimpleCapitalistModel(num_workers=num_workers, num_firms=num_firms)
    
    # Progress tracking
    for step in range(num_steps):
        model.step()
        
        # Progress updates
        if (step + 1) % 26 == 0:  # Every quarter year
            elapsed = time.time() - start_time
            remaining_steps = num_steps - (step + 1)
            steps_per_second = (step + 1) / elapsed if elapsed > 0 else 1
            eta_seconds = remaining_steps / steps_per_second if steps_per_second > 0 else 0
            eta_minutes = eta_seconds / 60
            
            print(f"Progress: {step + 1}/{num_steps} ({(step + 1)/num_steps*100:.1f}%) - Step time: {elapsed/(step + 1):.3f}s - ETA: {eta_minutes:.1f}min")
    
    elapsed_time = time.time() - start_time
    print(f"\n✅ Simulation completed in {elapsed_time/60:.1f} minutes!")
    
    # Get results
    data = model.get_model_data()
    final_data = data.iloc[-1]
    
    print("\n" + "="*50)
    print("SIMULATION RESULTS")
    print("="*50)
    print(f"Final Unemployment Rate: {final_data['Unemployment Rate']*100:.1f}%")
    print(f"Long-term Unemployment Rate: {final_data['Long-term Unemployment Rate']*100:.1f}%")
    print(f"Employed Workers: {final_data['Employed Workers']:.0f}")
    print(f"Final Wage Share: {final_data['Wage Share']*100:.1f}%")
    print(f"Total Profit: ${final_data['Total Profit']:,.0f}")
    print(f"Total Wages: ${final_data['Total Wages']:,.0f}")
    print(f"Average Exploitation Rate: {final_data['Average Exploitation Rate']*100:.1f}%")
    print(f"Total Unmet Needs: ${final_data['Total Unmet Needs']:,.0f}")
    print(f"Price Index (Inflation): {final_data['Price Index']:.3f}")
    
    # INEQUALITY METRICS
    print(f"\n--- WEALTH INEQUALITY ---")
    print(f"Gini Coefficient: {final_data['Gini Coefficient']:.3f}")
    print(f"Total Worker Wealth: ${final_data['Total Worker Wealth']:,.0f}")
    print(f"Net Worker Wealth: ${final_data['Net Worker Wealth']:,.0f}")
    
    # SKILL-BASED METRICS
    print(f"\n--- SKILL DISTRIBUTION ---")
    print(f"High-skill Workers: {final_data['High Skill Workers']:.0f} ({final_data['High Skill Workers']/num_workers*100:.1f}%)")
    print(f"Medium-skill Workers: {final_data['Medium Skill Workers']:.0f} ({final_data['Medium Skill Workers']/num_workers*100:.1f}%)")
    print(f"Low-skill Workers: {final_data['Low Skill Workers']:.0f} ({final_data['Low Skill Workers']/num_workers*100:.1f}%)")
    print(f"Firm Owners: {final_data['Firm Owners']:.0f} ({final_data['Firm Owners']/num_workers*100:.1f}%)")
    
    # DEBT METRICS
    print(f"\n--- DEBT CRISIS INDICATORS ---")
    print(f"Total Worker Debt: ${final_data['Total Worker Debt']:,.0f}")
    print(f"Average Debt per Worker: ${final_data['Average Debt per Worker']:,.0f}")
    print(f"Workers in Debt: {final_data['Workers in Debt']:.0f} ({final_data['Workers in Debt']/num_workers*100:.1f}%)")
    print(f"Average Debt-to-Income Ratio: {final_data['Debt to Income Ratio']:.2f}x")
    print(f"Bankrupt Workers: {final_data['Bankrupt Workers']:.0f} ({final_data['Bankrupt Workers']/num_workers*100:.1f}%)")
    
    # Show available columns for debugging
    print(f"\nAvailable columns: {list(data.columns)}")
    
    # DEBUG: Check wealth distribution for Gini debugging
    print(f"\n--- WEALTH DISTRIBUTION DEBUG ---")
    workers = model.get_workers()
    net_wealth_values = [w.wealth - w.debt for w in workers]
    firm_owners_wealth = [w.wealth - w.debt for w in workers if w.owns_firm]
    
    print(f"Sample net wealth values (first 10): {sorted(net_wealth_values)[:10]}")
    print(f"Sample net wealth values (last 10): {sorted(net_wealth_values)[-10:]}")
    print(f"Firm owners wealth (first 10): {sorted(firm_owners_wealth)[:10] if firm_owners_wealth else 'None'}")
    print(f"Unique net wealth values: {len(set(net_wealth_values))}")
    print(f"Min net wealth: ${min(net_wealth_values):,.0f}")
    print(f"Max net wealth: ${max(net_wealth_values):,.0f}")
    print(f"Wealth range: ${max(net_wealth_values) - min(net_wealth_values):,.0f}")
    
    # Test Gini calculation manually
    test_gini = model.compute_gini()
    print(f"Mesa Gini calculation: {test_gini:.6f}")

    # Save data
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_simulation_results_{timestamp}.csv"
    data.to_csv(filename, index=False)

    print(f"\nData saved to: {filename}")
    
    print(f"\n🔍 Creating detailed worker dashboard...")
    
    # Create visualizations using existing dashboard system
    print(f"Run: python create_all_dashboards.py")
    print(f"to generate comprehensive visualizations of this simulation.")

if __name__ == "__main__":
    main() 