import { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

export default function TimeSlotForm({ onSubmit }) {
  const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  
  const [availability, setAvailability] = useState(
    weekdays.reduce((acc, day) => ({ ...acc, [day]: [] }), {})
  );
  
  const [exceptions, setExceptions] = useState([]);

  const addTimeBlock = (day) => {
    setAvailability((prev) => ({
      ...prev,
      [day]: [...prev[day], { start: '', end: '' }]
    }));
  };

  const updateTime = (day, index, field, value) => {
    setAvailability((prev) => {
      const blocks = [...prev[day]];
      blocks[index][field] = value;
      return { ...prev, [day]: blocks };
    });
  };

  const addException = () => {
    setExceptions((prev) => [...prev, { date: new Date(), times: [''] }]);
  };

  const handleExceptionChange = (index, date) => {
    setExceptions((prev) => {
      const updated = [...prev];
      updated[index] = { ...updated[index], date };
      return updated;
    });
  };

  const handleSubmit = () => {
    const formattedAvailability = {};
    weekdays.forEach((day) => {
      const validTimes = availability[day]
        .filter((b) => b.start && b.end && b.start < b.end)
        .map((b) => `${b.start}–${b.end}`);
      formattedAvailability[day] = validTimes;
    });

    const formattedExceptions = {};
    exceptions.forEach(({ date }) => {
      const key = date.toISOString().split('T')[0];
      formattedExceptions[key] = [];  // "Unavailable all day"
    });

    const result = {
      available: formattedAvailability,
      exceptions: formattedExceptions
    };

    console.log('📤 Submitting:', result); // helpful for debugging
    onSubmit(result);  // make sure parent handles it
  };

  return (
    <div className="space-y-4">
      {weekdays.map((day) => (
        <div key={day}>
          <h3 className="font-semibold mb-1">{day}</h3>
          {availability[day].map((block, i) => (
            <div key={i} className="flex gap-2 mb-1">
              <input
                type="time"
                value={block.start}
                onChange={(e) => updateTime(day, i, 'start', e.target.value)}
              />
              <span>-</span>
              <input
                type="time"
                value={block.end}
                onChange={(e) => updateTime(day, i, 'end', e.target.value)}
              />
            </div>
          ))}
          <button
            className="text-sm text-blue-600 underline"
            onClick={() => addTimeBlock(day)}
          >
            + Add time block
          </button>
        </div>
      ))}

      <div>
        <h3 className="font-semibold mb-1">Exceptions</h3>
        {exceptions.map((ex, i) => (
          <div key={i} className="flex items-center gap-2 mb-1">
            <DatePicker
              selected={ex.date}
              onChange={(date) => handleExceptionChange(i, date)}
              dateFormat="yyyy-MM-dd"
            />
            <span className="text-sm text-gray-500">(Unavailable all day)</span>
          </div>
        ))}
        <button
          className="text-sm text-blue-600 underline"
          onClick={addException}
        >
          + Add exception
        </button>
      </div>

      <button
        onClick={handleSubmit}
        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
      >
        📅 Submit Availability
      </button>
    </div>
  );
}
