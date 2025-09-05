import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  EllipsisVerticalIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline'
import { Menu, Transition } from '@headlessui/react'

const merchants = [
  {
    id: '1',
    name: 'TechCorp Solutions',
    email: 'admin@techcorp.com',
    status: 'active',
    riskScore: 85,
    revenue: '$125,000',
    transactions: 1247,
    joinDate: '2024-01-15',
    category: 'Technology',
    country: 'United States',
    trend: 'up',
  },
  {
    id: '2',
    name: 'Global Retail Inc',
    email: 'contact@globalretail.com',
    status: 'active',
    riskScore: 72,
    revenue: '$89,500',
    transactions: 892,
    joinDate: '2024-02-03',
    category: 'Retail',
    country: 'Canada',
    trend: 'up',
  },
  {
    id: '3',
    name: 'FinanceFirst LLC',
    email: 'info@financefirst.com',
    status: 'flagged',
    riskScore: 45,
    revenue: '$67,200',
    transactions: 534,
    joinDate: '2024-01-28',
    category: 'Finance',
    country: 'United Kingdom',
    trend: 'down',
  },
  {
    id: '4',
    name: 'HealthTech Innovations',
    email: 'support@healthtech.com',
    status: 'active',
    riskScore: 91,
    revenue: '$156,800',
    transactions: 1689,
    joinDate: '2023-12-10',
    category: 'Healthcare',
    country: 'Germany',
    trend: 'up',
  },
]

const stats = [
  { name: 'Total Merchants', value: '247', icon: ArrowTrendingUpIcon, color: 'blue' },
  { name: 'Active', value: '234', icon: CheckCircleIcon, color: 'green' },
  { name: 'Flagged', value: '13', icon: ExclamationTriangleIcon, color: 'yellow' },
  { name: 'High Risk', value: '0', icon: ArrowTrendingDownIcon, color: 'red' },
]

export default function Merchants() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('All')

  const filteredMerchants = merchants.filter((merchant) => {
    const matchesSearch = merchant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         merchant.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'All' || merchant.status === statusFilter.toLowerCase()
    return matchesSearch && matchesStatus
  })

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
        <div>
          <h1 className="text-3xl font-bold text-white">Merchants</h1>
          <p className="text-gray-400 mt-1">Manage and monitor your merchant portfolio</p>
        </div>
        <button className="btn-primary flex items-center space-x-2">
          <PlusIcon className="w-5 h-5" />
          <span>Add Merchant</span>
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-400">{stat.name}</p>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
              </div>
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                stat.color === 'blue' ? 'bg-blue-500/20' :
                stat.color === 'green' ? 'bg-green-500/20' :
                stat.color === 'yellow' ? 'bg-yellow-500/20' :
                'bg-red-500/20'
              }`}>
                <stat.icon className={`w-6 h-6 ${
                  stat.color === 'blue' ? 'text-blue-400' :
                  stat.color === 'green' ? 'text-green-400' :
                  stat.color === 'yellow' ? 'text-yellow-400' :
                  'text-red-400'
                }`} />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search merchants..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field pl-10"
          />
        </div>
        <div className="flex items-center space-x-2">
          <FunnelIcon className="w-5 h-5 text-gray-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input-field w-auto"
          >
            <option>All</option>
            <option>Active</option>
            <option>Flagged</option>
            <option>High Risk</option>
          </select>
        </div>
      </div>

      {/* Merchants Table */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="card overflow-hidden"
      >
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-dark-700">
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-400">Merchant</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-400">Status</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-400">Risk Score</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-400">Revenue</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-400">Transactions</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-400">Join Date</th>
                <th className="text-right py-4 px-6 text-sm font-medium text-gray-400">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredMerchants.map((merchant, index) => (
                <motion.tr
                  key={merchant.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border-b border-dark-700 hover:bg-dark-700/50 transition-colors"
                >
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                        <span className="text-white font-medium text-sm">
                          {merchant.name.charAt(0)}
                        </span>
                      </div>
                      <div>
                        <Link
                          to={`/merchants/${merchant.id}`}
                          className="font-medium text-white hover:text-primary-400 transition-colors"
                        >
                          {merchant.name}
                        </Link>
                        <p className="text-sm text-gray-400">{merchant.email}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <span className={`status-badge ${
                      merchant.status === 'active' ? 'status-active' :
                      merchant.status === 'flagged' ? 'status-pending' :
                      'status-rejected'
                    }`}>
                      {merchant.status}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-2">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getRiskScoreBg(merchant.riskScore)}`}>
                        <span className={`text-xs font-bold ${getRiskScoreColor(merchant.riskScore)}`}>
                          {merchant.riskScore}
                        </span>
                      </div>
                      {merchant.trend === 'up' ? (
                        <ArrowTrendingUpIcon className="w-4 h-4 text-green-400" />
                      ) : (
                        <ArrowTrendingDownIcon className="w-4 h-4 text-red-400" />
                      )}
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <span className="text-green-400 font-medium">{merchant.revenue}</span>
                  </td>
                  <td className="py-4 px-6">
                    <span className="text-white">{merchant.transactions.toLocaleString()}</span>
                  </td>
                  <td className="py-4 px-6">
                    <span className="text-gray-300">{merchant.joinDate}</span>
                  </td>
                  <td className="py-4 px-6 text-right">
                    <Menu as="div" className="relative inline-block text-left">
                      <Menu.Button className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-600 transition-colors">
                        <EllipsisVerticalIcon className="w-5 h-5" />
                      </Menu.Button>
                      <Transition
                        enter="transition ease-out duration-100"
                        enterFrom="transform opacity-0 scale-95"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-95"
                      >
                        <Menu.Items className="absolute right-0 mt-2 w-48 bg-dark-700 rounded-lg shadow-lg border border-dark-600 focus:outline-none z-10">
                          <div className="py-1">
                            <Menu.Item>
                              {({ active }) => (
                                <Link
                                  to={`/merchants/${merchant.id}`}
                                  className={`block px-4 py-2 text-sm ${
                                    active ? 'bg-dark-600 text-white' : 'text-gray-300'
                                  }`}
                                >
                                  View Details
                                </Link>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`block w-full text-left px-4 py-2 text-sm ${
                                    active ? 'bg-dark-600 text-white' : 'text-gray-300'
                                  }`}
                                >
                                  Request Rescore
                                </button>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`block w-full text-left px-4 py-2 text-sm ${
                                    active ? 'bg-dark-600 text-red-400' : 'text-red-400'
                                  }`}
                                >
                                  Suspend Account
                                </button>
                              )}
                            </Menu.Item>
                          </div>
                        </Menu.Items>
                      </Transition>
                    </Menu>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  )
}