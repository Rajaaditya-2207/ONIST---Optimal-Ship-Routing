# 🌊 ONIST - Optimal Ship Routing

**ONIST** is a full-stack web application designed to find the most efficient maritime routes.  
By considering environmental factors like wind, waves, and currents, it helps in planning **safer** and **more fuel-efficient** journeys for various types of ships.

---

## ✨ Key Features

- **Interactive Map Interface** – A user-friendly map to select start and end points for the route.  
- **Dynamic Route Optimization** – Utilizes the **A\*** algorithm to calculate the optimal path based on real-time environmental data.  
- **Support for Multiple Ship Types** – Tailored routing for passenger ships, cargo ships, and tankers.  
- **Route Visualization** – Animates the ship’s journey along the calculated path.  
- **Detailed Explanations** – Provides reasoning for suggested routes, highlighting influencing environmental factors.  
- **Nearest Port Finder** – Utility to find the closest port to a given geographical coordinate.  

---

## 🛠️ Technologies Used

### Frontend
- **Next.js**
- **React**
- **TypeScript**
- **Leaflet** (map rendering)
- **Tailwind CSS**
- **Framer Motion**

### Backend
- **Flask (Python)**
- **NumPy**
- **SciPy**
- **GeoPandas**
- **Numba**

---

## 🚀 Getting Started

Follow these steps to set up ONIST locally:

### ✅ Prerequisites
- [Node.js](https://nodejs.org/) & npm  
- [Python 3.x](https://www.python.org/) & pip  

### ⚡ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajaaditya-2207/onist---optimal-ship-routing.git
   cd onist---optimal-ship-routing
Install frontend dependencies

bash
Copy code
npm install
Install backend dependencies

bash
Copy code
pip install -r backend/requirements.txt
Run the frontend development server

bash
Copy code
npm run dev
Run the backend server

bash
Copy code
python backend/app.py
Open the application
Navigate to 👉 http://localhost:3000 in your browser.

📖 Usage
Select Ship Type – Passenger ship, cargo ship, or tanker.

Choose Start & End Ports – Click directly on the map to set departure and arrival points.

Set Departure Date – Specify your journey start date.

Calculate Route – Click “Calculate Optimal Route” to view the most efficient path.

Visualize the Journey – Use “Start Animation” to simulate the voyage.

🧠 Route Optimization
At its core, ONIST uses the A* pathfinding algorithm implemented in Python.

🔎 How it Works:
Grid Creation – The world map is divided into a grid of nodes.

Cost Calculation – Each edge cost is influenced by:

Distance – Geographical distance between nodes.

Weather – Significant wave height (SWH) and wind speed (WS) increase traversal cost.

Ship Type – Ship speed and handling characteristics.

Pathfinding – A* searches for the path with the lowest combined cost (distance + heuristic).

Land Avoidance – Landmasses are treated as impassable barriers.

Path Smoothing – The resulting path is adjusted for realistic and practical navigation.

🔮 Future Improvements
⏩ More advanced routing algorithms.

🚢 Support for more ship types and environmental factors.

📊 Enhanced data visualization in the UI.

🌐 Real-time environmental data updates.

📱 Mobile app version for on-the-go planning.

📞 Contact
For questions, feedback, or collaborations, please open an issue on the GitHub repository.
We’d love to hear from you!

