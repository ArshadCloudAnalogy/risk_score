import React from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { CheckCircleIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

interface PricingSuccessModalProps {
  isOpen: boolean
  onClose: () => void
  selectedPlan: string | null
}

export default function PricingSuccessModal({ isOpen, onClose, selectedPlan }: PricingSuccessModalProps) {
  const handleContinue = () => {
    // Here you would typically redirect to payment processing or next steps
    console.log('Continuing with plan:', selectedPlan)
    onClose()
  }

  return (
    <Transition appear show={isOpen} as={React.Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={React.Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={React.Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-dark-800 p-6 text-left align-middle shadow-xl transition-all border border-dark-700">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center">
                      <CheckCircleIcon className="w-6 h-6 text-white" />
                    </div>
                    <Dialog.Title as="h3" className="text-lg font-semibold text-white">
                      Plan Selected!
                    </Dialog.Title>
                  </div>
                  <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    <XMarkIcon className="w-6 h-6" />
                  </button>
                </div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="space-y-4"
                >
                  <div className="bg-dark-700 rounded-lg p-4">
                    <h4 className="font-medium text-white mb-2">You've selected:</h4>
                    <p className="text-primary-400 text-lg font-semibold">{selectedPlan} Plan</p>
                  </div>

                  <div className="space-y-3">
                    <h4 className="font-medium text-white">Next Steps:</h4>
                    <div className="space-y-2 text-sm text-gray-300">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-primary-400 rounded-full"></div>
                        <span>Complete payment setup</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-primary-400 rounded-full"></div>
                        <span>Configure your dashboard</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-primary-400 rounded-full"></div>
                        <span>Start onboarding merchants</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-primary-400 rounded-full"></div>
                        <span>Access API documentation</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-900/20 border border-blue-800 rounded-lg p-4">
                    <p className="text-blue-400 text-sm">
                      <strong>Welcome to TokenCore!</strong> Our team will reach out within 24 hours to help you get started.
                    </p>
                  </div>
                </motion.div>

                <div className="flex space-x-3 pt-6">
                  <button
                    onClick={onClose}
                    className="flex-1 btn-secondary"
                  >
                    Close
                  </button>
                  <button
                    onClick={handleContinue}
                    className="flex-1 btn-primary"
                  >
                    Continue Setup
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  )
}