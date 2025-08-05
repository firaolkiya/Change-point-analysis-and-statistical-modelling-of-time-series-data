import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiCalendar, FiBarChart2, FiSettings } from 'react-icons/fi';

const HeaderContainer = styled(motion.header)`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 16px 24px;
  border-radius: 0 20px 20px 0;
  margin: 20px 0 0 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const HeaderLeft = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
`;

const LogoIcon = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
`;

const HeaderRight = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: ${props => props.status === 'online' ? '#d4edda' : '#f8d7da'};
  color: ${props => props.status === 'online' ? '#155724' : '#721c24'};
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
`;

const StatusDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.status === 'online' ? '#28a745' : '#dc3545'};
  animation: ${props => props.status === 'online' ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const QuickStats = styled.div`
  display: flex;
  gap: 24px;
`;

const StatItem = styled.div`
  text-align: center;
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  border-left: 3px solid #667eea;
`;

const StatValue = styled.div`
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
`;

const StatLabel = styled.div`
  font-size: 0.75rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const Header = () => {
  const [apiStatus, setApiStatus] = React.useState('checking');
  const [stats, setStats] = React.useState({
    totalRecords: 0,
    totalEvents: 0,
    changePoints: 0
  });

  React.useEffect(() => {
    // Check API status
    const checkApiStatus = async () => {
      try {
        const response = await fetch('/api/stats');
        if (response.ok) {
          const data = await response.json();
          setStats({
            totalRecords: data.price_data?.total_records || 0,
            totalEvents: data.events_data?.total_events || 0,
            changePoints: data.analysis_results?.change_points_count || 0
          });
          setApiStatus('online');
        } else {
          setApiStatus('offline');
        }
      } catch (error) {
        setApiStatus('offline');
      }
    };

    checkApiStatus();
    const interval = setInterval(checkApiStatus, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <HeaderContainer
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <HeaderLeft>
        <Logo>
          <LogoIcon>🛢️</LogoIcon>
          Brent Oil Analysis
        </Logo>
      </HeaderLeft>

      <HeaderRight>
        <QuickStats>
          <StatItem>
            <StatValue>{stats.totalRecords.toLocaleString()}</StatValue>
            <StatLabel>Price Records</StatLabel>
          </StatItem>
          <StatItem>
            <StatValue>{stats.totalEvents}</StatValue>
            <StatLabel>Events</StatLabel>
          </StatItem>
          <StatItem>
            <StatValue>{stats.changePoints}</StatValue>
            <StatLabel>Change Points</StatLabel>
          </StatItem>
        </QuickStats>

        <StatusIndicator status={apiStatus}>
          <StatusDot status={apiStatus} />
          {apiStatus === 'online' ? 'API Online' : 'API Offline'}
        </StatusIndicator>
      </HeaderRight>
    </HeaderContainer>
  );
};

export default Header; 