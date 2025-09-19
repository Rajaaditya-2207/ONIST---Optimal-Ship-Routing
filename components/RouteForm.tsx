import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Ship, Anchor, Navigation, Calendar } from 'lucide-react'
import { Button } from './ui/buttons'
import { Label } from './ui/layout'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { DateTimePicker } from "./ui/date-time-picker"

interface RouteFormProps {
  setSelectedRoute: (route: [number, number][]) => void
  setExplanation: (explanation: string) => void
  isNavOpen: boolean
  startPort: [number, number] | null
  endPort: [number, number] | null
  setIsSelectingLocation: (type: 'start' | 'end' | null) => void
}

export default function RouteForm({ 
  setSelectedRoute, 
  setExplanation,
  isNavOpen, 
  startPort, 
  endPort, 
  setIsSelectingLocation 
}: RouteFormProps) {
  const [shipType, setShipType] = useState('Cargo ship')
  const [departureDate, setDepartureDate] = useState<Date | undefined>(new Date())
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setExplanation('')
    setSelectedRoute([])

    if (!startPort || !endPort || !shipType || !departureDate) {
      setError("Please fill in all fields.");
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:5000/optimize_route', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          shipType,
          startPort,
          endPort,
          departureDate: departureDate.toISOString(),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSelectedRoute(data.optimized_route);
      setExplanation(data.explanation);

    } catch (err: any) {
      console.error('Error optimizing route:', err);
      setError(`Error: ${err.message}`);
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <motion.div animate={{ opacity: isNavOpen ? 1 : 0 }}>
        <Label htmlFor="shipType" className="text-lg font-semibold text-gray-700 dark:text-gray-300 flex items-center">
          <Ship className="mr-2" /> Ship Type
        </Label>
        <Select onValueChange={setShipType} value={shipType}>
          <SelectTrigger id="shipType" className="w-full mt-1">
            <SelectValue placeholder="Select Ship Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Passenger ship">Passenger Ship</SelectItem>
            <SelectItem value="Cargo ship">Cargo Ship</SelectItem>
            <SelectItem value="Tanker">Tanker</SelectItem>
          </SelectContent>
        </Select>
      </motion.div>

      <motion.div animate={{ opacity: isNavOpen ? 1 : 0 }}>
        <Label htmlFor="startPort" className="text-lg font-semibold text-gray-700 dark:text-gray-300 flex items-center">
          <Anchor className="mr-2" /> Start Port
        </Label>
        <Button type="button" onClick={() => setIsSelectingLocation('start')} className="mt-2 w-full">
          {startPort ? `Lat: ${startPort[1].toFixed(2)}, Lon: ${startPort[0].toFixed(2)}` : 'Select on Map'}
        </Button>
      </motion.div>

      <motion.div animate={{ opacity: isNavOpen ? 1 : 0 }}>
        <Label htmlFor="endPort" className="text-lg font-semibold text-gray-700 dark:text-gray-300 flex items-center">
          <Navigation className="mr-2" /> End Port
        </Label>
        <Button type="button" onClick={() => setIsSelectingLocation('end')} className="mt-2 w-full">
          {endPort ? `Lat: ${endPort[1].toFixed(2)}, Lon: ${endPort[0].toFixed(2)}` : 'Select on Map'}
        </Button>
      </motion.div>

      <motion.div animate={{ opacity: isNavOpen ? 1 : 0 }}>
        <Label htmlFor="departureDate" className="text-lg font-semibold text-gray-700 dark:text-gray-300 flex items-center">
          <Calendar className="mr-2" /> Departure Date
        </Label>
        <DateTimePicker
          date={departureDate}
          setDate={setDepartureDate}
        />
      </motion.div>

      <motion.div animate={{ opacity: isNavOpen ? 1 : 0 }}>
        <Button 
          type="submit" 
          className="w-full bg-emerald-500 hover:bg-emerald-600 text-white"
          disabled={isLoading}
        >
          {isLoading ? 'Optimizing...' : 'Calculate Optimal Route'}
        </Button>
      </motion.div>

      {error && (
        <p className="text-red-500 text-sm">{error}</p>
      )}
    </form>
  )
}
