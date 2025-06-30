import random
# Simple replacement for Mesa Agent
class Agent:
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model

USE_MESA = False

class SimpleWorkerAgent(Agent):
    """Enhanced worker agent with skill levels, firm ownership, and debt mechanics."""
    
    def __init__(self, unique_id, model, work_hours=40):
        if USE_MESA:
            super().__init__(unique_id, model)
        else:
            self.unique_id = unique_id
            self.model = model
        
        # Set work hours first  
        self.work_hours = work_hours
        
        # Skill level affects wages and wealth accumulation
        self.skill_level = self._determine_skill_level()
        
        # Basic worker attributes
        self.work_hours = work_hours
        self.worked_overtime = 0
        self.wage = 0  # Current wage per hour
        self.is_employed = False
        self.employer = None
        
        # Enhanced financial attributes
        self.wealth = self._get_initial_wealth()
        self.debt = max(0, -self.wealth) if self.wealth < 0 else 0
        if self.debt > 0:
            self.wealth = 0  # If starting with debt, wealth is 0
        
        # Financial history
        self.total_wages_earned = 0
        self.total_taxes_paid = 0
        self.weeks_unemployed = 0
        self.financial_stress = 0  # 0-1 scale
        
        # Debt mechanics
        self.debt_capacity = random.uniform(5000, 15000)  # Max debt before bankruptcy
        self.interest_rate = random.uniform(0.10, 0.26)  # 10-26% annual interest
        self.is_bankrupt = False
        
        # Productivity and firm ownership potential
        self.productivity = self._get_productivity()
        self.owns_firm = self._determine_firm_ownership()
        
        # Basic needs (adjusted for skill level)
        base_needs = 500  # Base weekly needs
        skill_multiplier = {"low": 0.8, "medium": 1.0, "high": 1.3}
        self.basic_needs = base_needs * skill_multiplier[self.skill_level]
    
    def _determine_skill_level(self):
        """Determine worker skill level with realistic distribution."""
        rand = random.random()
        if rand < 0.65:  # 65% low-skill
            return "low"
        elif rand < 0.85:  # 20% medium-skill
            return "medium"
        else:  # 15% high-skill
            return "high"
    
    def _get_initial_wealth(self):
        """Set initial wealth based on skill level."""
        if self.skill_level == "high":
            return random.uniform(5000, 25000)  # High-skill starts wealthy
        elif self.skill_level == "medium":
            return random.uniform(1500, 8000)   # Medium-skill modest savings
        else:
            return random.uniform(0, 2000)   # Low-skill may start with nothing
    
    def _get_productivity(self):
        """Get productivity multiplier based on skill level."""
        if self.skill_level == "high":
            return random.uniform(1.3, 1.8)  # 30-80% more productive
        elif self.skill_level == "medium":
            return random.uniform(1.0, 1.4)  # 0-40% more productive
        else:
            return random.uniform(0.7, 1.2)  # 30% less to 20% more productive
    
    def _determine_firm_ownership(self):
        """Determine if worker owns part of a firm (higher for high-skill workers)."""
        ownership_chance = {"high": 0.15, "medium": 0.05, "low": 0.01}
        return random.random() < ownership_chance[self.skill_level]
    
    def get_debt_to_income_ratio(self):
        """Calculate debt-to-income ratio."""
        if self.wage == 0:
            return float('inf') if self.debt > 0 else 0
        annual_income = self.wage * 52
        return self.debt / annual_income if annual_income > 0 else float('inf')
    
    def get_productive_value(self):
        """Calculate total value produced by this worker."""
        base_value_per_hour = 25.0  # Base productivity value
        return self.work_hours * self.get_productivity() * base_value_per_hour
    
    def get_productivity(self):
        """Return the worker's productivity multiplier."""
        return self.productivity
    
    def get_exploitation_rate(self):
        """Calculate this worker's exploitation rate."""
        if self.wage == 0:
            return 0
        value_produced = self.get_productive_value()
        if value_produced > 0:
            return 1 - (self.wage / value_produced)
        return 0
    
    def get_real_wage(self):
        """Get inflation-adjusted wage."""
        if hasattr(self.model, 'price_index'):
            return self.wage / self.model.price_index
        return self.wage
    
    def get_tax_rate(self):
        """Get tax rate based on skill level (progressive taxation)."""
        if self.skill_level == "high":
            return random.uniform(0.20, 0.30)  # 20-30% for high earners
        elif self.skill_level == "medium":
            return random.uniform(0.12, 0.20)  # 12-20% for medium earners
        else:
            return random.uniform(0.05, 0.12)  # 5-12% for low earners
            
    
    def get_reservation_wage(self):
        """Get minimum wage this worker will accept based on skill level and desperation."""
        # Base reservation wage by skill level
        base_reservation = {
            "high": 20.0,    # $20/hour minimum for high-skill
            "medium": 12.0,  # $12/hour minimum for medium-skill
            "low": 8.0       # $8/hour minimum for low-skill
        }
        
        reservation_hourly = base_reservation[self.skill_level]
        
        # Desperation factor - unemployed workers accept lower wages
        if not self.is_employed and self.weeks_unemployed > 4:
            desperation_factor = min(0.7, 1 - (self.weeks_unemployed * 0.05))
            reservation_hourly *= desperation_factor
        
        # Debt desperation - workers in debt accept even lower wages
        if self.debt > 0:
            debt_desperation = max(0.6, 1 - (self.debt / self.debt_capacity * 0.4))
            reservation_hourly *= debt_desperation
        
        return reservation_hourly * self.work_hours  # Convert to weekly wage
    
    def work_for_firm(self, firm, wage_rate):
        """Work for a firm and receive wages."""
        if self.is_employed:
            return
        
        self.is_employed = True
        self.employer = firm
        self.wage = wage_rate
        self.weeks_unemployed = 0
        
        # Calculate value produced
        value_produced = self.get_productive_value()
        
        # Calculate gross pay
        gross_pay = self.wage * self.work_hours
        
        # Calculate and pay taxes
        tax_rate = self.get_tax_rate()
        taxes = gross_pay * tax_rate
        net_pay = gross_pay - taxes
        
        # Add to wealth
        self.wealth += net_pay
        self.total_wages_earned += gross_pay
        self.total_taxes_paid += taxes
        
        # Firm ownership dividends (if applicable)
        if self.owns_firm and hasattr(firm, 'profit') and firm.profit > 0:
            ownership_share = random.uniform(0.01, 0.05)  # 1-5% ownership
            dividend = firm.profit * ownership_share
            self.wealth += dividend
        
        return value_produced
    
    def lose_job(self):
        """Lose job and become unemployed."""
        self.is_employed = False
        self.employer = None
        self.wage = 0
    
    def handle_debt_mechanics(self):
        """Handle debt accumulation, interest, and bankruptcy."""
        if self.debt > 0:
            # Add weekly interest (annual rate / 52)
            weekly_interest = self.debt * (self.interest_rate / 52)
            self.debt += weekly_interest
            
            # Try to pay minimum debt service (2% of debt or $20, whichever is higher)
            min_payment = max(self.debt * 0.02, 20)
            
            if self.wealth >= min_payment:
                payment = min(min_payment, self.debt)
                self.wealth -= payment
                self.debt -= payment
            
            # Check for bankruptcy
            if self.debt > self.debt_capacity and self.get_unmet_needs() > self.basic_needs * 2:
                self.is_bankrupt = True
                self.debt = self.debt_capacity  # Cap debt at capacity
    
    def get_unmet_needs(self):
        """Calculate unmet basic needs."""
        affordable_needs = min(self.wealth, self.basic_needs)
        return self.basic_needs - affordable_needs
    
    def calculate_financial_stress(self):
        """Calculate financial stress level (0-1 scale)."""
        stress_factors = []
        
        # Unemployment stress
        if not self.is_employed:
            stress_factors.append(0.4)
        
        # Debt stress
        if self.debt > 0:
            debt_ratio = self.debt / self.debt_capacity
            stress_factors.append(debt_ratio * 0.3)
        
        # Unmet needs stress
        unmet_ratio = self.get_unmet_needs() / self.basic_needs
        stress_factors.append(min(unmet_ratio, 1.0) * 0.3)
        
        self.financial_stress = min(sum(stress_factors), 1.0)
        return self.financial_stress
    
    def step(self):
        """Execute one step of the worker's behavior."""
        # Calculate financial stress
        self.calculate_financial_stress()
        
        # Handle basic needs and debt
        if not self.is_employed:
            self.weeks_unemployed += 1
            
            # Pay for basic needs
            needs_cost = self.basic_needs
            if self.wealth >= needs_cost:
                self.wealth -= needs_cost
            else:
                # Go into debt to survive
                shortfall = needs_cost - self.wealth
                self.debt += shortfall
                self.wealth = 0
        else:
            # Pay for basic needs when employed
            needs_cost = self.basic_needs
            if self.wealth >= needs_cost:
                self.wealth -= needs_cost
        
        # Handle debt mechanics
        self.handle_debt_mechanics()
        
        # Wealth decay for unemployed workers (desperation effect)
        if not self.is_employed and self.wealth > 0:
            decay_rate = {"high": 0.02, "medium": 0.03, "low": 0.05}
            self.wealth *= (1 - decay_rate[self.skill_level])
        
        # Small chance of wealth growth for high-skill workers (investments)
        if self.skill_level == "high" and self.wealth > 10000:
            if random.random() < 0.3:  # 30% chance
                self.wealth *= random.uniform(1.001, 1.003)  # 0.1-0.3% weekly growth 