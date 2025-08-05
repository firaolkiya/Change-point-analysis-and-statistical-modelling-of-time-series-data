# Brent Oil Price Analysis Dashboard
## Interactive Dashboard for Brent Oil Price Analysis - Task 3

### Project Overview

This project provides a comprehensive analysis of Brent oil price trends, events, and change points through an interactive web dashboard. The analysis focuses on identifying key events that have significantly impacted oil prices over the past three decades and quantifying their effects to provide actionable insights for investors, policymakers, and energy companies.

### 🚀 Live Dashboard

**Access the interactive dashboard**: http://localhost:3000  
**Backend API**: http://localhost:5000

### Project Structure

```
week10/
├── data/
│   ├── BrentOilPrices.csv          # Historical Brent oil price data (1987-2022)
│   └── major_oil_events.csv        # Database of major oil market events
├── frontend/                       # React frontend application
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   │   ├── Header.js          # Dashboard header with stats
│   │   │   └── Sidebar.js         # Navigation sidebar
│   │   ├── pages/                 # Dashboard pages
│   │   │   ├── Dashboard.js       # Main dashboard overview
│   │   │   ├── PriceAnalysis.js   # Price trends and statistics
│   │   │   ├── EventAnalysis.js   # Event categorization and impact
│   │   │   ├── ChangePointAnalysis.js # Bayesian change point detection
│   │   │   └── EventImpact.js     # Detailed event impact analysis
│   │   └── App.js                 # Main React application
│   ├── package.json               # Frontend dependencies
│   └── public/                    # Static assets
├── src/
│   ├── dashboard_api.py           # Flask REST API backend
│   ├── time_series_analysis.py    # Time series analysis modules
│   └── bayesian_change_point.py   # Bayesian change point detection
├── docs/
│   └── Task1_Foundation_Report.md # Comprehensive foundation analysis report
├── notebooks/
│   └── Task1_Foundation_Analysis.ipynb # Jupyter notebook for interactive analysis
├── output/                        # Generated plots and analysis results
├── venv/                          # Python virtual environment
├── requirements.txt               # Python dependencies
├── start_both.py                  # Script to start both frontend and backend
├── start_dashboard.py             # Alternative dashboard starter
└── README.md                      # This file
```

### Key Components

#### 1. Interactive Dashboard (Frontend)
- **React Application**: Modern, responsive web interface
- **Real-time Data**: Live API integration with backend
- **Interactive Charts**: Chart.js visualizations for price trends
- **Event Analysis**: Categorized event impact analysis
- **Change Point Detection**: Bayesian analysis results visualization

#### 2. REST API Backend
- **Flask API**: RESTful endpoints for data access
- **Data Management**: Efficient data loading and processing
- **Statistical Analysis**: Real-time computation of statistics
- **CORS Support**: Cross-origin requests for frontend integration

#### 3. Analysis Modules
- **Time Series Analysis**: Comprehensive statistical analysis
- **Bayesian Change Point Detection**: Advanced structural break identification
- **Event Impact Analysis**: Quantified event effects on prices

### Installation and Setup

#### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

#### 1. Clone and Setup
```bash
# Navigate to project directory
cd week10

# Activate virtual environment (if exists)
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to project root
cd ..
```

#### 3. Start the Dashboard
```bash
# Start both frontend and backend services
python3 start_both.py
```

The dashboard will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

### Dashboard Features

#### 📊 Main Dashboard
- **Overview Statistics**: Total records, events, change points
- **Real-time API Status**: Connection monitoring
- **Quick Navigation**: Access to all analysis sections
- 

<img width="1303" height="653" alt="Image" src="https://github.com/user-attachments/assets/56ee32db-5774-40c0-822e-be374c875742" />
<img width="1303" height="653" alt="Image" src="https://github.com/user-attachments/assets/14b527bf-4bc8-4536-8049-4dc24de027c1" />
<img width="1303" height="653" alt="Image" src="https://github.com/user-attachments/assets/cc850682-9924-4e40-8420-ecbd439d9697" />

#### 📈 Price Analysis
- **Interactive Charts**: Line charts with price trends
- **Statistical Summary**: Mean, max, min, volatility
- **Data Range**: Complete dataset from 1987-2022
- **Price Statistics**: Comprehensive price analysis

#### 📅 Event Analysis
- **Event Categories**: Economic, Geopolitical, OPEC
- **Impact Analysis**: Positive vs. negative impacts
- **Event Database**: 28 major oil market events
- **Visualization**: Pie charts and bar charts

#### 🔍 Change Point Analysis
- **Bayesian Detection**: Advanced structural break identification
- **Change Points**: 6 significant regime changes detected
- **Confidence Intervals**: Statistical uncertainty quantification
- **Interactive Visualization**: Price trends with change point markers

#### 🎯 Event Impact Analysis
- **Detailed Impact**: Individual event analysis
- **Price Movement**: Pre/post event price changes
- **Impact Quantification**: Statistical impact measures
- **Recovery Analysis**: Time to price stabilization

### API Endpoints

#### Core Endpoints
- `GET /api/stats` - Dashboard statistics and overview
- `GET /api/price-data` - Historical price data (9,011 records)
- `GET /api/events-data` - Event database and categorization
- `GET /api/change-points` - Bayesian change point analysis results
- `GET /api/event-impact/:eventId` - Specific event impact analysis

#### Data Structure
```json
{
  "price_data": {
    "total_records": 9011,
    "date_range": {"start": "1987-05-20", "end": "2022-11-14"},
    "price_stats": {
      "mean": 48.42,
      "max": 143.95,
      "min": 9.1,
      "std": 32.86
    }
  },
  "events_data": {
    "total_events": 28,
    "categories": {"Economic": 7, "Geopolitical": 8, "OPEC": 13},
    "impact_directions": {"Positive": 12, "Negative": 16}
  },
  "analysis_results": {
    "change_points_count": 6,
    "regimes_count": 0
  }
}
```

### Key Findings

#### Time Series Properties
- **Non-stationary**: Brent oil prices show clear trends and changing statistical properties
- **Volatility clustering**: Periods of high/low volatility tend to cluster
- **Structural breaks**: 6 significant change points identified over 35 years
- **Fat tails**: Returns show higher kurtosis than normal distribution

#### Event Categories Analyzed
1. **Geopolitical Events** (8 events): Wars, conflicts, sanctions
2. **OPEC Decisions** (13 events): Production quota changes and policy shifts
3. **Economic Shocks** (7 events): Financial crises, pandemics

#### Major Events Identified
- Gulf War (1990-1991)
- Global Financial Crisis (2008)
- Arab Spring (2011)
- OPEC production decisions (2014-2016)
- COVID-19 pandemic (2020)
- Russia-Ukraine conflict (2022)

### Technical Architecture

#### Frontend (React)
- **Framework**: React 18 with functional components
- **Styling**: Styled-components for modern CSS-in-JS
- **Charts**: Chart.js with react-chartjs-2
- **Animations**: Framer Motion for smooth transitions
- **Icons**: React Icons (Feather icons)
- **Routing**: React Router for navigation

#### Backend (Flask)
- **Framework**: Flask with Flask-RESTful
- **CORS**: Cross-origin resource sharing enabled
- **Data Processing**: Pandas for efficient data manipulation
- **Statistical Analysis**: NumPy, SciPy, PyMC for Bayesian analysis
- **Virtual Environment**: Isolated Python dependencies

#### Data Flow
1. **Data Loading**: CSV files loaded into pandas DataFrames
2. **API Processing**: Real-time data transformation and statistics
3. **Frontend Integration**: RESTful API calls with error handling
4. **Visualization**: Chart.js rendering with responsive design

### Development Commands

#### Start Services
```bash
# Start both frontend and backend
python3 start_both.py

# Start only backend
source venv/bin/activate && python src/dashboard_api.py

# Start only frontend
cd frontend && npm start
```

#### Development
```bash
# Install new Python dependencies
pip install package_name

# Install new Node.js dependencies
cd frontend && npm install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### Assumptions and Limitations

#### Critical Limitations
- **Correlation vs. Causation**: Analysis identifies statistical correlations, not causal relationships
- **Multiple factors**: Oil prices influenced by many simultaneous factors
- **Market complexity**: Non-linear and interactive effects
- **Temporal issues**: Lag effects and cumulative impacts

#### Mitigation Strategies
- Robust statistical methodology
- Multiple analysis approaches
- Sensitivity testing
- Expert validation
- Conservative interpretation

### Communication Strategy

#### Stakeholder-Specific Outputs
1. **Investors**: Risk assessment, hedging strategies, timing recommendations
2. **Policymakers**: Economic stability implications, policy effectiveness
3. **Energy Companies**: Supply chain optimization, pricing strategies

#### Communication Formats
- Interactive web dashboard (real-time)
- Executive summary reports (PDF)
- Technical analysis notebooks
- Presentation materials
- API documentation

### Next Steps

1. **Advanced Analytics**
   - Implement machine learning forecasting models
   - Add sentiment analysis for news events
   - Develop real-time data feeds

2. **Dashboard Enhancements**
   - Add user authentication and personalization
   - Implement data export functionality
   - Add more interactive visualizations

3. **Data Expansion**
   - Include more oil price benchmarks
   - Add macroeconomic indicators
   - Expand event database with real-time feeds

4. **Performance Optimization**
   - Implement data caching
   - Add database backend for scalability
   - Optimize chart rendering for large datasets

### Technical Requirements
<img width="1242" height="646" alt="Image" src="https://github.com/user-attachments/assets/1e0dd5a6-18fb-4e29-ae97-0e2584d4cfda" />
<img width="1293" height="669" alt="Image" src="https://github.com/user-attachments/assets/897f3361-7a17-497d-a9c9-59e7e652b558" />

#### Backend
- Python 3.8+
- Key libraries: pandas, numpy, matplotlib, seaborn, statsmodels, ruptures, pymc, flask, flask-cors, flask-restful
- Virtual environment for dependency isolation

#### Frontend
- Node.js 14+
- React 18+
- Key libraries: react-router-dom, styled-components, framer-motion, react-chartjs-2, chart.js, react-icons

#### System Requirements
- 4GB+ RAM for large dataset processing
- Modern web browser with ES6+ support
- Network connectivity for API communication

### Contributing

This project is part of Birhan Energies' data science initiative. For questions or contributions, please contact the data science team.

### License

This project is proprietary to Birhan Energies and is intended for internal use and client deliverables.

---

**By**: Firaol Bulo  
**Last Updated**: December 2024  
**Version**: 2.0 (Interactive Dashboard)  
**Status**: Production Ready ✅ 
