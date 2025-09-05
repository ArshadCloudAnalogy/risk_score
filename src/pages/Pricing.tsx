import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  CheckIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import PricingSuccessModal from '../components/PricingSuccessModal'

const plans = [
  {
    name: 'Starter',
    description: 'Perfect for getting started with core features',
    price: 350,
    features: [
      'Base SaaS subscription (includes up to 2 MIDs)',
      '$0.05 per transaction fee',
      'Dashboard & API Access',
      'Basic Risk Scoring & Monitoring',
      'Email Support (M-F business hours)',
      '1 Add-On Module included (e.g. TokenIQ Lite or ConsentIQ)',
    ],
    notIncluded: [
      'Priority Email Support',
      'Compliance Pack',
      'Advanced Analytics',
      'Multiple Add-On Modules',
    ],
    buttonText: 'Choose Starter',
    popular: false,
  },
  {
    name: 'Growth',
    description: 'For scaling businesses that need compliance and advanced tools',
    price: 575,
    features: [
      'All Starter features',
      'Priority Email Support',
      'Compliance Pack (2 Assessments included)',
      'Advanced Analytics',
      '3 Add-On Modules included (e.g. CancelIQ, DisputeIQ, BIN Risk Scoring)',
    ],
    notIncluded: [
      'Dedicated Support',
      'Unlimited Projects / MIDs',
      'Custom Integrations',
      'Team Collaboration Tools',
    ],
    buttonText: 'Choose Growth',
    popular: true,
  },
  {
    name: 'Enterprise',
    description: 'Full suite for large-scale operations',
    price: 775,
    features: [
      'All Growth features',
      'Dedicated Support',
      'Unlimited Projects / MIDs',
      'Custom Integrations',
      'Team Collaboration Tools',
      'All Add-On Modules included',
    ],
    notIncluded: [],
    buttonText: 'Choose Enterprise',
    popular: false,
  },
]

export default function Pricing() {
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const handlePlanSelect = (planName: string) => {
    setSelectedPlan(planName)
    setIsModalOpen(true)
  }

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">Choose Your Plan</h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Select the plan that best fits your needs
        </p>
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
        {plans.map((plan, index) => (
          <motion.div
            key={plan.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`relative card ${
              plan.popular
                ? 'ring-2 ring-primary-500 bg-gradient-to-b from-dark-800 to-dark-900'
                : ''
            }`}
          >
            {plan.popular && (
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-primary-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                  Most Popular
                </span>
              </div>
            )}

            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
              <p className="text-gray-400 mb-4">{plan.description}</p>
              <div className="flex items-baseline justify-center">
                <span className="text-5xl font-bold text-white">${plan.price}</span>
                <span className="text-gray-400 ml-2">/month</span>
              </div>
            </div>

            <div className="space-y-4 mb-8">
              {plan.features.map((feature, featureIndex) => (
                <div key={featureIndex} className="flex items-start space-x-3">
                  <CheckIcon className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-300 text-sm leading-relaxed">{feature}</span>
                </div>
              ))}
              {plan.notIncluded.map((feature, featureIndex) => (
                <div key={featureIndex} className="flex items-start space-x-3 opacity-50">
                  <XMarkIcon className="w-5 h-5 text-gray-500 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-500 text-sm leading-relaxed line-through">
                    {feature}
                  </span>
                </div>
              ))}
            </div>

            <button
              onClick={() => handlePlanSelect(plan.name)}
              className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                plan.popular
                  ? 'bg-primary-600 hover:bg-primary-700 text-white'
                  : 'bg-dark-600 hover:bg-dark-500 text-white'
              }`}
            >
              {plan.buttonText}
            </button>
          </motion.div>
        ))}
      </div>

      {/* Additional Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="text-center space-y-4"
      >
        <p className="text-gray-400">
          All plans include our core risk scoring engine and 24/7 system monitoring
        </p>
        <p className="text-sm text-gray-500">
          Need a custom solution? <a href="#" className="text-primary-400 hover:text-primary-300">Contact our sales team</a>
        </p>
      </motion.div>

      {/* Pricing Success Modal */}
      <PricingSuccessModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        selectedPlan={selectedPlan}
      />
    </div>
  )
}