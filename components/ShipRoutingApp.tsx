'use client';

import { useState, useCallback } from 'react'
import dynamic from 'next/dynamic'
import Sidebar from './Sidebar'

const LeafletMap = dynamic(() => import('./LeafletMap'), {
  ssr: false,
  loading: () => <p>Loading map...</p>
})

const DEFAULT_CENTER: [number, number] = [78.9629, 20.5937] // [lon, lat] for India
const DEFAULT_ZOOM = 5

export default function ShipRoutingApp() {
  const [isNavOpen, setIsNavOpen] = useState(true)
  const [selectedRoute, setSelectedRoute] = useState<[number, number][] | null>(null)
  const [startPort, setStartPort] = useState<[number, number] | null>(null)
  const [endPort, setEndPort] = useState<[number, number] | null>(null)
  const [isSelectingLocation, setIsSelectingLocation] = useState<'start' | 'end' | null>(null)
  const [zoomToLocation, setZoomToLocation] = useState<[number, number] | null>(null)
  const [explanation, setExplanation] = useState<string>('');

  const handleLocationSelect = (location: [number, number]) => {
    if (isSelectingLocation === 'start') {
      setStartPort(location)
      setIsSelectingLocation(null)
    } else if (isSelectingLocation === 'end') {
      setEndPort(location)
      setIsSelectingLocation(null)
    }
    setZoomToLocation(location)
  }

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar
        isNavOpen={isNavOpen}
        setIsNavOpen={setIsNavOpen}
        setSelectedRoute={setSelectedRoute}
        setExplanation={setExplanation}
        startPort={startPort}
        endPort={endPort}
        setIsSelectingLocation={setIsSelectingLocation}
        explanation={explanation}
      />
      <main className="flex-1 relative">
        <LeafletMap
          route={selectedRoute}
          startPort={startPort}
          endPort={endPort}
          isSelectingLocation={isSelectingLocation}
          onLocationSelect={handleLocationSelect}
          zoomToLocation={zoomToLocation}
          defaultCenter={DEFAULT_CENTER}
          defaultZoom={DEFAULT_ZOOM}
        />
      </main>
    </div>
  )
}
