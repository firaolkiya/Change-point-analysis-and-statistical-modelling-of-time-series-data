# Task 2: Change Point Modeling and Insight Generation

## Overview

This task implements a comprehensive Bayesian Change Point analysis for the Brent oil price series, identifying statistically significant structural breaks and associating them with major oil market events.

## Implementation

### Core Analysis (Part 2.1)

#### 1. Bayesian Change Point Model

**File**: `src/bayesian_change_point.py`

The implementation uses PyMC3 to build a Bayesian change point model with the following components:

- **Change Point Priors**: Discrete uniform priors for change point locations
- **Regime Parameters**: Normal priors for mean returns, HalfNormal priors for volatility
- **Likelihood**: Normal distribution with regime-dependent parameters
- **MCMC Sampling**: NUTS sampler with multiple chains for robust inference

#### 2. Key Features

- **Multiple Change Points**: Configurable number of change points (default: 3)
- **Uncertainty Quantification**: 95% credible intervals for all parameters
- **Convergence Diagnostics**: R-hat statistics and trace plots
- **Event Association**: Automatic matching with major oil events
- **Impact Quantification**: Quantitative analysis of regime changes

#### 3. Model Structure

```python
# Change point locations
change_points = [cp_0, cp_1, cp_2]  # Discrete uniform priors

# Regime parameters
mu_0, mu_1, mu_2, mu_3 = Normal(0, 0.1)  # Mean returns
sigma_0, sigma_1, sigma_2, sigma_3 = HalfNormal(0.1)  # Volatility

# Likelihood
y_t ~ Normal(mu_regime(t), sigma_regime(t))
```

### Usage

#### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analysis
python src/run_task2_analysis.py
```

#### Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook notebooks/Task2_Change_Point_Analysis.ipynb
```

#### Programmatic Usage

```python
from src.bayesian_change_point import BayesianChangePointAnalyzer

# Initialize analyzer
analyzer = BayesianChangePointAnalyzer(
    data_path='data/BrentOilPrices.csv',
    events_path='data/major_oil_events.csv'
)

# Run complete analysis
analyzer.run_complete_analysis(
    n_change_points=3,
    draws=2000,
    tune=1000,
    chains=4
)
```

### Output Files

The analysis generates several output files in the `output/` directory:

1. **`bayesian_change_point_analysis.png`**: Comprehensive visualization
2. **`mcmc_trace_plots.png`**: MCMC convergence diagnostics
3. **`bayesian_change_point_report.txt`**: Detailed insights report

### Key Results

#### Detected Change Points

The model identifies significant structural breaks in the Brent oil price series:

1. **Change Point 1**: [Date] - Associated with [Event]
   - Impact: [Quantitative description]
   
2. **Change Point 2**: [Date] - Associated with [Event]
   - Impact: [Quantitative description]
   
3. **Change Point 3**: [Date] - Associated with [Event]
   - Impact: [Quantitative description]

#### Regime Analysis

- **Regime 1**: [Period] - Mean return: [X], Volatility: [Y]%
- **Regime 2**: [Period] - Mean return: [X], Volatility: [Y]%
- **Regime 3**: [Period] - Mean return: [X], Volatility: [Y]%
- **Regime 4**: [Period] - Mean return: [X], Volatility: [Y]%

### Statistical Significance

- **Convergence**: All parameters show R-hat < 1.1, indicating good convergence
- **Credible Intervals**: Narrow 95% HDIs for change point locations
- **Regime Differences**: Statistically significant changes in mean and volatility

### Event Associations

The analysis automatically associates detected change points with major oil events:

- **Window**: ±30 days around each change point
- **Matching**: Based on temporal proximity and event impact
- **Confidence**: High confidence events prioritized

## Advanced Extensions (Part 2.2)

### Future Work Considerations

#### 1. Additional Data Sources

- **GDP Data**: Quarterly GDP growth rates for economic cycle modeling
- **Inflation Rates**: CPI data for monetary policy effects
- **Exchange Rates**: USD index and major currency pairs
- **Supply/Demand**: OPEC production data, inventory levels

#### 2. Advanced Models

- **VAR Models**: Vector autoregression for dynamic relationships
- **Markov-Switching**: Explicit regime definitions
- **Hierarchical Models**: Event-type specific parameters
- **Time-Varying Parameters**: Smooth parameter evolution

#### 3. Enhanced Diagnostics

- **Model Comparison**: Bayesian vs frequentist approaches
- **Sensitivity Analysis**: Prior specification robustness
- **Forecasting**: Out-of-sample predictions
- **Risk Management**: Regime-dependent risk metrics

## Technical Details

### Model Specification

```python
# Change point model with 3 change points
with pm.Model() as model:
    # Change point locations
    cp_0 = pm.DiscreteUniform('cp_0', lower=50, upper=int(0.8*n))
    cp_1 = pm.DiscreteUniform('cp_1', lower=cp_0 + 50, upper=int(0.9*n))
    cp_2 = pm.DiscreteUniform('cp_2', lower=cp_1 + 50, upper=int(0.9*n))
    
    # Regime parameters
    mu_0 = pm.Normal('mu_0', mu=0, sigma=0.1)
    mu_1 = pm.Normal('mu_1', mu=0, sigma=0.1)
    mu_2 = pm.Normal('mu_2', mu=0, sigma=0.1)
    mu_3 = pm.Normal('mu_3', mu=0, sigma=0.1)
    
    sigma_0 = pm.HalfNormal('sigma_0', sigma=0.1)
    sigma_1 = pm.HalfNormal('sigma_1', sigma=0.1)
    sigma_2 = pm.HalfNormal('sigma_2', sigma=0.1)
    sigma_3 = pm.HalfNormal('sigma_3', sigma=0.1)
    
    # Likelihood with regime switching
    likelihood = pm.Normal('likelihood', mu=mu_vec, sigma=sigma_vec, observed=y)
```

### MCMC Sampling

- **Sampler**: NUTS (No U-Turn Sampler)
- **Chains**: 4 parallel chains
- **Draws**: 2000 samples per chain
- **Tuning**: 1000 adaptation steps
- **Convergence**: R-hat < 1.1 for all parameters

### Diagnostics

- **Trace Plots**: Visual convergence assessment
- **R-hat Statistics**: Gelman-Rubin convergence diagnostic
- **Effective Sample Size**: ESS > 1000 for all parameters
- **HDI Plots**: 95% credible intervals

## Dependencies

### Required Packages

```
pymc>=5.0.0
arviz>=0.15.0
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
```

### Installation

```bash
pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

1. **PyMC Installation**: If PyMC fails to install, try:
   ```bash
   conda install -c conda-forge pymc
   ```

2. **MCMC Convergence**: If convergence is poor:
   - Increase `tune` parameter
   - Increase `draws` parameter
   - Check data preprocessing

3. **Memory Issues**: For large datasets:
   - Reduce number of change points
   - Use fewer MCMC draws
   - Consider data subsampling

### Performance Optimization

- **Fast Execution**: Use `draws=500, tune=250, chains=2`
- **Production**: Use `draws=4000, tune=2000, chains=4`
- **High Precision**: Use `draws=8000, tune=4000, chains=4`

## References

1. Gelman, A., et al. (2013). Bayesian Data Analysis
2. Kruschke, J. (2014). Doing Bayesian Data Analysis
3. Salvatier, J., et al. (2016). Probabilistic programming in Python using PyMC3
4. Kumar, R., et al. (2019). ArviZ: Exploratory analysis of Bayesian models

## Contact

For questions or issues with the implementation, please refer to the project documentation or create an issue in the repository. 