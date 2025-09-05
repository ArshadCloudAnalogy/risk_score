import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ArrowLeftIcon,
  BuildingOfficeIcon,
  EnvelopeIcon,
  PhoneIcon,
  GlobeAltIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
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

// Mock data - in real app, fetch based on ID
const merchantData = {
  id: '1',
  name: 'TechCorp Solutions',
  email: 'admin@techcorp.com',
  phone: '+1 (555) 123-4567',
  website: 'https://techcorp.com',
  status: 'active',
  riskScore: 85,
  tier: 'Hot',
  decision: 'Approve',
  joinDate: '2024-01-15',
  category: 'Technology',
  country: 'United States',
  revenue: '$125,000',
  transactions: 1247,
  profile: {
    businessAddress: '123 Tech Street, San Francisco, CA 94105',
    contactName: 'John Smith',
    contactTitle: 'CEO',
    ein: '12-3456789',
    mid: 'MID123456',
    mcc: '5734',
  },
}

const scoreHistoryData = [
  { month: 'Jan', score: 78 },
  { month: 'Feb', score: 82 },
  { month: 'Mar', score: 79 },
  { month: 'Apr', score: 85 },
  { month: 'May', score: 83 },
  { month: 'Jun', score: 85 },
]

const riskFactors = [
  { name: 'Credit Score', value: 25, color: '#10b981' },
  { name: 'Transaction History', value: 30, color: '#3b82f6' },
  { name: 'Industry Risk', value: 20, color: '#f59e0b' },
  { name: 'Fraud Indicators', value: 15, color: '#ef4444' },
  { name: 'Other Factors', value: 10, color: '#8b5cf6' },
]

const recentActivity = [
  {
    id: '1',
    type: 'score_update',
    message: 'Risk score updated from 83 to 85',
    timestamp: '2 hours ago',
    icon: ChartBarIcon,
    color: 'text-green-400',
  },
  {
    id: '2',
    type: 'transaction',
    message: 'Large transaction processed: $15,000',
    timestamp: '1 day ago',
    icon: BuildingOfficeIcon,
    color: 'text-blue-400',
  },
  {
    id: '3',
    type: 'alert',
    message: 'Unusual transaction pattern detected',
    timestamp: '3 days ago',
    icon: ExclamationTriangleIcon,
    color: 'text-yellow-400',
  },
]

export default function MerchantDetail() {
  const { id } = useParams()

  const getRiskScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400'
    if (score >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getRiskScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-900/20'
    if (score >= 60) return 'bg-yellow-900/20'
    return 'bg-red-900/20'
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/merchants"
            className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-700 transition-colors"
          >
            <ArrowLeftIcon className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-white">{merchantData.name}</h1>
            <p className="text-gray-400 mt-1">Merchant Details & Risk Analysis</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary">Request Rescore</button>
          <button className="btn-primary">Edit Merchant</button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-400">Risk Score</p>
              <p className="text-2xl font-bold text-white">{merchantData.riskScore}</p>
              <p className={`text-sm font-medium ${getRiskScoreColor(merchantData.riskScore)}`}>
                {merchantData.tier}
              </p>
            </div>
            <div className={`w-16 h-16 rounded-full flex items-center justify-center ${getRiskScoreBg(merchantData.riskScore)}`}>
              <span className={`text-xl font-bold ${getRiskScoreColor(merchantData.riskScore)}`}>
                {merchantData.riskScore}
              </span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div>
            <p className="text-sm font-medium text-gray-400">Revenue</p>
            <p className="text-2xl font-bold text-green-400">{merchantData.revenue}</p>
            <p className="text-sm text-gray-400 mt-1">Monthly</p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div>
            <p className="text-sm font-medium text-gray-400">Transactions</p>
            <p className="text-2xl font-bold text-white">{merchantData.transactions.toLocaleString()}</p>
            <p className="text-sm text-gray-400 mt-1">This month</p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <div>
            <p className="text-sm font-medium text-gray-400">Status</p>
            <span className={`status-badge ${
              merchantData.status === 'active' ? 'status-active' : 'status-pending'
            } mt-2`}>
              {merchantData.status}
            </span>
            <p className="text-sm text-gray-400 mt-2">Since {merchantData.joinDate}</p>
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Merchant Information */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Merchant Information</h2>
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <EnvelopeIcon className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-400">Email</p>
                <p className="text-white">{merchantData.email}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <PhoneIcon className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-400">Phone</p>
                <p className="text-white">{merchantData.phone}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <GlobeAltIcon className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-400">Website</p>
                <a href={merchantData.website} className="text-primary-400 hover:text-primary-300">
                  {merchantData.website}
                </a>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <BuildingOfficeIcon className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-400">Business Address</p>
                <p className="text-white">{merchantData.profile.businessAddress}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 pt-4 border-t border-dark-700">
              <div>
                <p className="text-sm text-gray-400">EIN</p>
                <p className="text-white">{merchantData.profile.ein}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">MID</p>
                <p className="text-white">{merchantData.profile.mid}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">MCC</p>
                <p className="text-white">{merchantData.profile.mcc}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Category</p>
                <p className="text-white">{merchantData.category}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="flex items-start space-x-3 p-3 bg-dark-700 rounded-lg"
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center bg-dark-600`}>
                  <activity.icon className={`w-4 h-4 ${activity.color}`} />
                </div>
                <div className="flex-1">
                  <p className="text-white text-sm">{activity.message}</p>
                  <p className="text-gray-400 text-xs mt-1">{activity.timestamp}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Score History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Score History</h2>
          <div className="h-64">
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

        {/* Risk Factors */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Risk Factors</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskFactors}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                  labelLine={false}
                >
                  {riskFactors.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
    </div>
  )
}