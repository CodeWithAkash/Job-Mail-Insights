import React, { useState } from 'react';
import { Search, Download, Eye, CheckCircle, XCircle, Clock, Mail } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { exportToCSV } from '../utils/exportCSV';

const EmailTable = ({ emails }) => {
  const { darkMode } = useTheme();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const filteredEmails = emails.filter(email => {
    const matchesSearch = email.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.subject.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || email.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'Rejection': return 'bg-red-500';
      case 'Selection': return 'bg-green-500';
      case 'Pending': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Rejection': return <XCircle className="w-5 h-5" />;
      case 'Selection': return <CheckCircle className="w-5 h-5" />;
      case 'Pending': return <Clock className="w-5 h-5" />;
      default: return null;
    }
  };

  return (
    <div>
      {/* Search and Filter Bar */}
      <div className={`p-6 rounded-2xl shadow-xl mb-6 ${darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-100'}`}>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className={`absolute left-4 top-3.5 w-5 h-5 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
            <input
              type="text"
              placeholder="Search companies or subjects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className={`w-full pl-12 pr-4 py-3 rounded-xl border-2 transition-all ${
                darkMode
                  ? 'bg-gray-900 border-gray-700 text-white placeholder-gray-500 focus:border-blue-500'
                  : 'bg-gray-50 border-gray-200 text-gray-900 focus:border-blue-500'
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
            />
          </div>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className={`px-6 py-3 rounded-xl border-2 font-medium transition-all ${
              darkMode
                ? 'bg-gray-900 border-gray-700 text-white focus:border-blue-500'
                : 'bg-gray-50 border-gray-200 text-gray-900 focus:border-blue-500'
            } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
          >
            <option value="all">All Status</option>
            <option value="Selection">✓ Selection</option>
            <option value="Pending">○ Pending</option>
            <option value="Rejection">✕ Rejection</option>
          </select>
          <button
            onClick={() => exportToCSV(filteredEmails)}
            className="flex items-center justify-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl font-semibold"
          >
            <Download className="w-5 h-5" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Email Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEmails.length > 0 ? (
          filteredEmails.map((email) => (
            <div 
              key={email.id}
              className={`p-6 rounded-2xl shadow-xl cursor-pointer transition-all hover:scale-105 ${
                darkMode 
                  ? 'bg-gray-800 border border-gray-700 hover:border-blue-500' 
                  : 'bg-white border border-gray-100 hover:border-blue-400'
              } ${!email.read ? 'ring-2 ring-blue-500 ring-opacity-50' : ''}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className={`w-12 h-12 rounded-xl ${getStatusColor(email.status)} flex items-center justify-center text-white shadow-lg`}>
                    {getStatusIcon(email.status)}
                  </div>
                  <div>
                    <h3 className={`font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{email.company}</h3>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{email.date}</p>
                  </div>
                </div>
                {!email.read && (
                  <span className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></span>
                )}
              </div>
              
              <h4 className={`text-sm font-semibold mb-2 line-clamp-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                {email.subject}
              </h4>
              
              <p className={`text-xs mb-4 line-clamp-2 ${darkMode ? 'text-gray-500' : 'text-gray-600'}`}>
                {email.snippet}
              </p>
              
              <div className="flex items-center justify-between">
                <span className={`px-3 py-1 rounded-lg text-xs font-semibold ${
                  email.status === 'Selection' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                  email.status === 'Pending' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                  'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                }`}>
                  {email.status}
                </span>
                <button className={`p-2 rounded-lg ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'} transition-colors`}>
                  <Eye className={`w-4 h-4 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className={`col-span-full text-center py-12 rounded-2xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
            <Mail className={`w-16 h-16 mx-auto mb-4 ${darkMode ? 'text-gray-600' : 'text-gray-400'}`} />
            <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>No emails found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailTable;