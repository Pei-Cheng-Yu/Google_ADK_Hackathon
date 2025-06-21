import { useState } from 'react';
import api from '../api';
import TimeSlotForm from '../components/TimeSlotForm';

export default function ChatPage({ refreshGoals }) {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [showSchedule, setShowSchedule] = useState(false);
    const [canSetPlan, setCanSetPlan] = useState(false);
    const [loading, setLoading] = useState(false);
    
    const sendMessage = async (content = input, shouldRefresh = false) => {
        if (!content.trim()) return;
        const userMessage = { role: 'user', content };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);
        try {
        const res = await api.post('/run_memory_agent', { user_input: content });
        const agentMessage = { role: 'agent', content: res.data.response };
        setMessages(prev => [...prev, agentMessage]);
        if (shouldRefresh) refreshGoals();
        } catch (err) {
        console.error(err);
        alert('❌ Failed to contact agent. Try logging in again.');
        } finally {
            setLoading(false); // <-- Stop loading
        }
    };

    const handleAvailabilitySubmit = async (jsonObj) => {
        const jsonText = JSON.stringify(jsonObj, null, 2); // pretty print
        const formatted = `My availability schedule:\n\`\`\`json\n${jsonText}\n\`\`\``;
        await sendMessage(formatted);
        setCanSetPlan(true);
    };

    const sendSetPlan = async () => {
        await sendMessage('set plan');
    };

    return (
        <div className="flex flex-col h-screen p-4">
        <div className="flex-1 overflow-y-auto space-y-2 mb-4">
            {messages.map((msg, i) => (
            <div
                key={i}
                className={`p-2 rounded max-w-xl whitespace-pre-wrap ${
                msg.role === 'user'
                    ? 'ml-auto bg-blue-100 text-right'
                    : 'mr-auto bg-gray-200 text-left'
                }`}
            >
                {msg.content}
            </div>
            ))}
            {loading && (
            <div className="p-2 rounded max-w-xl mr-auto bg-gray-200 text-left italic text-gray-500">
                Agent is thinking...
            </div>
            )}
        </div>

        <div className="space-y-3">
            <div className="flex gap-2">
            <input
                className="border p-2 flex-1 rounded"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && sendMessage(input, true)}
                placeholder="Ask the agent something..."
            />
            <button
                onClick={() => sendMessage(input, true)}
                className="bg-blue-500 text-white px-4 rounded"
            >
                Send
            </button>
            </div>

            <button
            onClick={() => setShowSchedule(!showSchedule)}
            className="text-sm timeslot_form "
            >
            {showSchedule ? 'Hide availability form' : 'Set weekly availability'}
            </button>

            {showSchedule && (
            <div className="border p-3 rounded bg-gray-50 space-y-2">
                <TimeSlotForm onSubmit={handleAvailabilitySubmit} />

                <div className="flex flex-wrap gap-2">
                {canSetPlan && (
                    <button
                    onClick={sendSetPlan}
                    className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
                    >
                    🗓️ Set Plan
                    </button>
                )}
                </div>
            </div>
            )}
        </div>
        </div>
    );
}
