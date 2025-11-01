import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';
import { useTheme } from '../context/ThemeContext';

const Charts = ({ stats }) => {
  const { darkMode } = useTheme();

  const pieData = [
    { name: 'Selection', value: stats.selection, color: '#10b981' },
    { name: 'Pending', value: stats.pending, color: '#f59e0b' },
    { name: 'Rejection', value: stats.rejection, color: '#ef4444' },
  ];

  // Mock trend data - you can fetch this from backend later
  const trendData = [
    { month: 'Jun', applications: 15, responses: 8 },
    { month: 'Jul', applications: 22, responses: 12 },
    { month: 'Aug', applications: 28, responses: 18 },
    { month: 'Sep', applications: 25, responses: 15 },
    { month: 'Oct', applications: stats.total, responses: stats.selection + stats.rejection },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <div className={`lg:col-span-2 p-6 rounded-2xl shadow-xl ${darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-100'}`}>
        <h3 className={`text-lg font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          Application Trends
        </h3>
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={trendData}>
            <defs>
              <linearGradient id="colorApps" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorResp" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
            <XAxis dataKey="month" stroke={darkMode ? '#9ca3af' : '#6b7280'} />
            <YAxis stroke={darkMode ? '#9ca3af' : '#6b7280'} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: darkMode ? '#1f2937' : '#fff', 
                border: 'none', 
                borderRadius: '12px', 
                boxShadow: '0 10px 40px rgba(0,0,0,0.1)' 
              }} 
            />
            <Legend />
            <Area type="monotone" dataKey="applications" stroke="#3b82f6" fillOpacity={1} fill="url(#colorApps)" name="Applications" />
            <Area type="monotone" dataKey="responses" stroke="#10b981" fillOpacity={1} fill="url(#colorResp)" name="Responses" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className={`p-6 rounded-2xl shadow-xl ${darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-100'}`}>
        <h3 className={`text-lg font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          Status Distribution
        </h3>
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie 
              data={pieData} 
              cx="50%" 
              cy="50%" 
              labelLine={false}
              outerRadius={90}
              innerRadius={50}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            >
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;