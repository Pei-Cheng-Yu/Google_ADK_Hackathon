import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import MilestoneAccordion from '../components/MilestoneAccordion';

export default function GoalDetailPage() {
  const { goalId } = useParams();
  const [goal, setGoal] = useState(null);
  const [roadmap, setRoadmap] = useState(null); // was []
  const [skillpath, setSkillpath] = useState(null); // was []

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [goalRes, roadmapRes, skillpathRes] = await Promise.all([
          api.get(`/goal/${goalId}`),
          api.get(`/roadmap/${goalId}`),
          api.get(`/skillpath/${goalId}`)
        ]);

        setGoal(goalRes.data);
        setRoadmap(roadmapRes.data);
        setSkillpath(skillpathRes.data);
      } catch (err) {
        console.error('Failed to load goal details:', err);
      }
    };

    fetchData();
  }, [goalId]);

  if (!goal) return <div className="p-6">Loading goal...</div>;

  const milestones = roadmap?.structured_roadmaps?.milestones || [];
  const tasks = skillpath?.structured_skillpaths?.learning_path || [];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-2">{goal.structured_goals?.goal || 'Untitled Goal'}</h1>
        <p className="text-sm text-gray-600">Category: {goal.structured_goals?.category}</p>
        <p className="text-sm text-gray-600">Timeframe: {goal.structured_goals?.timeframe}</p>
        <p className="text-sm text-gray-600">Experience Level: {goal.structured_goals?.experience_level}</p>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-2">📍 Milestones & Tasks</h2>
        <MilestoneAccordion
        milestones={roadmap.structured_roadmaps?.milestones || []}
        tasks={skillpath.structured_skillpaths?.learning_path || []}
        goalId={goalId}
        />
      </div>
    </div>
  );
}
