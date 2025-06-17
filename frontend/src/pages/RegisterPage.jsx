import { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      await api.post('/signup', { username, password });
      alert('✅ Registration successful! Please log in.');
      navigate('/login');
    } catch (err) {
      alert('Register failed');
    }
  };

  return (
    <div className="flex justify-center items-center w-screen ">
    <div className="p-8 max-w-md mx-auto ">
      <h2 className="text-xl font-bold mb-4">Register</h2>
      <input className="border p-2 w-full mb-4" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input className="border p-2 w-full mb-4" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button className="bg-green-500 text-black px-4 py-2 rounded" onClick={handleRegister}>Register</button>
      <p className="text-sm mt-4">
        Already have an account? <a href="/login" className="text-blue-500 underline">Login</a>
        </p>
    </div>
    </div>
  );
}
