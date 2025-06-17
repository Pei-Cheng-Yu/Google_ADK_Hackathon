import { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import api from '../api';
import { goalIdToColorLighterClassHash } from '../utils/utils';

export default function CalendarPage() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    api.get('/plan')
      .then(res => setEvents(formatPlanForCalendar(res.data)))
      .catch(console.error);
  }, []);

  const formatPlanForCalendar = (plan) => {
  return plan.map(item => {
     const color = goalIdToColorLighterClassHash(item.goal_id);
    return {
        title: item.title,
        start: `${item.date}T${item.start_time}`,
        end: `${item.date}T${item.end_time}`,
        backgroundColor: color,
        borderColor: color,
        
        extendedProps: {
            description: item.description,
            tags: item.tags,
            milestone: item.milestone,
            goal_id: item.goal_id,
            resource: item.resource
        }
    };
  });
};

  return (
    <div className="flex h-screen">
      <div className="flex-1 p-4 ">
        <FullCalendar
          height="auto"
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          events={events}
          eventClick={(info) => {
            setSelectedEvent(info.event);
          }}
        />
      </div>

      <div className="w-96 p-4 border-l bg-gray-50 overflow-y-auto">
        {selectedEvent ? (
          <div className="space-y-2">
            <h2 className="text-xl font-semibold">{selectedEvent.title}</h2>
            <p className="text-sm text-gray-500">
              🕒 {selectedEvent.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {selectedEvent.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
            <p className="text-sm"><strong>Milestone:</strong> {selectedEvent.extendedProps.milestone}</p>
            <p className="text-sm"><strong>Goal ID:</strong> {selectedEvent.extendedProps.goal_id}</p>
            <p className="text-sm"><strong>Description:</strong> {selectedEvent.extendedProps.description}</p>
            {selectedEvent.extendedProps.tags.length > 0 && (
              <p className="text-sm"><strong>Tags:</strong> {selectedEvent.extendedProps.tags.join(', ')}</p>
            )}
            {selectedEvent.extendedProps.resource.length > 0 && (
              <p className="text-sm"><strong>Resources:</strong> {selectedEvent.extendedProps.resource.join(', ')}</p>
            )}
          </div>
        ) : (
          <p className="text-gray-500">Click a task to view details.</p>
        )}
      </div>
    </div>
  );
}
