import React from 'react';
import { Mail, Moon, Sun, RefreshCw, LogOut } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const Header = ({ onLogout, onRefresh, loading }) => {
  const { darkMode, toggleTheme } = useTheme();

  return (
    <div className={`sticky top-0 z-50 backdrop-blur-xl border-b ${darkMode ? 'bg-gray-900/80 border-gray-800' : 'bg-white/80 border-gray-200'} shadow-lg`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo Section */}
          <div className="flex items-center space-x-4">
            <div className={`p-2 rounded-xl ${darkMode ? 'bg-gradient-to-br from-blue-600 to-purple-600' : 'bg-gradient-to-br from-blue-500 to-purple-500'} shadow-lg`}>
              <Mail className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                JobMail Insight
              </h1>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                Track your job applications
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3">
            {onRefresh && (
              <button
                onClick={onRefresh}
                disabled={loading}
                className={`p-2.5 rounded-xl ${darkMode ? 'bg-gray-800 text-gray-300 hover:bg-gray-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed`}
                title="Refresh emails"
              >
                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
              </button>
            )}
            
            <button
              onClick={toggleTheme}
              className={`p-2.5 rounded-xl ${darkMode ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-all shadow-md hover:shadow-lg`}
              title="Toggle theme"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {onLogout && (
              <button
                onClick={onLogout}
                className={`p-2.5 rounded-xl ${darkMode ? 'bg-gray-800 text-red-400 hover:bg-gray-700' : 'bg-gray-100 text-red-600 hover:bg-gray-200'} transition-all shadow-md hover:shadow-lg`}
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;