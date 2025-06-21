import { useCallback, useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import api from './api';
import Sidebar from './components/Sidebar';
import CalendarPage from './pages/CalendarPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ChatPage from './pages/ChatPage'
import GoalDetailPage from './pages/GoalDetailPage';
import WelcomePage from './pages/WelcomePage';
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const [goals, setGoals] = useState([]);
  const refreshGoals = useCallback(async () => {
    try {
      const res = await api.get('/goal');
      setGoals(res.data);
    } catch (err) {
      console.error('Failed to fetch goals:', err);
    }
  }, []);


    
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  return (
    <Router basename="/Google_ADK_Hackathon" key={isAuthenticated ? 'auth' : 'guest'}>
      {isAuthenticated ? (
        <div className="flex h-screen w-screen">
          <Sidebar goals={goals} refreshGoals={refreshGoals} onLogout={handleLogout} />
          <div className="flex-1">
            <Routes>
              <Route path="/" element={<WelcomePage />} />
              <Route path="/calendar" element={<CalendarPage />} />
              <Route path="/chat" element={<ChatPage refreshGoals={refreshGoals} />} />
              <Route path="/goals/:goalId" element={<GoalDetailPage />} />
              <Route path="/login" element={<Navigate to="/" />} />
              <Route path="/register" element={<Navigate to="/" />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      ) : (
        <Routes>
          <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* Redirect all other routes to login */}
          <Route path="*" element={<Navigate to="/register" />} />
        </Routes>
      )}
    </Router>
  );
}

export default App;
