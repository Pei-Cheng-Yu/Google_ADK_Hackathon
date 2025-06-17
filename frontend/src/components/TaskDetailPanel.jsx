export default function TaskDetailPanel({ task, onClose }) {
  if (!task) return null;

  return (
    <div className="w-96 h-full bg-white border-l shadow-inner p-4 overflow-y-auto">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">{task.title}</h2>
        <button onClick={onClose}>✖</button>
      </div>
      <p><strong>Date:</strong> {task.date}</p>
      <p><strong>Time:</strong> {task.start_time} - {task.end_time}</p>
      <p><strong>Goal:</strong> {task.goal}</p>
      <div className="mt-2">
        <p className="font-semibold">Description:</p>
        <p className="text-gray-700">{task.description}</p>
      </div>
    </div>
  );
}
