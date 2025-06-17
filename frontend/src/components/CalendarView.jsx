

const tasks = [
  {
    id: 1,
    title: "Build UI",
    date: 12,
    start_time: "14:00",
    end_time: "15:00",
    goal: "Hackathon MVP",
    goalColor: "bg-orange-300",
    description: "Work on sidebar and calendar."
  },
  {
    id: 2,
    title: "Study React",
    date: 13,
    start_time: "10:00",
    end_time: "11:00",
    goal: "Learn React",
    goalColor: "bg-blue-300",
    description: "Read React documentation."
  }
];

export default function CalendarView({ onSelectTask }) {
  const days = Array.from({ length: 30 }, (_, i) => i + 1);

  const tasksForDay = (day) => tasks.filter((t) => t.date === day);

  return (
    <div className="flex-1 p-6 justify-center">
        <div className="w-full max-w-fit">
      <h2 className="text-xl font-semibold mb-4">📅 My Calendar</h2>
      <div className="grid grid-cols-7 gap-2">
        {days.map((day) => (
          <div key={day} className="border h-50 w-40 bg-white rounded shadow-sm p-2">
            <div className="text-sm font-bold">{day}</div>
            {tasksForDay(day).map((task) => (
              <div
                key={task.id}
                className={`mt-1 p-1 text-xs rounded cursor-pointer ${task.goalColor}`}
                onClick={() => onSelectTask(task)}
              >
                {task.title}
              </div>
            ))}
          </div>
        ))}
      </div>
      </div>
    </div>
  );
}
