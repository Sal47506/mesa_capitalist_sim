"""
Simple Firm Agent for Capitalist Economy Simulation
Enhanced to pay different wages based on worker skill levels.
"""

# Simple replacement for Mesa Agent
class Agent:
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model

USE_MESA = False

import random
import numpy as np

class SimpleFirmAgent(Agent):
    """A firm agent that hires workers and extracts surplus value, with skill-based hiring."""
    
    def __init__(self, unique_id, model):
        if USE_MESA:
            super().__init__(unique_id, model)
        else:
            self.unique_id = unique_id
            self.model = model
        
        # Firm characteristics
        self.capital = random.uniform(50000, 200000)  # Starting capital
        self.profit = 0
        self.total_surplus_value = 0
        self.wages_paid = 0
        self.taxes_paid = 0
        
        # Employment - track workers by skill level
        self.workers = []
        self.max_workers = random.randint(30, 80)  # Firm size
        
        # Skill preferences for hiring
        self.preferred_skill_mix = self._determine_skill_preferences()
        
        # Wage rates by skill level
        self.wage_rates = {
            "high": random.uniform(25, 45),    # $25-45/hour for high-skill
            "medium": random.uniform(15, 25),  # $15-25/hour for medium-skill  
            "low": random.uniform(8, 18)       # $8-18/hour for low-skill
        }
        
        # Tax rate for firms
        self.tax_rate = random.uniform(0.20, 0.35)  # 20-35% corporate tax
        
        # Surplus value extraction
        self.wage_share = random.uniform(0.65, 0.75)  # Workers get 65-75%
        self.surplus_value_rate = 1 - self.wage_share
        
        # Firm parameters
        self.productivity_factor = random.uniform(0.9, 1.1)
        self.base_wage_rate = random.uniform(12.0, 20.0)
        
        # Business cycle
        self.demand_multiplier = random.uniform(0.9, 1.1)
        
        # Hiring parameters
        self.hiring_aggressiveness = random.uniform(0.4, 0.6)
        self.firing_threshold = random.uniform(0.1, 0.2)
        

    def get_current_skill_mix(self):
        """Get current distribution of worker skills."""
        if not self.workers:
            return {"high": 0, "medium": 0, "low": 0}
        
        skill_counts = {"high": 0, "medium": 0, "low": 0}
        for worker in self.workers:
            skill_counts[worker.skill_level] += 1
        
        total = len(self.workers)
        return {skill: count/total for skill, count in skill_counts.items()}

    def _determine_skill_preferences(self):
        """Determine what skill mix this firm prefers."""
        preferences = {
            "high": random.uniform(0.1, 0.3),
            "medium": random.uniform(0.2, 0.4), 
            "low": random.uniform(0.4, 0.7)
        }
        # Normalize to sum to 1
        total = sum(preferences.values())
        return {skill: count/total for skill, count in preferences.items()}
    
    def should_hire_worker(self, worker):
        """Determine if firm should hire this worker based on skill needs."""
        if worker not in self.workers:
            if len(self.workers) >= self.max_workers:
                return False
            
            # Check if we need this skill level
            current_mix = self.get_current_skill_mix()
            preferred_count = self.preferred_skill_mix[worker.skill_level]
            current_count = current_mix[worker.skill_level]
            
            # More likely to hire if we're below preferred skill mix
            if current_count < preferred_count:
                hire_probability = 0.8  # High chance if we need this skill
            else:
                hire_probability = 0.3  # Lower chance if we have enough
            
            # Adjust for firm profitability
            if self.profit > 0:
                hire_probability *= 1.5  # More likely to hire if profitable
            elif self.profit < -1000:
                hire_probability *= 0.3  # Less likely if losing money
            hire = random.random() < hire_probability
            if(hire):
                self.hire_worker(worker, self.calculate_worker_wage_offer(worker))
                return True
            else:
                return False
        return False
    
    def calculate_worker_wage_offer(self, worker):
        """Calculate wage offer based on worker skill level and firm needs."""
        base_hourly_rate = self.wage_rates[worker.skill_level]
        
        # Adjust based on current needs
        current_mix = self.get_current_skill_mix()
        if current_mix[worker.skill_level] < self.preferred_skill_mix[worker.skill_level]:
            # We need this skill - offer higher wage
            wage_multiplier = random.uniform(1.1, 1.3)
        else:
            # We have enough of this skill - offer lower wage
            wage_multiplier = random.uniform(0.8, 1.0)
        
        final_hourly_rate = base_hourly_rate * wage_multiplier
        weekly_wage = final_hourly_rate * worker.work_hours
        
        return max(weekly_wage, worker.get_reservation_wage())
    
    def step(self):
        """Execute one step of the firm's behavior."""
        # Reset profit calculation
        self.total_surplus_value = 0
        self.wages_paid = 0
        
        # Produce with current workers
        total_production_value = 0
        for worker in self.workers:
            # Each worker produces value based on their skill level
            worker_value = worker.get_productive_value()
            total_production_value += worker_value
            
            # Pay worker their wage (surplus value extraction happens here)
            wage_offer = self.calculate_worker_wage_offer(worker)
            worker.work_for_firm(self, wage_offer / worker.work_hours)  # Convert to hourly
            self.wages_paid += worker.wage
        
        # Calculate surplus value (value produced - wages paid)
        self.total_surplus_value = total_production_value - self.wages_paid
        
        # Firm profit before taxes
        gross_profit = self.total_surplus_value
        
        # Pay corporate taxes
        self.taxes_paid = max(0, gross_profit * self.tax_rate)
        self.profit = gross_profit - self.taxes_paid
        
        # Update capital
        self.capital += self.profit
        
        # Hiring and firing decisions
        self._make_employment_decisions()
    
    def _make_employment_decisions(self):
        """Make decisions about hiring and firing workers."""
        # Firing decision (less aggressive than before)
        if self.profit < -500 and len(self.workers) > 5:
            # Fire workers if losing money, but less aggressively
            fire_probability = 0.45  # 45% chance to fire someone
            if random.random() < fire_probability:
                worker_to_fire = random.choice(self.workers)
                self.fire_worker(worker_to_fire)
        
        # Hiring decision
        if len(self.workers) < self.max_workers:
            # Look for workers to hire
            unemployed_workers = [w for w in self.model.unemployed_workers]
            if unemployed_workers:
                # Try to hire up to 3 workers per step
                for _ in range(min(3, len(unemployed_workers))):
                    if len(self.workers) >= self.max_workers:
                        break
                    
                    potential_worker = random.choice(unemployed_workers)
                    if self.should_hire_worker(potential_worker):
                        wage_offer = self.calculate_worker_wage_offer(potential_worker)
                        if wage_offer >= potential_worker.get_reservation_wage():
                            self.hire_worker(potential_worker, wage_offer / potential_worker.work_hours)
                            unemployed_workers.remove(potential_worker)
    
    def hire_worker(self, worker, hourly_wage):
        """Hire a worker at the specified hourly wage."""
        # Add worker to firm's worker list
        self.workers.append(worker)
        worker.work_for_firm(self, hourly_wage)
        
        # Update model employment tracking
        if worker in self.model.unemployed_workers:
            self.model.unemployed_workers.remove(worker)
        if worker not in self.model.employed_workers:
            self.model.employed_workers.append(worker)
        return True
    
    def fire_worker(self, worker):
        """Fire a worker."""
        if worker in self.workers:
            self.workers.remove(worker)
            worker.lose_job()
            
            # Update model employment tracking  
            if worker in self.model.employed_workers:
                self.model.employed_workers.remove(worker)
            if worker not in self.model.unemployed_workers:
                self.model.unemployed_workers.append(worker)
            
            return True
        return False
    
    def get_total_surplus_value(self):
        """Get total surplus value extracted this period."""
        return self.total_surplus_value
    
    def get_exploitation_rate(self):
        """Calculate exploitation rate (surplus value / total value produced)."""
        total_value = self.total_surplus_value + self.wages_paid
        if total_value > 0:
            return self.total_surplus_value / total_value
        return 0
    
    def get_wage_share_of_output(self):
        """Get wage share of total output."""
        if not self.workers:
            return 0
        
        total_value = sum(worker.get_value_produced() * self.productivity_factor 
                         for worker in self.workers)
        total_wages = sum(worker.wage + worker.taxes_paid for worker in self.workers)
        
        return total_wages / total_value if total_value > 0 else 0 