import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PageContainer = styled(motion.div)`
  padding: 20px;
`;

const PageHeader = styled.div`
  margin-bottom: 30px;
`;

const PageTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 10px;
`;

const PageSubtitle = styled.p`
  font-size: 1.1rem;
  color: #718096;
  margin-bottom: 20px;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const StatCard = styled(motion.div)`
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
`;

const StatTitle = styled.h3`
  font-size: 0.9rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
`;

const ChartContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 30px;
`;

const ChartTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 20px;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.1rem;
  color: #718096;
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  color: #c53030;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
`;

function PriceAnalysis() {
  const [priceData, setPriceData] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPriceData();
  }, []);

  const fetchPriceData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/price-data');
      if (!response.ok) {
        throw new Error('Failed to fetch price data');
      }
      const data = await response.json();
      setPriceData(data);
      
      // Fetch stats
      const statsResponse = await fetch('http://localhost:5000/api/stats');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData.price_data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return `$${parseFloat(price).toFixed(2)}`;
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString();
  };

  if (loading) {
    return (
      <PageContainer>
        <LoadingSpinner>Loading price analysis...</LoadingSpinner>
      </PageContainer>
    );
  }

  if (error) {
    return (
      <PageContainer>
        <ErrorMessage>Error: {error}</ErrorMessage>
      </PageContainer>
    );
  }

  const chartData = priceData ? {
    labels: priceData.slice(-100).map(item => item.Date), // Last 100 data points
    datasets: [
      {
        label: 'Brent Oil Price (USD)',
        data: priceData.slice(-100).map(item => item.Price),
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
      },
    ],
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Brent Oil Price Trends',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value) {
            return '$' + value.toFixed(2);
          }
        }
      },
    },
  };

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <PageTitle>Price Analysis</PageTitle>
        <PageSubtitle>
          Comprehensive analysis of Brent oil price trends, statistics, and historical patterns
        </PageSubtitle>
      </PageHeader>

      {stats && (
        <StatsGrid>
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <StatTitle>Average Price</StatTitle>
            <StatValue>{formatPrice(stats.price_stats.mean)}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <StatTitle>Highest Price</StatTitle>
            <StatValue>{formatPrice(stats.price_stats.max)}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <StatTitle>Lowest Price</StatTitle>
            <StatValue>{formatPrice(stats.price_stats.min)}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <StatTitle>Price Volatility</StatTitle>
            <StatValue>{formatPrice(stats.price_stats.std)}</StatValue>
          </StatCard>
        </StatsGrid>
      )}

      {chartData && (
        <ChartContainer>
          <ChartTitle>Price Trends</ChartTitle>
          <Line data={chartData} options={chartOptions} />
        </ChartContainer>
      )}

      {priceData && (
        <ChartContainer>
          <ChartTitle>Data Summary</ChartTitle>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
            <div>
              <StatTitle>Total Records</StatTitle>
              <StatValue>{priceData.length.toLocaleString()}</StatValue>
            </div>
            <div>
              <StatTitle>Date Range</StatTitle>
              <StatValue style={{ fontSize: '1.2rem' }}>
                {formatDate(priceData[0]?.Date)} - {formatDate(priceData[priceData.length - 1]?.Date)}
              </StatValue>
            </div>
          </div>
        </ChartContainer>
      )}
    </PageContainer>
  );
}

export default PriceAnalysis; 