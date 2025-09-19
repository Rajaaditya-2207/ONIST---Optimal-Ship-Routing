'use client';

import { motion } from 'framer-motion'
import RouteForm from './RouteForm'
import Explanation from './Explanation'
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface SidebarProps {
  isNavOpen: boolean
  setIsNavOpen: (isOpen: boolean) => void
  setSelectedRoute: (route: [number, number][]) => void
  setExplanation: (explanation: string) => void;
  startPort: [number, number] | null
  endPort: [number, number] | null
  setIsSelectingLocation: (type: 'start' | 'end' | null) => void
  explanation: string;
}

export default function Sidebar({ 
  isNavOpen, 
  setIsNavOpen, 
  setSelectedRoute, 
  setExplanation,
  startPort, 
  endPort, 
  setIsSelectingLocation,
  explanation
}: SidebarProps) {
  return (
    <motion.div 
      className={`bg-white dark:bg-gray-800 shadow-lg overflow-y-auto transition-all duration-300 ease-in-out relative ${
        isNavOpen ? 'w-96' : 'w-20'
      }`}
      initial={false}
      animate={{ width: isNavOpen ? '24rem' : '5rem' }}
    >
      <div className="p-6">
        <motion.h1 
          className="text-3xl font-bold mb-6 text-emerald-600 dark:text-emerald-400 whitespace-nowrap"
          animate={{ opacity: isNavOpen ? 1 : 0 }}
        >
          {isNavOpen ? 'Ship Route Optimizer' : 'SRO'}
        </motion.h1>
        <RouteForm
          setSelectedRoute={setSelectedRoute}
          setExplanation={setExplanation}
          isNavOpen={isNavOpen}
          startPort={startPort}
          endPort={endPort}
          setIsSelectingLocation={setIsSelectingLocation}
        />
        <Explanation explanation={explanation} isNavOpen={isNavOpen} />
      </div>
      <button
        onClick={() => setIsNavOpen(!isNavOpen)}
        className="absolute top-4 right-[-12px] bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 p-1 rounded-full shadow-md z-10 border border-gray-200 dark:border-gray-600"
      >
        {isNavOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>
    </motion.div>
  )
}
