import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { FiTrendingUp, FiTrendingDown, FiDollarSign, FiActivity } from 'react-icons/fi';

const DashboardContainer = styled(motion.div)`
  padding: 20px;
`;

const PageHeader = styled.div`
  margin-bottom: 32px;
`;

const PageTitle = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
`;

const PageSubtitle = styled.p`
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
`;

const StatCard = styled(motion.div)`
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
`;

const StatHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
`;

const StatIcon = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  background: ${props => props.color || '#667eea'};
  color: white;
`;

const StatContent = styled.div`
  text-align: right;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
`;

const StatLabel = styled.div`
  font-size: 0.875rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const StatChange = styled.div`
  font-size: 0.875rem;
  color: ${props => props.positive ? '#28a745' : '#dc3545'};
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
`;

const ChartsGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
  
  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const ChartCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border: 1px solid #e9ecef;
`;

const ChartHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const ChartTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
`;

const Spinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({});
  const [priceData, setPriceData] = useState([]);
  const [eventsData, setEventsData] = useState([]);
  const [changePoints, setChangePoints] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch all data in parallel
        const [statsRes, priceRes, eventsRes, changePointsRes] = await Promise.all([
          fetch('/api/stats'),
          fetch('/api/price-data?limit=1000'),
          fetch('/api/events'),
          fetch('/api/change-points')
        ]);

        if (statsRes.ok) {
          const statsData = await statsRes.json();
          setStats(statsData);
        }

        if (priceRes.ok) {
          const priceData = await priceRes.json();
          setPriceData(priceData.data || []);
        }

        if (eventsRes.ok) {
          const eventsData = await eventsRes.json();
          setEventsData(eventsData.data || []);
        }

        if (changePointsRes.ok) {
          const changePointsData = await changePointsRes.json();
          setChangePoints(changePointsData.change_points || []);
        }

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // Prepare data for charts
  const priceChartData = priceData.map(item => ({
    date: new Date(item.Date).toLocaleDateString(),
    price: parseFloat(item.Price)
  }));

  const eventCategories = eventsData.reduce((acc, event) => {
    acc[event.Event_Category] = (acc[event.Event_Category] || 0) + 1;
    return acc;
  }, {});

  const pieChartData = Object.entries(eventCategories).map(([category, count]) => ({
    name: category,
    value: count
  }));

  if (loading) {
    return (
      <DashboardContainer>
        <LoadingSpinner>
          <Spinner />
        </LoadingSpinner>
      </DashboardContainer>
    );
  }

  return (
    <DashboardContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <PageTitle>Dashboard Overview</PageTitle>
        <PageSubtitle>
          Comprehensive analysis of Brent oil prices and market events
        </PageSubtitle>
      </PageHeader>

      <StatsGrid>
        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <StatHeader>
            <StatIcon color="#667eea">
              <FiDollarSign />
            </StatIcon>
            <StatContent>
              <StatValue>
                ${stats.price_data?.price_stats?.mean?.toFixed(2) || '0.00'}
              </StatValue>
              <StatLabel>Average Price</StatLabel>
              <StatChange positive={true}>
                <FiTrendingUp />
                +2.5%
              </StatChange>
            </StatContent>
          </StatHeader>
        </StatCard>

        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <StatHeader>
            <StatIcon color="#28a745">
              <FiActivity />
            </StatIcon>
            <StatContent>
              <StatValue>{stats.events_data?.total_events || 0}</StatValue>
              <StatLabel>Total Events</StatLabel>
              <StatChange positive={true}>
                <FiTrendingUp />
                Active
              </StatChange>
            </StatContent>
          </StatHeader>
        </StatCard>

        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <StatHeader>
            <StatIcon color="#dc3545">
              <FiTrendingDown />
            </StatIcon>
            <StatContent>
              <StatValue>{stats.analysis_results?.change_points_count || 0}</StatValue>
              <StatLabel>Change Points</StatLabel>
              <StatChange positive={false}>
                <FiTrendingDown />
                Detected
              </StatChange>
            </StatContent>
          </StatHeader>
        </StatCard>

        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <StatHeader>
            <StatIcon color="#ffc107">
              <FiTrendingUp />
            </StatIcon>
            <StatContent>
              <StatValue>{stats.price_data?.total_records?.toLocaleString() || 0}</StatValue>
              <StatLabel>Price Records</StatLabel>
              <StatChange positive={true}>
                <FiTrendingUp />
                Complete
              </StatChange>
            </StatContent>
          </StatHeader>
        </StatCard>
      </StatsGrid>

      <ChartsGrid>
        <ChartCard>
          <ChartHeader>
            <ChartTitle>Brent Oil Price Trend</ChartTitle>
          </ChartHeader>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={priceChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={80}
                interval="preserveStartEnd"
              />
              <YAxis />
              <Tooltip 
                formatter={(value) => [`$${value}`, 'Price']}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#667eea" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard>
          <ChartHeader>
            <ChartTitle>Event Categories</ChartTitle>
          </ChartHeader>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={pieChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </ChartsGrid>

      <ChartCard>
        <ChartHeader>
          <ChartTitle>Recent Events Timeline</ChartTitle>
        </ChartHeader>
        <div style={{ maxHeight: 300, overflowY: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Event</th>
                <th>Category</th>
                <th>Impact</th>
              </tr>
            </thead>
            <tbody>
              {eventsData.slice(0, 10).map((event, index) => (
                <tr key={index}>
                  <td>{event.Date}</td>
                  <td>{event.Event_Description}</td>
                  <td>
                    <span className={`badge badge-${event.Event_Category === 'Geopolitical' ? 'danger' : 
                      event.Event_Category === 'OPEC' ? 'warning' : 'info'}`}>
                      {event.Event_Category}
                    </span>
                  </td>
                  <td>
                    <span className={`badge badge-${event.Impact_Direction === 'Positive' ? 'success' : 'danger'}`}>
                      {event.Impact_Direction}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ChartCard>
    </DashboardContainer>
  );
};

export default Dashboard; 