import { useState } from 'react';
import api from '../api'; // use the configured instance
import { Link , useNavigate} from 'react-router-dom';
export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const handleLogin = async () => {
    try {
       const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const res = await api.post('/login', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        });
      localStorage.setItem('token', res.data.access_token);
      alert('✅ Login successful');
      onLogin(); 
      navigate('/'); 
    } catch (err) {
      alert('Login failed');
    }
  };

  return (
    <div className="flex justify-center items-center w-screen ">
    <div className="p-8 max-w-md mx-auto justify-center">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        className="border p-2 w-full mb-4"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        className="border p-2 w-full mb-4"
      />
      <button onClick={handleLogin} className="bg-blue-500 text-black px-4 py-2 rounded">
        Login
      </button>
      <p className="text-sm mt-4">
    Don't have an account? <Link to="/register" className="text-blue-500 underline">Register</Link>
  </p>
    </div>
    </div>
    
  );
}
