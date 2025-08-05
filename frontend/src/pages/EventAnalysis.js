import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
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

const EventsTable = styled.div`
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
`;

const TableHeader = styled.div`
  background: #f7fafc;
  padding: 20px 30px;
  border-bottom: 1px solid #e2e8f0;
`;

const TableTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const Th = styled.th`
  text-align: left;
  padding: 15px 20px;
  background: #f7fafc;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 1px solid #e2e8f0;
`;

const Td = styled.td`
  padding: 15px 20px;
  border-bottom: 1px solid #e2e8f0;
  color: #2d3748;
`;

const EventCategory = styled.span`
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
`;

const EconomicCategory = styled(EventCategory)`
  background: #c6f6d5;
  color: #22543d;
`;

const GeopoliticalCategory = styled(EventCategory)`
  background: #fed7d7;
  color: #742a2a;
`;

const OpecCategory = styled(EventCategory)`
  background: #bee3f8;
  color: #2a4365;
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

function EventAnalysis() {
  const [eventsData, setEventsData] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEventsData();
  }, []);

  const fetchEventsData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/events-data');
      if (!response.ok) {
        throw new Error('Failed to fetch events data');
      }
      const data = await response.json();
      setEventsData(data);
      
      // Fetch stats
      const statsResponse = await fetch('http://localhost:5000/api/stats');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData.events_data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryComponent = (category) => {
    switch (category) {
      case 'Economic':
        return EconomicCategory;
      case 'Geopolitical':
        return GeopoliticalCategory;
      case 'OPEC':
        return OpecCategory;
      default:
        return EventCategory;
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString();
  };

  if (loading) {
    return (
      <PageContainer>
        <LoadingSpinner>Loading event analysis...</LoadingSpinner>
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

  const categoryData = stats ? {
    labels: Object.keys(stats.categories),
    datasets: [
      {
        data: Object.values(stats.categories),
        backgroundColor: [
          '#c6f6d5',
          '#fed7d7',
          '#bee3f8',
        ],
        borderColor: [
          '#22543d',
          '#742a2a',
          '#2a4365',
        ],
        borderWidth: 2,
      },
    ],
  } : null;

  const impactData = stats ? {
    labels: Object.keys(stats.impact_directions),
    datasets: [
      {
        label: 'Number of Events',
        data: Object.values(stats.impact_directions),
        backgroundColor: [
          '#48bb78',
          '#f56565',
        ],
        borderColor: [
          '#22543d',
          '#742a2a',
        ],
        borderWidth: 1,
      },
    ],
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
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
        <PageTitle>Event Analysis</PageTitle>
        <PageSubtitle>
          Analysis of major oil events and their impact on Brent oil prices
        </PageSubtitle>
      </PageHeader>

      {stats && (
        <StatsGrid>
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <StatTitle>Total Events</StatTitle>
            <StatValue>{stats.total_events}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <StatTitle>Economic Events</StatTitle>
            <StatValue>{stats.categories.Economic}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <StatTitle>Geopolitical Events</StatTitle>
            <StatValue>{stats.categories.Geopolitical}</StatValue>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <StatTitle>OPEC Events</StatTitle>
            <StatValue>{stats.categories.OPEC}</StatValue>
          </StatCard>
        </StatsGrid>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '30px' }}>
        {categoryData && (
          <ChartContainer>
            <ChartTitle>Events by Category</ChartTitle>
            <Pie data={categoryData} options={chartOptions} />
          </ChartContainer>
        )}
        
        {impactData && (
          <ChartContainer>
            <ChartTitle>Events by Impact Direction</ChartTitle>
            <Bar data={impactData} options={barOptions} />
          </ChartContainer>
        )}
      </div>

      {eventsData && (
        <EventsTable>
          <TableHeader>
            <TableTitle>Major Oil Events</TableTitle>
          </TableHeader>
          <Table>
            <thead>
              <tr>
                <Th>Date</Th>
                <Th>Event</Th>
                <Th>Category</Th>
                <Th>Impact</Th>
                <Th>Description</Th>
              </tr>
            </thead>
            <tbody>
              {eventsData.events.slice(0, 10).map((event, index) => {
                const CategoryComponent = getCategoryComponent(event.category);
                return (
                  <motion.tr
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Td>{formatDate(event.date)}</Td>
                    <Td style={{ fontWeight: '600' }}>{event.event}</Td>
                    <Td>
                      <CategoryComponent>{event.category}</CategoryComponent>
                    </Td>
                    <Td>
                      <span style={{
                        color: event.impact_direction === 'Positive' ? '#48bb78' : '#f56565',
                        fontWeight: '600'
                      }}>
                        {event.impact_direction}
                      </span>
                    </Td>
                    <Td style={{ maxWidth: '300px' }}>{event.description}</Td>
                  </motion.tr>
                );
              })}
            </tbody>
          </Table>
        </EventsTable>
      )}
    </PageContainer>
  );
}

export default EventAnalysis; 