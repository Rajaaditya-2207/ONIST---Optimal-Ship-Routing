Ship Routing Optimizer
Project Overview
A web application that optimizes ship routes within the Indian Ocean region, considering factors such as fuel efficiency, travel time, and safety. The system integrates environmental data to provide efficient and secure routes for various types of ships.

Key Features
Interactive map interface centered on the Indian Ocean region

Route optimization algorithm considering environmental factors

Integration of environmental data (significant wave height, wind speed, sea surface temperature, surface currents, salinity)

Support for different ship types (Passenger ship, Cargo ship, Tanker)

Animated route visualization

Location search functionality

Weather overlay option

Technologies Used
Frontend
Next.js, React, TypeScript

Map Integration: Leaflet, React-Leaflet

3D Rendering: Three.js

Styling: Tailwind CSS

Animation: Framer Motion

Icons: Lucide React

Date Handling: date-fns

Backend
Python

Flask

NumPy, SciPy

netCDF4 for environmental data processing

Numba for performance optimization

Project Structure
Frontend
components/:

LeafletMap.tsx: Main map component with route visualization

RouteForm.tsx: Form for inputting route parameters

ShipRoutingApp.tsx: Main application component

Sidebar.tsx: Collapsible sidebar for route input

Backend
app.py: Flask application with route optimization logic

Setup and Installation
Clone the repository:

git clone [https://github.com/your-username/ship-routing-app.git](https://github.com/your-username/ship-routing-app.git)
cd ship-routing-app

Install frontend dependencies:

npm install

Install backend dependencies:

pip install flask flask-cors netCDF4 numpy scipy numba

Run the frontend development server:

npm run dev

Run the backend server:

python backend/app.py

Open http://localhost:3000 in your browser.

Usage
Open the sidebar and select the ship type.

Choose start and end ports by clicking on the map.

Set the departure date.

Click "Calculate Optimal Route" to generate the route.

Use the "Start Animation" button to visualize the ship's journey.

Toggle the weather overlay for additional environmental information.

Route Optimization
The backend uses the Dijkstra algorithm to calculate the optimal route, considering:

Ship type and speed

Significant wave height

Wind speed

Environmental data is processed from netCDF files and interpolated to a common grid for route calculations.

Future Improvements
Implement more sophisticated routing algorithms

Add support for more ship types and environmental factors

Enhance the user interface for better data visualization

Implement real-time data updates

Develop a mobile app version

Contact
For questions or collaborations, please open an issue on our GitHub repository.