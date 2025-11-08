import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import { initiateLogin, checkAuthStatus, logout } from './utils/api';
import { Mail, Loader } from 'lucide-react';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [checking, setChecking] = useState(false);
 
  
  useEffect(() => {
    const checkAuth = async () => {
      if (checking) return;
      
      setChecking(true);
      try {
        const result = await checkAuthStatus();
        setAuthenticated(result.authenticated);
      } catch (err) {
        console.log('Not authenticated');
        setAuthenticated(false);
      } finally {
        setLoading(false);
        setChecking(false);
      }
    };

    // Check for auth callback first
    const params = new URLSearchParams(window.location.search);
    if (params.get('auth') === 'success') {
      setAuthenticated(true);
      setLoading(false);
      window.history.replaceState({}, document.title, '/');
      return;
    } else if (params.get('auth') === 'error') {
      const message = params.get('message') || 'Authentication failed';
      setError(message);
      setLoading(false);
      window.history.replaceState({}, document.title, '/');
      return;
    }

    // Only check auth once
    checkAuth();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps 

  const handleLogin = async () => {
    try {
      setError(null);
      const result = await initiateLogin();
      window.location.href = result.auth_url;
    } catch (err) {
      setError('Failed to initiate login. Please try again.');
      console.error('Login error:', err);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      setAuthenticated(false);
      window.location.reload();
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  // Initial loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600 text-lg">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // Login screen
  if (!authenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-10 max-w-md w-full text-center transform hover:scale-105 transition-transform duration-300">
          {/* Logo/Icon */}
          <div className="bg-gradient-to-br from-blue-600 to-purple-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
            <Mail className="w-10 h-10 text-white" />
          </div>

          {/* Title */}
          <h1 className="text-4xl font-bold text-gray-900 mb-3 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            JobMail Insight
          </h1>
          
          {/* Subtitle */}
          <p className="text-gray-600 mb-8 text-lg leading-relaxed">
            Connect your Gmail to analyze and track your job application emails with AI-powered insights
          </p>

          {/* Login Button */}
          <button
            onClick={handleLogin}
            disabled={!!error}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-8 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div className="flex items-center justify-center space-x-3">
              <Mail className="w-6 h-6" />
              <span>Connect Gmail Account</span>
            </div>
          </button>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-red-600 text-sm font-medium">{error}</p>
              <button
                onClick={() => setError(null)}
                className="mt-2 text-red-700 underline text-xs hover:text-red-800"
              >
                Dismiss
              </button>
            </div>
          )}

          {/* Features */}
          <div className="mt-8 pt-6 border-t border-gray-200 space-y-3">
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
              <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Smart email classification</span>
            </div>
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
              <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Beautiful analytics dashboard</span>
            </div>
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
              <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Secure & private</span>
            </div>
          </div>

          {/* Security Badge */}
          <div className="mt-6 flex items-center justify-center space-x-2 text-xs text-gray-500">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
            </svg>
            <span>Your data is encrypted and secure</span>
          </div>
        </div>
      </div>
    );
  }

  // Main application
  return (
    <ThemeProvider>
      <div className="min-h-screen">
        <Header onLogout={handleLogout} />
        <Dashboard />
      </div>
    </ThemeProvider>
  );
}

export default App;