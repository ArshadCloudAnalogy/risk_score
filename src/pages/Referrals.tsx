import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  UserGroupIcon,
  GiftIcon,
  ShareIcon,
  ClipboardDocumentIcon,
  CheckIcon,
} from '@heroicons/react/24/outline'

const referralStats = [
  { name: 'Total Referrals', value: '24', color: 'blue' },
  { name: 'Active Referrals', value: '18', color: 'green' },
  { name: 'Pending Rewards', value: '$2,400', color: 'yellow' },
  { name: 'Total Earned', value: '$8,750', color: 'purple' },
]

const recentReferrals = [
  {
    id: '1',
    name: 'TechStart Inc.',
    email: 'admin@techstart.com',
    status: 'active',
    joinDate: '2024-01-15',
    reward: '$500',
    tier: 'Growth',
  },
  {
    id: '2',
    name: 'Digital Solutions LLC',
    email: 'contact@digitalsolutions.com',
    status: 'pending',
    joinDate: '2024-01-20',
    reward: '$350',
    tier: 'Starter',
  },
  {
    id: '3',
    name: 'Enterprise Corp',
    email: 'info@enterprisecorp.com',
    status: 'active',
    joinDate: '2024-01-10',
    reward: '$775',
    tier: 'Enterprise',
  },
]

const rewardTiers = [
  {
    tier: 'Starter',
    reward: '$350',
    description: 'For each Starter plan referral',
    color: 'bg-blue-500/20 text-blue-400',
  },
  {
    tier: 'Growth',
    reward: '$500',
    description: 'For each Growth plan referral',
    color: 'bg-green-500/20 text-green-400',
  },
  {
    tier: 'Enterprise',
    reward: '$775',
    description: 'For each Enterprise plan referral',
    color: 'bg-purple-500/20 text-purple-400',
  },
]

export default function Referrals() {
  const [referralCode] = useState('TOKENCORE-REF-2024')
  const [copied, setCopied] = useState(false)

  const copyReferralCode = () => {
    navigator.clipboard.writeText(referralCode)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const shareReferralLink = () => {
    const referralLink = `https://tokencore.com/signup?ref=${referralCode}`
    navigator.clipboard.writeText(referralLink)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-white mb-2">Referral Program</h1>
        <p className="text-gray-400">
          Earn rewards by referring new merchants to TokenCore
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {referralStats.map((stat, index) => (
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
                'bg-purple-500/20'
              }`}>
                <GiftIcon className={`w-6 h-6 ${
                  stat.color === 'blue' ? 'text-blue-400' :
                  stat.color === 'green' ? 'text-green-400' :
                  stat.color === 'yellow' ? 'text-yellow-400' :
                  'text-purple-400'
                }`} />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Referral Code & Sharing */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-6"
        >
          {/* Your Referral Code */}
          <div className="card">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <ShareIcon className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-xl font-semibold text-white">Your Referral Code</h2>
            </div>
            
            <div className="bg-dark-700 rounded-lg p-4 mb-4">
              <div className="flex items-center justify-between">
                <code className="text-primary-400 font-mono text-lg">{referralCode}</code>
                <button
                  onClick={copyReferralCode}
                  className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors"
                >
                  {copied ? (
                    <CheckIcon className="w-5 h-5 text-green-400" />
                  ) : (
                    <ClipboardDocumentIcon className="w-5 h-5" />
                  )}
                  <span className="text-sm">{copied ? 'Copied!' : 'Copy'}</span>
                </button>
              </div>
            </div>

            <button
              onClick={shareReferralLink}
              className="w-full btn-primary flex items-center justify-center space-x-2"
            >
              <ShareIcon className="w-5 h-5" />
              <span>Share Referral Link</span>
            </button>
          </div>

          {/* Reward Tiers */}
          <div className="card">
            <h2 className="text-xl font-semibold text-white mb-4">Reward Tiers</h2>
            <div className="space-y-3">
              {rewardTiers.map((tier, index) => (
                <motion.div
                  key={tier.tier}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  className="flex items-center justify-between p-3 bg-dark-700 rounded-lg"
                >
                  <div>
                    <h3 className="font-medium text-white">{tier.tier} Plan</h3>
                    <p className="text-sm text-gray-400">{tier.description}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${tier.color}`}>
                    {tier.reward}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Recent Referrals */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
              <UserGroupIcon className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-xl font-semibold text-white">Recent Referrals</h2>
          </div>

          <div className="space-y-4">
            {recentReferrals.map((referral, index) => (
              <motion.div
                key={referral.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                className="flex items-center justify-between p-4 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium text-sm">
                      {referral.name.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-medium text-white">{referral.name}</h3>
                    <p className="text-sm text-gray-400">{referral.email}</p>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-gray-300">{referral.tier}</span>
                      <span
                        className={`status-badge ${
                          referral.status === 'active' ? 'status-active' : 'status-pending'
                        }`}
                      >
                        {referral.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-green-400">{referral.reward}</p>
                  <p className="text-sm text-gray-400">Joined: {referral.joinDate}</p>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="mt-6 text-center">
            <button className="text-primary-400 hover:text-primary-300 text-sm font-medium">
              View All Referrals
            </button>
          </div>
        </motion.div>
      </div>

      {/* How It Works */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-white mb-6 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-xl">1</span>
            </div>
            <h3 className="font-medium text-white mb-2">Share Your Code</h3>
            <p className="text-sm text-gray-400">
              Share your unique referral code with potential merchants
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-xl">2</span>
            </div>
            <h3 className="font-medium text-white mb-2">They Sign Up</h3>
            <p className="text-sm text-gray-400">
              New merchants sign up using your referral code
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-xl">3</span>
            </div>
            <h3 className="font-medium text-white mb-2">Earn Rewards</h3>
            <p className="text-sm text-gray-400">
              Receive rewards based on their chosen plan
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}