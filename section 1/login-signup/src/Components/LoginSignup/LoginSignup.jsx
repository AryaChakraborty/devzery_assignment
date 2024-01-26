import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import './LoginSignup.css';
import username_icon from '../Assets/username.png';
import password_icon from '../Assets/password.png';
import email_icon from '../Assets/email.png';

const LoginSignup = () => {
  const history = useHistory();
  const [action, setAction] = useState('Register');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async () => {
    console.log('Form data:', formData);

    try {
      const apiUrl = action === 'Register' ? 'http://127.0.0.1:5000/register' : 'http://127.0.0.1:5000/login';

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'access-control-allow-origin': '*',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        // Redirect to the profile page after successful login
        history.push('/profile');
      }

      document.getElementById('result').innerHTML = data.message;

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error during API call:', error.message);
    }
  };

  return (
    <div className="container">
      <div className="submit-container">
        <div className={`submit ${action === 'Login' ? 'gray' : ''}`} onClick={() => setAction('Register')}>
          Register
        </div>
        <div className={`submit ${action === 'Register' ? 'gray' : ''}`} onClick={() => setAction('Login')}>
          Login
        </div>
      </div>

      <div className="inputs">
        {action === 'Login' ? null : (
          <div className="input">
            <img src={username_icon} alt="" />
            <input type="text" name="username" placeholder="username" value={formData.username} onChange={handleChange} required />
          </div>
        )}

        <div className="input">
          <img src={email_icon} alt="" />
          <input type="email" name="email" placeholder="email id" value={formData.email} onChange={handleChange} required />
        </div>

        <div className="input">
          <img src={password_icon} alt="" />
          <input type="password" name="password" placeholder="password" value={formData.password} onChange={handleChange} required />
        </div>
      </div>

      <div className="submit-container">
        <div className="submit pink" onClick={handleSubmit}>
          Go!!
        </div>
      </div>

      <p id="result" className="result-login-signup"></p>
    </div>
  );
};

export default LoginSignup;
