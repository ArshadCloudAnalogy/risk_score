import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Merchants from './pages/Merchants'
import RescoreRequests from './pages/RescoreRequests'
import Onboarding from './pages/Onboarding'
import Pricing from './pages/Pricing'
import Referrals from './pages/Referrals'
import MerchantDetail from './pages/MerchantDetail'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/merchants" element={<Merchants />} />
          <Route path="/merchants/:id" element={<MerchantDetail />} />
          <Route path="/rescore-requests" element={<RescoreRequests />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/referrals" element={<Referrals />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App