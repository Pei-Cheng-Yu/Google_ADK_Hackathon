import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function WelcomePage() {
  const navigate = useNavigate();

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <h1 className="text-4xl font-bold">🏠 ADK Planner</h1>
      <p className="text-lg text-gray-600">
        Welcome to the <strong>ADK Planner</strong> — an intelligent planning assistant that helps you clarify goals, set your weekly availability, and auto-generate personalized daily plans.
      </p>

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">🧭 How It Works</h2>

        <div className="space-y-2">
          <h3 className="text-xl font-medium">1. 🤖 Define Your Goal</h3>
          <p>
            Go to the <strong>Goal Agent</strong> page and tell the agent what you want to achieve.
            <br />
            <em>Example:</em> "I want to learn Python for data science."
          </p>
        </div>

        <div className="space-y-2">
          <h3 className="text-xl font-medium">2. ✅ Goal Saved Automatically</h3>
          <p>The agent will ask follow-up questions to complete your goal and then save it for you.</p>
          <p>After agent save the <strong>"roadmap and skillpath"</strong>, you can still modify any thing about the goal. </p>
          <p>👀 Check out the milestone and task in <strong>"Goals"</strong> section in the sidebar.</p>
        </div>
        
      
        <div className="space-y-2">
          <h3 className="text-xl font-medium">3. 🗓️ Set Your Available Time</h3>
          <p>Tell agent <strong>"Set TimeSlot"</strong> and answer follow-up questions,</p>
          <p>or click <strong>"Set Weekly Availability"</strong> in the chat and input your schedule.</p>
        </div>

        <div className="space-y-2">
          <h3 className="text-xl font-medium">4. 📅 Ask to Generate a Plan</h3>
          <p>Type <em>"set plan"</em> and the agent will create a schedule based on all your goals.</p>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">💡 Tips</h2>
        <ul className="list-disc list-inside space-y-1">
          <li>No need to select goals for planning — it happens for all.</li>
          <li>Each goal is color-coded in the calendar.</li>
          <li>Click a calendar task to view its full details in the sidebar.</li>
          
        </ul>
      </section>


      <div className="pt-6">
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded"
          onClick={() => navigate('/chat')}
        >
          🚀 Start Planning Now
        </button>
      </div>
    </div>
  );
}
