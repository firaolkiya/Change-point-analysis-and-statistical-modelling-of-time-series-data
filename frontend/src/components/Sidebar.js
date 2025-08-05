import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { 
  FiHome, 
  FiTrendingUp, 
  FiCalendar, 
  FiBarChart2, 
  FiTarget,
  FiSettings,
  FiDatabase
} from 'react-icons/fi';

const SidebarContainer = styled(motion.nav)`
  width: 280px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 0 20px 20px 0;
  margin: 20px 0 20px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 24px 0;
  height: calc(100vh - 40px);
  overflow-y: auto;
`;

const SidebarHeader = styled.div`
  padding: 0 24px 24px 24px;
  border-bottom: 2px solid #f8f9fa;
  margin-bottom: 24px;
`;

const SidebarTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
`;

const NavSection = styled.div`
  margin-bottom: 32px;
`;

const SectionTitle = styled.h3`
  font-size: 0.875rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 16px 24px;
`;

const NavList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const NavItem = styled(motion.li)`
  margin: 4px 0;
`;

const NavLinkStyled = styled(NavLink)`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  color: #6c757d;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  
  &:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
  }
  
  &.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
  
  &.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: white;
    border-radius: 0 2px 2px 0;
  }
`;

const NavIcon = styled.div`
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const NavText = styled.span`
  font-size: 0.95rem;
`;

const SidebarFooter = styled.div`
  padding: 24px;
  border-top: 2px solid #f8f9fa;
  margin-top: auto;
`;

const FooterText = styled.p`
  font-size: 0.75rem;
  color: #6c757d;
  text-align: center;
  margin: 0;
`;

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    {
      section: 'Main',
      items: [
        { path: '/', icon: <FiHome />, text: 'Dashboard', exact: true },
        { path: '/price-analysis', icon: <FiTrendingUp />, text: 'Price Analysis' },
        { path: '/event-analysis', icon: <FiCalendar />, text: 'Event Analysis' },
        { path: '/change-points', icon: <FiBarChart2 />, text: 'Change Points' }
      ]
    },
    {
      section: 'Analysis',
      items: [
        { path: '/event-impact', icon: <FiTarget />, text: 'Event Impact' }
      ]
    }
  ];

  return (
    <SidebarContainer
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <SidebarHeader>
        <SidebarTitle>
          <FiDatabase />
          Analysis Hub
        </SidebarTitle>
      </SidebarHeader>

      {navItems.map((section, sectionIndex) => (
        <NavSection key={sectionIndex}>
          <SectionTitle>{section.section}</SectionTitle>
          <NavList>
            {section.items.map((item, itemIndex) => (
              <NavItem
                key={itemIndex}
                whileHover={{ x: 4 }}
                whileTap={{ scale: 0.95 }}
              >
                <NavLinkStyled
                  to={item.path}
                  className={({ isActive }) => isActive ? 'active' : ''}
                  end={item.exact}
                >
                  <NavIcon>{item.icon}</NavIcon>
                  <NavText>{item.text}</NavText>
                </NavLinkStyled>
              </NavItem>
            ))}
          </NavList>
        </NavSection>
      ))}

      <SidebarFooter>
        <FooterText>
          Brent Oil Price Analysis Dashboard
          <br />
          v1.0.0
        </FooterText>
      </SidebarFooter>
    </SidebarContainer>
  );
};

export default Sidebar; 