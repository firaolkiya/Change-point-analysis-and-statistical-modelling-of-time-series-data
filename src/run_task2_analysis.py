#!/usr/bin/env python3
"""
Task 2: Change Point Modeling and Insight Generation
Runner Script

This script runs the complete Bayesian Change Point analysis for Task 2.
It includes proper error handling and fallback options if PyMC3 is not available.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if required dependencies are available"""
    print("Checking dependencies...")
    
    # Check PyMC3
    try:
        import pymc as pm
        import arviz as az
        print("✓ PyMC and ArviZ available")
        return True
    except ImportError:
        print("✗ PyMC not available")
        print("  To install: pip install pymc arviz")
        return False

def run_basic_analysis():
    """Run basic analysis without PyMC3"""
    print("\n" + "="*60)
    print("RUNNING BASIC CHANGE POINT ANALYSIS")
    print("="*60)
    
    # Import the basic analyzer
    from time_series_analysis import BrentOilAnalyzer
    
    # Initialize analyzer
    analyzer = BrentOilAnalyzer('data/BrentOilPrices.csv')
    
    # Run basic analysis
    analyzer.load_data()
    analyzer.preprocess_data()
    analyzer.basic_statistics()
    analyzer.plot_time_series()
    analyzer.volatility_analysis()
    analyzer.change_point_analysis()
    
    print("\n✓ Basic analysis completed!")
    print("Check the output/ directory for results")

def run_bayesian_analysis():
    """Run full Bayesian analysis with PyMC3"""
    print("\n" + "="*60)
    print("RUNNING BAYESIAN CHANGE POINT ANALYSIS")
    print("="*60)
    
    # Import the Bayesian analyzer
    from bayesian_change_point import BayesianChangePointAnalyzer
    
    # Initialize analyzer
    analyzer = BayesianChangePointAnalyzer(
        data_path='data/BrentOilPrices.csv',
        events_path='data/major_oil_events.csv'
    )
    
    # Run complete analysis
    analyzer.run_complete_analysis(
        n_change_points=3,
        draws=1000,  # Reduced for faster execution
        tune=500,
        chains=2
    )
    
    print("\n✓ Bayesian analysis completed!")
    print("Check the output/ directory for results")

def main():
    """Main function"""
    print("Task 2: Change Point Modeling and Insight Generation")
    print("="*60)
    
    # Check if output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')
        print("Created output/ directory")
    
    # Check dependencies
    pymc_available = check_dependencies()
    
    if pymc_available:
        # Run full Bayesian analysis
        run_bayesian_analysis()
    else:
        # Run basic analysis as fallback
        print("\nPyMC3 not available. Running basic analysis instead...")
        run_basic_analysis()
        
        print("\n" + "="*60)
        print("NEXT STEPS")
        print("="*60)
        print("To run the full Bayesian analysis:")
        print("1. Install PyMC3: pip install pymc arviz")
        print("2. Run this script again")
        print("3. Or run the Jupyter notebook: notebooks/Task2_Change_Point_Analysis.ipynb")

if __name__ == "__main__":
    main() 