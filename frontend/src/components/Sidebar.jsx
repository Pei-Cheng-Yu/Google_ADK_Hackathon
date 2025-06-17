import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { goalIdToColorLighterClassHash } from '../utils/utils';

export default function Sidebar({ goals, refreshGoals, onLogout }) {
  const navigate = useNavigate();
  
  useEffect(() => {
    refreshGoals();
  }, []);

 

  return (
    <div className="w-64 h-screen bg-gray-900 text-white p-4 flex flex-col justify-between">
      <div>
        <h1 className="text-2xl font-bold mb-6">ADK Planner</h1>
        <nav className="space-y-3">
          <Link to="/" className="sideBarItem">🏠 Home</Link>
          <Link to="/calendar" className="sideBarItem">📅 Calendar</Link>
          <Link to="/chat" className="chatBot">🤖 Goal Agent</Link>

          <hr className="my-4 border-gray-700" />
          <p className="text-sm text-gray-400">Goals</p>
          {goals.map(goal => (
            
            <Link
              key={goal.goal_id}
              to={`/goals/${goal.goal_id}`}
              className="sideBarItem" 
              style={{ color: goalIdToColorLighterClassHash(goal.goal_id) }}
            >
              {goal.structured_goals?.goal || 'Untitled Goal'}
            </Link>
          ))}
        </nav>
      </div>

      <div className="space-y-2">
        <button
          onClick={() => navigate('/chat')}
          className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          + Add Goal
        </button>
        <button
          onClick={onLogout}
          className="logout"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
