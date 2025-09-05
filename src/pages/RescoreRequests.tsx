import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  EllipsisVerticalIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline'
import { Menu, Transition } from '@headlessui/react'
import NewRescoreRequestModal from '../components/NewRescoreRequestModal'

const rescoreRequests = [
  {
    id: '1',
    merchantName: 'ABC Traders',
    requestedBy: 'John Doe',
    requestDate: 'Aug 28, 2025',
    status: 'pending',
    priority: 'high',
    currentScore: 65,
    reason: 'Spike in recent disputes',
    newScore: null,
  },
  {
    id: '2',
    merchantName: 'XYZ Enterprises',
    requestedBy: 'Jane Smith',
    requestDate: 'Aug 25, 2025',
    status: 'completed',
    priority: 'medium',
    currentScore: 78,
    reason: 'Updated financial information',
    newScore: 82,
  },
  {
    id: '3',
    merchantName: 'Tech Solutions Ltd',
    requestedBy: 'Mike Johnson',
    requestDate: 'Aug 22, 2025',
    status: 'rejected',
    priority: 'low',
    currentScore: 45,
    reason: 'Compliance review required',
    newScore: null,
  },
]

const stats = [
  { name: 'Total Requests', value: '24', color: 'blue' },
  { name: 'Pending', value: '8', color: 'yellow' },
  { name: 'Completed', value: '14', color: 'green' },
  { name: 'Rejected', value: '2', color: 'red' },
]

export default function RescoreRequests() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('All')
  const [isModalOpen, setIsModalOpen] = useState(false)

  const filteredRequests = rescoreRequests.filter((request) => {
    const matchesSearch = request.merchantName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.requestedBy.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'All' || request.status === statusFilter.toLowerCase()
    return matchesSearch && matchesStatus
  })

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <ClockIcon className="w-4 h-4 text-yellow-400" />
      case 'completed':
        return <CheckCircleIcon className="w-4 h-4 text-green-400" />
      case 'rejected':
        return <XCircleIcon className="w-4 h-4 text-red-400" />
      default:
        return null
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-900/20 text-red-400 border-red-800'
      case 'medium':
        return 'bg-yellow-900/20 text-yellow-400 border-yellow-800'
      case 'low':
        return 'bg-green-900/20 text-green-400 border-green-800'
      default:
        return 'bg-gray-900/20 text-gray-400 border-gray-800'
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Rescore Requests</h1>
          <p className="text-gray-400 mt-1">Monitor and manage merchant rescoring requests</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <PlusIcon className="w-5 h-5" />
          <span>New Rescore Request</span>
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
                stat.color === 'yellow' ? 'bg-yellow-500/20' :
                stat.color === 'green' ? 'bg-green-500/20' :
                'bg-red-500/20'
              }`}>
                <span className={`text-2xl font-bold ${
                  stat.color === 'blue' ? 'text-blue-400' :
                  stat.color === 'yellow' ? 'text-yellow-400' :
                  stat.color === 'green' ? 'text-green-400' :
                  'text-red-400'
                }`}>
                  {stat.value}
                </span>
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
            placeholder="Search requests..."
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
            <option>Pending</option>
            <option>Completed</option>
            <option>Rejected</option>
          </select>
        </div>
      </div>

      {/* Requests List */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="space-y-4"
      >
        {filteredRequests.map((request, index) => (
          <motion.div
            key={request.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card hover:bg-dark-700/50 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-medium text-sm">
                    {request.merchantName.charAt(0)}
                  </span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">{request.merchantName}</h3>
                  <p className="text-sm text-gray-400">
                    Requested by {request.requestedBy} • {request.requestDate}
                  </p>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className={`status-badge ${
                      request.status === 'pending' ? 'status-pending' :
                      request.status === 'completed' ? 'status-active' :
                      'status-rejected'
                    }`}>
                      {getStatusIcon(request.status)}
                      <span className="ml-1">{request.status}</span>
                    </span>
                    <span className={`status-badge ${getPriorityColor(request.priority)}`}>
                      {request.priority} priority
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-6">
                <div className="text-right">
                  <p className="text-sm text-gray-400">Current Score</p>
                  <p className="text-2xl font-bold text-white">{request.currentScore}</p>
                </div>
                {request.newScore && (
                  <div className="text-right">
                    <p className="text-sm text-gray-400">New Score</p>
                    <p className="text-2xl font-bold text-green-400">{request.newScore}</p>
                  </div>
                )}
                <div className="text-right">
                  <p className="text-sm text-gray-400">Reason</p>
                  <p className="text-sm text-white max-w-48">{request.reason}</p>
                </div>
                
                <Menu as="div" className="relative">
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
                            <button
                              className={`block w-full text-left px-4 py-2 text-sm ${
                                active ? 'bg-dark-600 text-white' : 'text-gray-300'
                              }`}
                            >
                              View Details
                            </button>
                          )}
                        </Menu.Item>
                        {request.status === 'pending' && (
                          <>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`block w-full text-left px-4 py-2 text-sm ${
                                    active ? 'bg-dark-600 text-green-400' : 'text-green-400'
                                  }`}
                                >
                                  Approve Request
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
                                  Reject Request
                                </button>
                              )}
                            </Menu.Item>
                          </>
                        )}
                      </div>
                    </Menu.Items>
                  </Transition>
                </Menu>
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* New Rescore Request Modal */}
      <NewRescoreRequestModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  )
}