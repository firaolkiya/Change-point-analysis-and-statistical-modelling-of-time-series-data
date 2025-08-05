"""
Time Series Analysis for Brent Oil Prices
Birhan Energies - Data Science Project

This script performs comprehensive time series analysis including:
- Data preprocessing and validation
- Stationarity tests
- Volatility analysis
- Change point detection
- Basic event impact analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class BrentOilAnalyzer:
    """Comprehensive analyzer for Brent oil price time series data"""
    
    def __init__(self, data_path):
        """Initialize with data path"""
        self.data_path = data_path
        self.df = None
        self.df_processed = None
        self.events_df = None
        self.returns = None
        self.log_returns = None
        
    def load_data(self):
        """Load and preprocess the Brent oil price data"""
        print("Loading Brent oil price data...")
        
        # Load main data
        self.df = pd.read_csv(self.data_path)
        print(f"Raw data shape: {self.df.shape}")
        
        # Load events data
        try:
            self.events_df = pd.read_csv('data/major_oil_events.csv')
            self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
            print(f"Events data shape: {self.events_df.shape}")
        except FileNotFoundError:
            print("Events data not found, proceeding without events")
            self.events_df = None
            
        return self
    
    def preprocess_data(self):
        """Preprocess the Brent oil price data"""
        print("Preprocessing data...")
        
        # Create a copy to avoid modifying original
        df_clean = self.df.copy()
        
        # Convert date column to datetime
        def parse_date(date_str):
            try:
                # Try different date formats
                for fmt in ['%d-%b-%y', '%d-%b-%Y', '%b %d, %Y', '%Y-%m-%d']:
                    try:
                        return pd.to_datetime(date_str, format=fmt)
                    except:
                        continue
                # If none work, use pandas default parser
                return pd.to_datetime(date_str)
            except:
                return pd.NaT
        
        df_clean['Date'] = df_clean['Date'].apply(parse_date)
        
        # Remove rows with invalid dates
        df_clean = df_clean.dropna(subset=['Date'])
        
        # Sort by date
        df_clean = df_clean.sort_values('Date').reset_index(drop=True)
        
        # Convert price to numeric, handling any non-numeric values
        df_clean['Price'] = pd.to_numeric(df_clean['Price'], errors='coerce')
        
        # Remove rows with missing prices
        df_clean = df_clean.dropna(subset=['Price'])
        
        # Set date as index
        df_clean = df_clean.set_index('Date')
        
        self.df_processed = df_clean
        
        # Calculate returns
        self.returns = self.df_processed['Price'].pct_change().dropna()
        self.log_returns = np.log(self.df_processed['Price'] / self.df_processed['Price'].shift(1)).dropna()
        
        print(f"Processed data shape: {self.df_processed.shape}")
        print(f"Date range: {self.df_processed.index.min()} to {self.df_processed.index.max()}")
        
        return self
    
    def basic_statistics(self):
        """Calculate and display basic statistics"""
        print("\n=== BASIC STATISTICS ===")
        
        # Price statistics
        print(f"Price Statistics:")
        print(f"  Mean: ${self.df_processed['Price'].mean():.2f}")
        print(f"  Median: ${self.df_processed['Price'].median():.2f}")
        print(f"  Min: ${self.df_processed['Price'].min():.2f}")
        print(f"  Max: ${self.df_processed['Price'].max():.2f}")
        print(f"  Std: ${self.df_processed['Price'].std():.2f}")
        print(f"  Skewness: {self.df_processed['Price'].skew():.4f}")
        print(f"  Kurtosis: {self.df_processed['Price'].kurtosis():.4f}")
        
        # Return statistics
        print(f"\nReturn Statistics:")
        print(f"  Mean daily return: {self.returns.mean():.6f} ({self.returns.mean()*100:.4f}%)")
        print(f"  Daily return std: {self.returns.std():.6f} ({self.returns.std()*100:.4f}%)")
        print(f"  Skewness: {self.returns.skew():.4f}")
        print(f"  Kurtosis: {self.returns.kurtosis():.4f}")
        
        return self
    
    def test_stationarity(self, series, title):
        """Perform stationarity tests on time series data"""
        from statsmodels.tsa.stattools import adfuller, kpss
        
        print(f"\n=== STATIONARITY TESTS: {title} ===")
        
        # Augmented Dickey-Fuller test
        adf_result = adfuller(series.dropna())
        print(f"\nAugmented Dickey-Fuller Test:")
        print(f"  ADF Statistic: {adf_result[0]:.6f}")
        print(f"  p-value: {adf_result[1]:.6f}")
        print(f"  Critical values:")
        for key, value in adf_result[4].items():
            print(f"    {key}: {value:.3f}")
        
        if adf_result[1] <= 0.05:
            print("  Result: Series is STATIONARY (reject null hypothesis)")
        else:
            print("  Result: Series is NON-STATIONARY (fail to reject null hypothesis)")
        
        # KPSS test
        try:
            kpss_result = kpss(series.dropna())
            print(f"\nKPSS Test:")
            print(f"  KPSS Statistic: {kpss_result[0]:.6f}")
            print(f"  p-value: {kpss_result[1]:.6f}")
            print(f"  Critical values:")
            for key, value in kpss_result[3].items():
                print(f"    {key}: {value:.3f}")
            
            if kpss_result[1] >= 0.05:
                print("  Result: Series is STATIONARY (fail to reject null hypothesis)")
            else:
                print("  Result: Series is NON-STATIONARY (reject null hypothesis)")
        except:
            print("  KPSS test could not be performed")
        
        return self
    
    def plot_time_series(self):
        """Create comprehensive time series plots"""
        print("Creating time series visualizations...")
        
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        
        # Plot 1: Price over time
        axes[0].plot(self.df_processed.index, self.df_processed['Price'], linewidth=0.8)
        axes[0].set_title('Brent Oil Prices Over Time (1987-2022)', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Price (USD/barrel)')
        axes[0].grid(True, alpha=0.3)
        
        # Add events if available
        if self.events_df is not None:
            for _, event in self.events_df.iterrows():
                if event['Date'] in self.df_processed.index:
                    color = 'red' if event['Impact_Direction'] == 'Negative' else 'green'
                    axes[0].axvline(x=event['Date'], color=color, linestyle='--', alpha=0.5)
        
        # Plot 2: Price changes (returns)
        axes[1].plot(self.returns.index, self.returns, linewidth=0.8, alpha=0.7)
        axes[1].set_title('Daily Price Changes (Returns)', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Daily Return')
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Volatility (rolling standard deviation)
        volatility = self.returns.rolling(window=30).std()
        axes[2].plot(volatility.index, volatility, linewidth=0.8, alpha=0.7)
        axes[2].set_title('30-Day Rolling Volatility', fontsize=14, fontweight='bold')
        axes[2].set_ylabel('Volatility')
        axes[2].set_xlabel('Date')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../output/time_series_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return self
    
    def volatility_analysis(self):
        """Analyze volatility clustering and patterns"""
        print("Analyzing volatility patterns...")
        
        # Calculate volatility measures
        rolling_vol = self.returns.rolling(window=30).std()
        abs_returns = abs(self.returns.dropna())
        
        # Test for volatility clustering
        acf_abs = pd.Series([abs_returns.autocorr(lag=i) for i in range(1, 21)])
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Returns with volatility clustering
        axes[0,0].plot(self.returns.index, self.returns, alpha=0.7, linewidth=0.8)
        axes[0,0].set_title('Daily Returns with Volatility Clustering', fontsize=12, fontweight='bold')
        axes[0,0].set_ylabel('Daily Return')
        axes[0,0].grid(True, alpha=0.3)
        
        # Plot 2: Absolute returns
        axes[0,1].plot(self.returns.index, abs_returns, alpha=0.7, linewidth=0.8)
        axes[0,1].set_title('Absolute Returns (Volatility Proxy)', fontsize=12, fontweight='bold')
        axes[0,1].set_ylabel('Absolute Return')
        axes[0,1].grid(True, alpha=0.3)
        
        # Plot 3: Rolling volatility
        axes[1,0].plot(rolling_vol.index, rolling_vol, alpha=0.7, linewidth=0.8)
        axes[1,0].set_title('30-Day Rolling Volatility', fontsize=12, fontweight='bold')
        axes[1,0].set_ylabel('Volatility')
        axes[1,0].grid(True, alpha=0.3)
        
        # Plot 4: Autocorrelation of absolute returns
        axes[1,1].bar(range(1, 21), acf_abs, alpha=0.7)
        axes[1,1].set_title('Autocorrelation of Absolute Returns', fontsize=12, fontweight='bold')
        axes[1,1].set_xlabel('Lag')
        axes[1,1].set_ylabel('Autocorrelation')
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../output/volatility_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\n=== VOLATILITY CLUSTERING ANALYSIS ===")
        print(f"First-order autocorrelation of absolute returns: {acf_abs.iloc[0]:.4f}")
        print(f"This indicates {'strong' if abs(acf_abs.iloc[0]) > 0.1 else 'weak'} volatility clustering")
        
        return self
    
    def change_point_analysis(self):
        """Perform change point detection"""
        print("Performing change point analysis...")
        
        try:
            import ruptures
            
            # Use log returns for better statistical properties
            log_returns = self.log_returns.dropna()
            
            # Method 1: Pelt algorithm for mean changes
            model_pelt = ruptures.Pelt(model="rbf", min_size=30, jump=5)
            model_pelt.fit(log_returns.values)
            change_points_pelt = model_pelt.predict(pen=10)
            
            # Method 2: Binary segmentation for variance changes
            model_binseg = ruptures.Binseg(model="normal", min_size=30, jump=5)
            model_binseg.fit(log_returns.values)
            change_points_binseg = model_binseg.predict(n_bkps=10)
            
            # Visualize change points
            fig, axes = plt.subplots(2, 1, figsize=(15, 12))
            
            # Plot 1: Pelt algorithm results
            axes[0].plot(log_returns.index, log_returns.values, linewidth=0.8, alpha=0.7)
            for cp in change_points_pelt[:-1]:  # Exclude last point (end of series)
                axes[0].axvline(x=log_returns.index[cp], color='red', linestyle='--', alpha=0.7)
            axes[0].set_title('Change Points Detection - Pelt Algorithm (Mean Changes)', fontsize=14, fontweight='bold')
            axes[0].set_ylabel('Log Returns')
            axes[0].grid(True, alpha=0.3)
            
            # Plot 2: Binary segmentation results
            axes[1].plot(log_returns.index, log_returns.values, linewidth=0.8, alpha=0.7)
            for cp in change_points_binseg[:-1]:  # Exclude last point (end of series)
                axes[1].axvline(x=log_returns.index[cp], color='green', linestyle='--', alpha=0.7)
            axes[1].set_title('Change Points Detection - Binary Segmentation (Variance Changes)', fontsize=14, fontweight='bold')
            axes[1].set_ylabel('Log Returns')
            axes[1].set_xlabel('Date')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('../output/change_point_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # Analyze change points
            print("\n=== CHANGE POINT ANALYSIS RESULTS ===")
            print(f"Pelt Algorithm (Mean Changes) - {len(change_points_pelt)-1} change points:")
            for i, cp in enumerate(change_points_pelt[:-1]):
                date = log_returns.index[cp]
                print(f"  {i+1}. {date.strftime('%Y-%m-%d')}")
            
            print(f"\nBinary Segmentation (Variance Changes) - {len(change_points_binseg)-1} change points:")
            for i, cp in enumerate(change_points_binseg[:-1]):
                date = log_returns.index[cp]
                print(f"  {i+1}. {date.strftime('%Y-%m-%d')}")
            
            return change_points_pelt, change_points_binseg
            
        except ImportError:
            print("Ruptures library not available. Using simple rolling window analysis...")
            
            # Simple rolling window analysis
            window_size = 252  # One year
            rolling_mean = log_returns.rolling(window=window_size).mean()
            rolling_std = log_returns.rolling(window=window_size).std()
            
            plt.figure(figsize=(15, 10))
            
            plt.subplot(2, 1, 1)
            plt.plot(log_returns.index, log_returns.values, alpha=0.5, linewidth=0.8, label='Log Returns')
            plt.plot(rolling_mean.index, rolling_mean.values, linewidth=2, label=f'{window_size}-day Rolling Mean')
            plt.title('Rolling Mean Analysis - Structural Changes', fontsize=14, fontweight='bold')
            plt.ylabel('Log Returns')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.subplot(2, 1, 2)
            plt.plot(log_returns.index, log_returns.values, alpha=0.5, linewidth=0.8, label='Log Returns')
            plt.plot(rolling_std.index, rolling_std.values, linewidth=2, label=f'{window_size}-day Rolling Std')
            plt.title('Rolling Volatility Analysis - Structural Changes', fontsize=14, fontweight='bold')
            plt.ylabel('Log Returns')
            plt.xlabel('Date')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('../output/rolling_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            return None, None
    
    def event_impact_analysis(self):
        """Analyze the impact of major events on oil prices"""
        if self.events_df is None:
            print("No events data available for impact analysis")
            return self
        
        print("Analyzing event impacts...")
        
        # Calculate event impacts
        event_impacts = []
        
        for _, event in self.events_df.iterrows():
            event_date = event['Date']
            
            # Find the closest trading day
            if event_date in self.df_processed.index:
                # Calculate pre and post event returns
                pre_window = 5  # 5 days before
                post_window = 5  # 5 days after
                
                event_idx = self.df_processed.index.get_loc(event_date)
                
                if event_idx >= pre_window and event_idx + post_window < len(self.df_processed):
                    pre_prices = self.df_processed['Price'].iloc[event_idx-pre_window:event_idx]
                    post_prices = self.df_processed['Price'].iloc[event_idx:event_idx+post_window]
                    
                    pre_avg = pre_prices.mean()
                    post_avg = post_prices.mean()
                    
                    impact = (post_avg - pre_avg) / pre_avg * 100
                    
                    event_impacts.append({
                        'Date': event_date,
                        'Event': event['Event_Description'],
                        'Category': event['Event_Category'],
                        'Expected_Impact': event['Impact_Direction'],
                        'Actual_Impact_Pct': impact,
                        'Pre_Avg_Price': pre_avg,
                        'Post_Avg_Price': post_avg
                    })
        
        if event_impacts:
            impacts_df = pd.DataFrame(event_impacts)
            
            # Plot event impacts
            plt.figure(figsize=(15, 8))
            
            colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
            impact_colors = [colors.get(exp, 'blue') for exp in impacts_df['Expected_Impact']]
            
            plt.bar(range(len(impacts_df)), impacts_df['Actual_Impact_Pct'], 
                   color=impact_colors, alpha=0.7)
            plt.title('Event Impact Analysis - 5-Day Price Changes', fontsize=14, fontweight='bold')
            plt.xlabel('Events')
            plt.ylabel('Price Change (%)')
            plt.xticks(range(len(impacts_df)), [f"{d.strftime('%Y-%m')}\n{c[:20]}..." 
                       for d, c in zip(impacts_df['Date'], impacts_df['Event'])], 
                       rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('../output/event_impacts.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # Summary statistics
            print("\n=== EVENT IMPACT SUMMARY ===")
            print(f"Total events analyzed: {len(impacts_df)}")
            print(f"Average impact: {impacts_df['Actual_Impact_Pct'].mean():.2f}%")
            print(f"Impact standard deviation: {impacts_df['Actual_Impact_Pct'].std():.2f}%")
            
            # By category
            print("\nImpact by Event Category:")
            for category in impacts_df['Category'].unique():
                cat_impacts = impacts_df[impacts_df['Category'] == category]['Actual_Impact_Pct']
                print(f"  {category}: {cat_impacts.mean():.2f}% (n={len(cat_impacts)})")
        
        return self
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting comprehensive Brent oil price analysis...")
        
        (self.load_data()
         .preprocess_data()
         .basic_statistics()
         .test_stationarity(self.df_processed['Price'], 'Brent Oil Prices')
         .test_stationarity(self.returns, 'Daily Returns')
         .plot_time_series()
         .volatility_analysis()
         .change_point_analysis()
         .event_impact_analysis())
        
        print("\n=== ANALYSIS COMPLETE ===")
        print("Key findings:")
        print("1. Brent oil prices show non-stationary behavior with clear trends")
        print("2. Daily returns are more suitable for statistical analysis")
        print("3. Strong evidence of volatility clustering")
        print("4. Multiple structural breaks identified over the period")
        print("5. Events show varying impacts on price movements")
        
        return self


def main():
    """Main function to run the analysis"""
    
    # Create output directory
    import os
    os.makedirs('../output', exist_ok=True)
    
    # Initialize analyzer
    analyzer = BrentOilAnalyzer('../data/BrentOilPrices.csv')
    
    # Run complete analysis
    analyzer.run_complete_analysis()
    
    print("\nAnalysis complete! Check the output directory for saved plots.")


if __name__ == "__main__":
    main() 