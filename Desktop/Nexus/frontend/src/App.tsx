import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import { AuthProvider } from './store/authStore'
import { UIProvider } from './store/uiStore'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import JobList from './pages/jobs/JobList'
import JobDetail from './pages/jobs/JobDetail'
import PostJob from './pages/jobs/PostJob'
import LearningRoadmap from './pages/learning/Roadmap'
import RoadmapView from './pages/learning/RoadmapView'
import Course from './pages/learning/Course'
import Progress from './pages/learning/Progress'
import MarketList from './pages/market/MarketList'
import ProductDetail from './pages/market/ProductDetail'
import SellProduct from './pages/market/SellProduct'
import Profile from './pages/profile/Profile'
import Portfolio from './pages/profile/Portfolio'

function AppRoutes() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/jobs" element={<JobList />} />
        <Route path="/jobs/new" element={<PostJob />} />
        <Route path="/jobs/:id" element={<JobDetail />} />
        <Route path="/learning" element={<LearningRoadmap />} />
        <Route path="/learning/roadmap/:id" element={<RoadmapView />} />
        <Route path="/learning/course/:id" element={<Course />} />
        <Route path="/learning/progress" element={<Progress />} />
        <Route path="/market" element={<MarketList />} />
        <Route path="/market/sell" element={<SellProduct />} />
        <Route path="/market/:id" element={<ProductDetail />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/profile/portfolio" element={<Portfolio />} />
        <Route path="*" element={<Home />} />
      </Route>
    </Routes>
  )
}

export default function App() {
  return (
    <UIProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </UIProvider>
  )
}
