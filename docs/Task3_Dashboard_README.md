# Task 3: Interactive Dashboard for Brent Oil Price Analysis

## Overview

This task implements a comprehensive interactive dashboard application using Flask (backend) and React (frontend) to visualize the results of the Brent oil price analysis, helping stakeholders explore how various events affect oil prices.

## Architecture

### Backend (Flask)
- **Framework**: Flask with Flask-RESTful and Flask-CORS
- **API Design**: RESTful endpoints for data access
- **Data Management**: Integrated with analysis results from Tasks 1 & 2
- **Real-time Updates**: API status monitoring and data validation

### Frontend (React)
- **Framework**: React 18 with modern hooks
- **Styling**: Styled-components with responsive design
- **Charts**: Recharts for interactive visualizations
- **Animations**: Framer Motion for smooth transitions
- **Icons**: React Icons for consistent UI elements

## Key Features

### 🎯 Core Dashboard Features

1. **Interactive Price Charts**
   - Real-time Brent oil price trends
   - Zoomable and pannable charts
   - Event markers and annotations
   - Multiple time period views

2. **Event Analysis**
   - Event timeline with filtering
   - Category-based event grouping
   - Impact analysis with quantitative metrics
   - Event-to-price correlation visualization

3. **Change Point Visualization**
   - Bayesian change point detection results
   - Regime analysis with statistical metrics
   - Confidence intervals and uncertainty quantification
   - Interactive change point exploration

4. **Advanced Filtering**
   - Date range selection
   - Event category filters
   - Impact direction filtering
   - Real-time data filtering

### 📊 Interactive Visualizations

1. **Price Trend Analysis**
   - Line charts with event overlays
   - Volatility clustering visualization
   - Rolling statistics display
   - Price change indicators

2. **Event Impact Analysis**
   - Before/after event price comparisons
   - Impact magnitude visualization
   - Statistical significance indicators
   - Event correlation matrices

3. **Statistical Dashboard**
   - Key performance indicators
   - Real-time statistics updates
   - Trend analysis metrics
   - Data quality indicators

## Installation & Setup

### Prerequisites

1. **Python Environment**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   ```

2. **Node.js Environment**
   ```bash
   # Install Node.js (v16 or higher)
   # Download from https://nodejs.org/
   ```

### Quick Start

1. **Setup Dashboard**
   ```bash
   # Run the setup script
   python run_dashboard.py
   ```

2. **Start Backend**
   ```bash
   # Start Flask API server
   python run_dashboard.py --backend
   ```

3. **Start Frontend**
   ```bash
   # Start React development server
   python run_dashboard.py --frontend
   ```

4. **Access Dashboard**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## API Endpoints

### Core Data Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/price-data` | GET | Get Brent oil price data with filtering |
| `/api/events` | GET | Get major oil events with filtering |
| `/api/change-points` | GET | Get change point analysis results |
| `/api/event-impact` | GET | Analyze specific event impact |
| `/api/stats` | GET | Get dashboard statistics |

### Query Parameters

#### Price Data Filtering
```
GET /api/price-data?start_date=2020-01-01&end_date=2022-12-31&limit=1000
```

#### Events Filtering
```
GET /api/events?category=Geopolitical&impact_direction=Positive&start_date=2020-01-01
```

#### Event Impact Analysis
```
GET /api/event-impact?event_id=5&window_days=30
```

## Frontend Components

### Core Components

1. **Header Component**
   - Real-time API status indicator
   - Quick statistics display
   - Navigation controls

2. **Sidebar Navigation**
   - Main navigation menu
   - Section organization
   - Active state indicators

3. **Dashboard Overview**
   - Key metrics cards
   - Interactive charts
   - Recent events timeline

4. **Analysis Pages**
   - Price Analysis: Detailed price trends
   - Event Analysis: Event exploration tools
   - Change Points: Bayesian analysis results
   - Event Impact: Individual event analysis

### Chart Components

1. **Price Trend Chart**
   ```jsx
   <LineChart data={priceData}>
     <Line dataKey="price" stroke="#667eea" />
     <XAxis dataKey="date" />
     <YAxis />
     <Tooltip />
   </LineChart>
   ```

2. **Event Categories Pie Chart**
   ```jsx
   <PieChart>
     <Pie data={eventCategories} dataKey="value" />
     <Tooltip />
   </PieChart>
   ```

3. **Impact Analysis Chart**
   ```jsx
   <BarChart data={impactData}>
     <Bar dataKey="impact" fill="#667eea" />
     <XAxis dataKey="event" />
     <YAxis />
   </BarChart>
   ```

## Data Flow

### Backend Data Processing

1. **Data Loading**
   ```python
   class DataManager:
       def load_data(self):
           # Load price data
           self.price_data = pd.read_csv('data/BrentOilPrices.csv')
           
           # Load events data
           self.events_data = pd.read_csv('data/major_oil_events.csv')
           
           # Load analysis results
           self.load_analysis_results()
   ```

2. **API Response Format**
   ```json
   {
     "data": [...],
     "total_records": 9011,
     "date_range": {
       "start": "1987-05-21",
       "end": "2022-11-14"
     }
   }
   ```

### Frontend Data Handling

1. **Data Fetching**
   ```javascript
   const fetchDashboardData = async () => {
     const [statsRes, priceRes, eventsRes] = await Promise.all([
       fetch('/api/stats'),
       fetch('/api/price-data?limit=1000'),
       fetch('/api/events')
     ]);
   };
   ```

2. **State Management**
   ```javascript
   const [loading, setLoading] = useState(true);
   const [stats, setStats] = useState({});
   const [priceData, setPriceData] = useState([]);
   const [eventsData, setEventsData] = useState([]);
   ```

## Responsive Design

### Mobile-First Approach

1. **Breakpoints**
   ```css
   @media (max-width: 768px) {
     .grid-2, .grid-3, .grid-4 {
       grid-template-columns: 1fr;
     }
   }
   ```

2. **Touch-Friendly Interface**
   - Large touch targets
   - Swipe gestures for navigation
   - Optimized chart interactions

3. **Performance Optimization**
   - Lazy loading of components
   - Efficient data pagination
   - Optimized chart rendering

## Advanced Features

### Real-time Updates

1. **API Status Monitoring**
   ```javascript
   const checkApiStatus = async () => {
     const response = await fetch('/api/stats');
     setApiStatus(response.ok ? 'online' : 'offline');
   };
   ```

2. **Data Refresh**
   - Automatic data updates
   - Manual refresh controls
   - Change notifications

### Interactive Filters

1. **Date Range Selection**
   ```jsx
   <DatePicker
     selected={startDate}
     onChange={setStartDate}
     placeholderText="Select start date"
   />
   ```

2. **Category Filtering**
   ```jsx
   <Select
     options={categories}
     onChange={setSelectedCategory}
     placeholder="Select category"
   />
   ```

### Export Capabilities

1. **Chart Export**
   - PNG/PDF export
   - Data export (CSV/JSON)
   - Report generation

2. **Share Functionality**
   - URL sharing with filters
   - Embeddable charts
   - Social media integration

## Performance Optimization

### Backend Optimization

1. **Data Caching**
   ```python
   @app.cache.memoize(timeout=300)
   def get_price_data(start_date, end_date):
       return process_price_data(start_date, end_date)
   ```

2. **Pagination**
   ```python
   def get(self):
       page = request.args.get('page', 1, type=int)
       per_page = request.args.get('per_page', 100, type=int)
       return paginate_data(data, page, per_page)
   ```

### Frontend Optimization

1. **Component Memoization**
   ```javascript
   const MemoizedChart = React.memo(PriceChart);
   ```

2. **Virtual Scrolling**
   ```javascript
   import { FixedSizeList as List } from 'react-window';
   ```

## Security Considerations

1. **API Security**
   - CORS configuration
   - Input validation
   - Rate limiting

2. **Data Protection**
   - Secure data transmission
   - Access control
   - Audit logging

## Deployment

### Production Setup

1. **Backend Deployment**
   ```bash
   # Using Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 dashboard_api:app
   ```

2. **Frontend Build**
   ```bash
   cd frontend
   npm run build
   ```

3. **Environment Configuration**
   ```bash
   # Set environment variables
   export FLASK_ENV=production
   export REACT_APP_API_URL=https://api.example.com
   ```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check if backend is running
   - Verify CORS configuration
   - Check network connectivity

2. **Chart Rendering Issues**
   - Clear browser cache
   - Check data format
   - Verify chart library versions

3. **Performance Issues**
   - Reduce data load size
   - Enable data caching
   - Optimize chart configurations

## Future Enhancements

### Planned Features

1. **Advanced Analytics**
   - Machine learning predictions
   - Anomaly detection
   - Pattern recognition

2. **Real-time Data**
   - Live price feeds
   - WebSocket connections
   - Push notifications

3. **User Management**
   - User authentication
   - Role-based access
   - Custom dashboards

4. **Mobile App**
   - React Native version
   - Offline capabilities
   - Push notifications

## Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Run tests**
5. **Submit pull request**

### Code Standards

- Follow PEP 8 for Python
- Use ESLint for JavaScript
- Write comprehensive tests
- Document all functions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review troubleshooting guide 