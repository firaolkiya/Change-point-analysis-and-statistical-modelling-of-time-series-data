import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import PriceAnalysis from './pages/PriceAnalysis';
import EventAnalysis from './pages/EventAnalysis';
import ChangePointAnalysis from './pages/ChangePointAnalysis';
import EventImpact from './pages/EventImpact';

// Global styles
import './App.css';

const AppContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const MainContent = styled(motion.main)`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px 0 0 20px;
  margin: 20px 0 20px 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

const ContentWrapper = styled.div`
  max-width: 1400px;
  margin: 0 auto;
`;

function App() {
  return (
    <Router>
      <AppContainer>
        <Sidebar />
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <Header />
          <MainContent
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <ContentWrapper>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/price-analysis" element={<PriceAnalysis />} />
                <Route path="/event-analysis" element={<EventAnalysis />} />
                <Route path="/change-points" element={<ChangePointAnalysis />} />
                <Route path="/event-impact/:eventId" element={<EventImpact />} />
              </Routes>
            </ContentWrapper>
          </MainContent>
        </div>
      </AppContainer>
    </Router>
  );
}

export default App; 