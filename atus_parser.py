import pandas as pd
import numpy as np
from typing import List, Dict
import logging

class ATUSDataParser:
    """Parser for American Time Use Survey (ATUS) data to extract realistic work patterns."""
    
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.work_hours_data = None
        self.logger = logging.getLogger(__name__)
        
    def parse_atus_data(self) -> Dict:
        """Parse ATUS fixed-width data file and extract work-related variables."""
        try:
            # Define column specifications based on ATUS codebook
            # Key variables: TEHRUSLT (total usual hours), TEERN (weekly earnings), TEERNHRO (hours at rate)
            colspecs = [
                (0, 14),    # TUCASEID - Case ID
                (90, 93),   # TEHRUSL1 - Hours per week main job
                (93, 96),   # TEHRUSL2 - Hours per week other jobs  
                (96, 99),   # TEHRUSLT - Total hours usually worked per week
                (54, 62),   # TEERN - Total weekly earnings (2 implied decimals)
                (66, 74),   # TEERNH1O - Hourly rate main job (2 implied decimals)
                (78, 86),   # TEERNHRO - Hours usually work per week at this rate
                (198, 206), # TEHRFTPT - Work more than 35 hours (full/part time)
            ]
            
            column_names = [
                'case_id', 'hours_main_job', 'hours_other_jobs', 'total_hours_week',
                'weekly_earnings', 'hourly_rate', 'hours_at_rate', 'full_part_time'
            ]
            
            # Read fixed-width file
            df = pd.read_fwf(
                self.data_file_path,
                colspecs=colspecs,
                names=column_names,
                skiprows=1  # Skip header if present
            )
            
            # Clean and process data
            df = self._clean_atus_data(df)
            
            self.work_hours_data = df
            self.logger.info(f"Successfully parsed {len(df)} ATUS records")
            
            return self._calculate_work_statistics()
            
        except Exception as e:
            self.logger.error(f"Error parsing ATUS data: {e}")
            # Return default values if parsing fails
            return self._get_default_work_stats()
    
    def _clean_atus_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate ATUS data."""
        # Convert string fields to numeric, handling missing values
        numeric_cols = ['hours_main_job', 'hours_other_jobs', 'total_hours_week', 
                       'weekly_earnings', 'hourly_rate', 'hours_at_rate']
        
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Filter out invalid/missing work hours (code -1, -2, -3 = not in universe)
        df = df[df['total_hours_week'] > 0]
        df = df[df['total_hours_week'] <= 80]  # Remove extreme outliers
        
        # Calculate earnings per hour where possible
        df['calculated_hourly_wage'] = np.where(
            (df['total_hours_week'] > 0) & (df['weekly_earnings'] > 0),
            df['weekly_earnings'] / df['total_hours_week'] / 100,  # Remove 2 implied decimals
            np.nan
        )
        
        return df.dropna(subset=['total_hours_week'])
    
    def _calculate_work_statistics(self) -> Dict:
        """Calculate key work statistics from ATUS data."""
        if self.work_hours_data is None or len(self.work_hours_data) == 0:
            return self._get_default_work_stats()
        
        df = self.work_hours_data
        
        stats = {
            'mean_weekly_hours': df['total_hours_week'].mean(),
            'median_weekly_hours': df['total_hours_week'].median(),
            'std_weekly_hours': df['total_hours_week'].std(),
            'hours_distribution': df['total_hours_week'].tolist(),
            'mean_hourly_wage': df['calculated_hourly_wage'].mean() if 'calculated_hourly_wage' in df.columns else 15.0,
            'median_hourly_wage': df['calculated_hourly_wage'].median() if 'calculated_hourly_wage' in df.columns else 12.0,
            'total_records': len(df)
        }
        
        # Handle any NaN values
        for key, value in stats.items():
            if isinstance(value, float) and np.isnan(value):
                stats[key] = self._get_default_work_stats()[key]
        
        return stats
    
    def _get_default_work_stats(self) -> Dict:
        """Return default work statistics if ATUS parsing fails."""
        return {
            'mean_weekly_hours': 38.5,
            'median_weekly_hours': 40.0,
            'std_weekly_hours': 10.2,
            'hours_distribution': [32, 35, 37, 40, 40, 40, 42, 45, 48, 50] * 100,
            'mean_hourly_wage': 15.50,
            'median_hourly_wage': 12.75,
            'total_records': 1000
        }
    
    def sample_realistic_hours(self, n_workers: int) -> List[float]:
        """Sample realistic work hours for n_workers based on ATUS data."""
        if self.work_hours_data is None:
            # Use default distribution
            np.random.seed(42)  # For reproducibility
            return np.random.normal(38.5, 10.2, n_workers).clip(15, 60).tolist()
        
        # Sample from actual ATUS distribution
        return np.random.choice(
            self.work_hours_data['total_hours_week'].tolist(),
            size=n_workers,
            replace=True
        ).tolist()
    
    def get_wage_distribution(self) -> Dict:
        """Get wage distribution statistics."""
        if self.work_hours_data is None or 'calculated_hourly_wage' not in self.work_hours_data.columns:
            return {'wages': [10, 12, 15, 18, 22, 25, 30, 35] * 125}  # Default distribution
        
        valid_wages = self.work_hours_data['calculated_hourly_wage'].dropna()
        return {'wages': valid_wages.tolist()} 