import React, { useState, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import StatsCards from './StatsCards';
import Charts from './Charts';
import EmailTable from './EmailTable';
import { fetchEmails, fetchStats } from '../utils/api';
import { Loader, AlertCircle, RefreshCw } from 'lucide-react';

const Dashboard = () => {
  const { darkMode } = useTheme();
  const [emails, setEmails] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    rejection: 0,
    selection: 0,
    pending: 0,
    unread: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async (forceRefresh = false) => {
    try {
      if (forceRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(null);

      const [emailsData, statsData] = await Promise.all([
        fetchEmails(forceRefresh),
        fetchStats()
      ]);

      setEmails(emailsData.emails || []);
      setStats(statsData);
    } catch (err) {
      console.error('Error loading data:', err);
      setError(err.response?.data?.error || err.message || 'Failed to load data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    loadData(true);
  };

  if (loading) {
    return (
      <div className={`min-h-screen flex items-center justify-center ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <div className="text-center">
          <Loader className={`w-16 h-16 animate-spin mx-auto mb-4 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
          <h3 className={`text-xl font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Loading Your Emails
          </h3>
          <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            Fetching and analyzing your job applications...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`min-h-screen flex items-center justify-center p-6 ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <div className={`max-w-md w-full p-8 rounded-2xl shadow-xl ${darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white'}`}>
          <div className="flex items-center justify-center w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/30 mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-red-600 dark:text-red-400" />
          </div>
          <h3 className={`text-xl font-bold text-center mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Oops! Something went wrong
          </h3>
          <p className={`text-center mb-6 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            {error}
          </p>
          <button
            onClick={() => loadData(true)}
            className="w-full flex items-center justify-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg font-semibold"
          >
            <RefreshCw className="w-5 h-5" />
            <span>Try Again</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900' : 'bg-gradient-to-br from-blue-50 via-white to-purple-50'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Refresh Indicator */}
        {refreshing && (
          <div className={`mb-6 p-4 rounded-xl ${darkMode ? 'bg-blue-900/30 border border-blue-800' : 'bg-blue-50 border border-blue-200'} flex items-center space-x-3`}>
            <Loader className={`w-5 h-5 animate-spin ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
            <span className={`font-medium ${darkMode ? 'text-blue-300' : 'text-blue-700'}`}>
              Refreshing your emails...
            </span>
          </div>
        )}

        {/* Stats Section */}
        <StatsCards stats={stats} />

        {/* Charts Section */}
        <Charts stats={stats} />

        {/* Email Table Section */}
        <EmailTable emails={emails} onRefresh={handleRefresh} />

        {/* Empty State */}
        {emails.length === 0 && !loading && (
          <div className={`mt-8 p-12 rounded-2xl shadow-xl text-center ${darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white'}`}>
            <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
              <svg className={`w-12 h-12 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className={`text-2xl font-bold mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              No Job Emails Found
            </h3>
            <p className={`mb-6 text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              We haven't found any job-related emails in your inbox yet.
            </p>
            <button
              onClick={handleRefresh}
              className="inline-flex items-center space-x-2 px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl font-semibold"
            >
              <RefreshCw className="w-5 h-5" />
              <span>Refresh Emails</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;