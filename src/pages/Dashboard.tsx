import React from 'react'
import { motion } from 'framer-motion'
import {
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowTrendingUpIcon,
} from '@heroicons/react/24/outline'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

const scoreHistoryData = [
  { month: 'Sep', score: 45 },
  { month: 'Oct', score: 42 },
  { month: 'Nov', score: 58 },
  { month: 'Dec', score: 48 },
  { month: 'Jan', score: 72 },
  { month: 'Feb', score: 68 },
]

const riskDistributionData = [
  { name: 'Low Risk', value: 72, color: '#10b981' },
  { name: 'Medium Risk', value: 20, color: '#f59e0b' },
  { name: 'High Risk', value: 8, color: '#ef4444' },
]

const flaggedMerchants = [
  { name: 'Merchant A', score: 62 },
  { name: 'Merchant C', score: 63 },
  { name: 'Merchant D', score: 90 },
]

const addOnModules = [
  { name: 'CancelIQ', status: 'Enabled', color: 'green' },
  { name: 'ConsentIQ', status: 'Capturing', color: 'blue' },
  { name: 'BIN Risk', status: 'Partial coverage', color: 'yellow' },
  { name: 'DPS API', status: '—', color: 'gray' },
]

const alerts = [
  {
    id: 1,
    message: '20% spike in early cancel signals - Investigate Merchant B',
    type: 'warning',
    icon: ExclamationTriangleIcon,
  },
  {
    id: 2,
    message: 'BINs flagged from 3 high-risk regions this week',
    type: 'info',
    icon: CheckCircleIcon,
  },
]

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 mt-1">Risk scoring overview and insights</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-400">Total Merchants</p>
              <p className="text-2xl font-bold text-white">247</p>
            </div>
            <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
              <ChartBarIcon className="w-6 h-6 text-blue-400" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <ArrowTrendingUpIcon className="w-4 h-4 text-green-400 mr-1" />
            <span className="text-green-400">+12%</span>
            <span className="text-gray-400 ml-1">from last month</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-400">Active Merchants</p>
              <p className="text-2xl font-bold text-white">234</p>
            </div>
            <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
              <CheckCircleIcon className="w-6 h-6 text-green-400" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-green-400">94.7%</span>
            <span className="text-gray-400 ml-1">active rate</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-400">Flagged</p>
              <p className="text-2xl font-bold text-white">13</p>
            </div>
            <div className="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center">
              <ExclamationTriangleIcon className="w-6 h-6 text-yellow-400" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-yellow-400">5.3%</span>
            <span className="text-gray-400 ml-1">require attention</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-400">Avg Risk Score</p>
              <p className="text-2xl font-bold text-white">72</p>
            </div>
            <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
              <div className="w-6 h-6 rounded-full bg-green-400 flex items-center justify-center">
                <span className="text-xs font-bold text-dark-900">72</span>
              </div>
            </div>
          </div>
          <div className="mt-4">
            <span className="text-green-400 text-sm font-medium">Low Risk</span>
          </div>
        </motion.div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Core Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-white mb-4">Core Score</h3>
          <div className="flex items-center justify-center">
            <div className="relative w-48 h-48">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskDistributionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    startAngle={180}
                    endAngle={0}
                    dataKey="value"
                  >
                    {riskDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold text-white">72</span>
                <span className="text-sm text-green-400 font-medium">Low Risk</span>
              </div>
            </div>
          </div>
          <div className="flex justify-between text-sm mt-4">
            <span className="text-gray-400">Low</span>
            <span className="text-gray-400">High</span>
          </div>
        </motion.div>

        {/* Score History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-white mb-4">Score History</h3>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={scoreHistoryData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="month" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#10b981"
                  strokeWidth={3}
                  dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Flagged Merchants */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-white mb-4">Flagged Merchants</h3>
          <div className="space-y-3">
            {flaggedMerchants.map((merchant, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-gray-300">{merchant.name}</span>
                <span className="text-white font-medium">{merchant.score}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Add-On Modules */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-white mb-4">Add-On Modules</h3>
          <div className="space-y-3">
            {addOnModules.map((module, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-gray-300">{module.name}</span>
                <span
                  className={`text-sm px-2 py-1 rounded ${
                    module.color === 'green'
                      ? 'bg-green-900/20 text-green-400'
                      : module.color === 'blue'
                      ? 'bg-blue-900/20 text-blue-400'
                      : module.color === 'yellow'
                      ? 'bg-yellow-900/20 text-yellow-400'
                      : 'bg-gray-900/20 text-gray-400'
                  }`}
                >
                  {module.status}
                </span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Alerts & Insights */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-white mb-4">Alerts & Insights</h3>
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div key={alert.id} className="flex items-start space-x-3">
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    alert.type === 'warning'
                      ? 'bg-yellow-500/20'
                      : 'bg-blue-500/20'
                  }`}
                >
                  <alert.icon
                    className={`w-4 h-4 ${
                      alert.type === 'warning' ? 'text-yellow-400' : 'text-blue-400'
                    }`}
                  />
                </div>
                <p className="text-sm text-gray-300 leading-relaxed">
                  {alert.message}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}