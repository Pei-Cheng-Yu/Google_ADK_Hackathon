import { useState } from 'react';
import { goalIdToColorClass,goalIdToColorLighterClass } from '../utils/utils';
export default function MilestoneAccordion({ milestones, tasks ,goalId}) {
  return (
    <div className="space-y-4">
      {milestones.map((milestone, index) => (
        <MilestoneItem
          key={index}
          milestone={milestone}
          tasks={tasks.filter(t => t.milestone === index + 1)}
          index={index}
          goalId={goalId}
        />
      ))}
    </div>
  );
}

function MilestoneItem({ milestone, tasks, index ,goalId}) {
    const [open, setOpen] = useState(false);
    const color = goalIdToColorClass(goalId);
    return (
        <div className="border rounded">
        <button
            className={`milestone ${color}`}
            onClick={() => setOpen(!open)}
        >
            {milestone.title}
        </button>
        {open && (
            <div className="p-4 space-y-2">
            <p className="text-sm text-gray-600 mb-2">{milestone.description}</p>
            {tasks.map((task, i) => (
                <TaskAccordion key={i} task={task} goalId={goalId} />
            ))}
            </div>
        )}
        </div>
    );
}

function TaskAccordion({ task ,goalId}) {
  const [open, setOpen] = useState(false);
 const color = goalIdToColorLighterClass(goalId);
  return (
    <div className="border rounded">
      <button
        onClick={() => setOpen(!open)}
        className={`skillpath ${color}`}
      >
        • {task.title}
      </button>
      {open && (
        <div className="pl-4 mt-2 text-sm text-gray-700 space-y-1">
          <p><strong>Description:</strong> {task.description}</p>
          <p><strong>Estimated Hours:</strong> {task.estimated_hours}</p>
          <p><strong>Tags:</strong> {task.tags?.map(t => (
            <span key={t} className="inline-block bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded mr-1">
              #{t}
            </span>
          ))}</p>
          {task.resource?.length > 0 && (
            <p><strong>Resources:</strong> {task.resource.join(', ')}</p>
          )}
        </div>
      )}
    </div>
  );
}
