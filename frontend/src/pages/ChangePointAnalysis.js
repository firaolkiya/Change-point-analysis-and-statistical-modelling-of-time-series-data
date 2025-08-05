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

const ChangePointsList = styled.div`
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
`;

const ListHeader = styled.div`
  background: #f7fafc;
  padding: 20px 30px;
  border-bottom: 1px solid #e2e8f0;
`;

const ListTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
`;

const ChangePointCard = styled(motion.div)`
  padding: 20px 30px;
  border-bottom: 1px solid #e2e8f0;
  background: white;
  
  &:last-child {
    border-bottom: none;
  }
`;

const ChangePointTitle = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 10px;
`;

const ChangePointDate = styled.div`
  font-size: 1rem;
  color: #718096;
  margin-bottom: 10px;
`;

const ChangePointDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
`;

const DetailItem = styled.div`
  background: #f7fafc;
  padding: 10px 15px;
  border-radius: 8px;
`;

const DetailLabel = styled.div`
  font-size: 0.8rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  margin-bottom: 5px;
`;

const DetailValue = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: #2d3748;
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

const NoDataMessage = styled.div`
  background: #fef5e7;
  color: #c05621;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
`;

function ChangePointAnalysis() {
  const [changePointsData, setChangePointsData] = useState(null);
  const [priceData, setPriceData] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChangePointsData();
  }, []);

  const fetchChangePointsData = async () => {
    try {
      setLoading(true);
      
      // Fetch change points data
      const response = await fetch('http://localhost:5000/api/change-points');
      if (!response.ok) {
        throw new Error('Failed to fetch change points data');
      }
      const data = await response.json();
      setChangePointsData(data);
      
      // Fetch price data for visualization
      const priceResponse = await fetch('http://localhost:5000/api/price-data');
      if (priceResponse.ok) {
        const priceData = await priceResponse.json();
        setPriceData(priceData);
      }
      
      // Fetch stats
      const statsResponse = await fetch('http://localhost:5000/api/stats');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData.analysis_results);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString();
  };

  if (loading) {
    return (
      <PageContainer>
        <LoadingSpinner>Loading change point analysis...</LoadingSpinner>
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
    labels: priceData.slice(-200).map(item => item.Date), // Last 200 data points
    datasets: [
      {
        label: 'Brent Oil Price (USD)',
        data: priceData.slice(-200).map(item => item.Price),
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        borderWidth: 2,
        fill: false,
        tension: 0.4,
      },
      // Add change points as scatter points if available
      ...(changePointsData && changePointsData.change_points ? 
        changePointsData.change_points.map((cp, index) => ({
          label: `Change Point ${index + 1}`,
          data: priceData.map((item, i) => {
            if (item.Date === cp.date) {
              return item.Price;
            }
            return null;
          }).filter(val => val !== null),
          pointBackgroundColor: '#f56565',
          pointBorderColor: '#c53030',
          pointBorderWidth: 2,
          pointRadius: 8,
          pointHoverRadius: 10,
          showLine: false,
        })) : []
      ),
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
        text: 'Brent Oil Price with Change Points',
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
        <PageTitle>Change Point Analysis</PageTitle>
        <PageSubtitle>
          Bayesian change point detection analysis to identify significant structural breaks in oil price trends
        </PageSubtitle>
      </PageHeader>

      {stats && (
        <StatsGrid>
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <StatTitle>Change Points Detected</StatTitle>
            <StatValue>{stats.change_points_count}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <StatTitle>Regimes Identified</StatTitle>
            <StatValue>{stats.regimes_count}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <StatTitle>Analysis Method</StatTitle>
            <StatValue style={{ fontSize: '1.2rem' }}>Bayesian</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <StatTitle>Confidence Level</StatTitle>
            <StatValue style={{ fontSize: '1.2rem' }}>95%</StatValue>
          </StatCard>
        </StatsGrid>
      )}

      {chartData && (
        <ChartContainer>
          <ChartTitle>Price Trends with Change Points</ChartTitle>
          <Line data={chartData} options={chartOptions} />
        </ChartContainer>
      )}

      {changePointsData && changePointsData.change_points && changePointsData.change_points.length > 0 ? (
        <ChangePointsList>
          <ListHeader>
            <ListTitle>Detected Change Points</ListTitle>
          </ListHeader>
          {changePointsData.change_points.map((changePoint, index) => (
            <ChangePointCard
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <ChangePointTitle>Change Point {index + 1}</ChangePointTitle>
              <ChangePointDate>Date: {formatDate(changePoint.date)}</ChangePointDate>
              
              <ChangePointDetails>
                {changePoint.confidence_interval && (
                  <DetailItem>
                    <DetailLabel>Confidence Interval</DetailLabel>
                    <DetailValue>{changePoint.confidence_interval}</DetailValue>
                  </DetailItem>
                )}
                
                {changePoint.uncertainty && (
                  <DetailItem>
                    <DetailLabel>Uncertainty</DetailLabel>
                    <DetailValue>{changePoint.uncertainty}</DetailValue>
                  </DetailItem>
                )}
                
                {changePoint.description && (
                  <DetailItem>
                    <DetailLabel>Description</DetailLabel>
                    <DetailValue>{changePoint.description}</DetailValue>
                  </DetailItem>
                )}
              </ChangePointDetails>
            </ChangePointCard>
          ))}
        </ChangePointsList>
      ) : (
        <NoDataMessage>
          No change points data available. The analysis may still be running or no significant change points were detected.
        </NoDataMessage>
      )}
    </PageContainer>
  );
}

export default ChangePointAnalysis; 