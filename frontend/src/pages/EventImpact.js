import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useParams } from 'react-router-dom';

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

const EventCard = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 30px;
`;

const EventTitle = styled.h2`
  font-size: 1.8rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 15px;
`;

const EventDate = styled.div`
  font-size: 1.1rem;
  color: #718096;
  margin-bottom: 20px;
`;

const EventDescription = styled.p`
  font-size: 1.1rem;
  color: #4a5568;
  line-height: 1.6;
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

function EventImpact() {
  const { eventId } = useParams();
  const [eventData, setEventData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEventData();
  }, [eventId]);

  const fetchEventData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5000/api/event-impact/${eventId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch event data');
      }
      const data = await response.json();
      setEventData(data.event);
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
        <LoadingSpinner>Loading event impact analysis...</LoadingSpinner>
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

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <PageTitle>Event Impact Analysis</PageTitle>
        <PageSubtitle>
          Detailed analysis of the impact of specific events on Brent oil prices
        </PageSubtitle>
      </PageHeader>

      {eventData ? (
        <EventCard>
          <EventTitle>{eventData.event}</EventTitle>
          <EventDate>Date: {formatDate(eventData.date)}</EventDate>
          <EventDescription>{eventData.description}</EventDescription>
        </EventCard>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Event not found or no impact data available.</p>
        </div>
      )}
    </PageContainer>
  );
}

export default EventImpact; 