import React from 'react';
import { TrendingUp, CheckCircle, Clock, XCircle, Mail, ArrowUp, ArrowDown } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const StatsCards = ({ stats }) => {
  const { darkMode } = useTheme();

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
      <div className={`p-6 rounded-2xl shadow-xl ${darkMode ? 'bg-gradient-to-br from-gray-800 to-gray-850' : 'bg-white'} border ${darkMode ? 'border-gray-700' : 'border-gray-100'} hover:scale-105 transition-transform duration-200`}>
        <div className="flex items-center justify-between mb-2">
          <h3 className={`text-sm font-semibold ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Total</h3>
          <TrendingUp className={`w-5 h-5 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
        </div>
        <p className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{stats.total}</p>
        <p className="text-xs text-green-500 mt-1 flex items-center">
          <ArrowUp className="w-3 h-3 mr-1" />12% this week
        </p>
      </div>
      
      <div className="p-6 rounded-2xl shadow-xl bg-gradient-to-br from-green-500 to-emerald-600 text-white hover:scale-105 transition-transform duration-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold opacity-90">Selections</h3>
          <CheckCircle className="w-5 h-5" />
        </div>
        <p className="text-3xl font-bold">{stats.selection}</p>
        <p className="text-xs opacity-80 mt-1 flex items-center">
          <ArrowUp className="w-3 h-3 mr-1" />+{stats.selection} new
        </p>
      </div>
      
      <div className="p-6 rounded-2xl shadow-xl bg-gradient-to-br from-yellow-500 to-orange-500 text-white hover:scale-105 transition-transform duration-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold opacity-90">Pending</h3>
          <Clock className="w-5 h-5" />
        </div>
        <p className="text-3xl font-bold">{stats.pending}</p>
        <p className="text-xs opacity-80 mt-1">{stats.pending} awaiting response</p>
      </div>
      
      <div className="p-6 rounded-2xl shadow-xl bg-gradient-to-br from-red-500 to-rose-600 text-white hover:scale-105 transition-transform duration-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold opacity-90">Rejections</h3>
          <XCircle className="w-5 h-5" />
        </div>
        <p className="text-3xl font-bold">{stats.rejection}</p>
        <p className="text-xs opacity-80 mt-1 flex items-center">
          <ArrowDown className="w-3 h-3 mr-1" />-8% this month
        </p>
      </div>
      
      <div className={`p-6 rounded-2xl shadow-xl ${darkMode ? 'bg-gradient-to-br from-purple-900 to-purple-800' : 'bg-gradient-to-br from-purple-500 to-indigo-600'} text-white hover:scale-105 transition-transform duration-200`}>
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold opacity-90">Unread</h3>
          <Mail className="w-5 h-5" />
        </div>
        <p className="text-3xl font-bold">{stats.unread || 0}</p>
        <p className="text-xs opacity-80 mt-1">New responses</p>
      </div>
    </div>
  );
};

export default StatsCards;