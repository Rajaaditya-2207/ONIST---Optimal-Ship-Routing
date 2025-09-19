import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    # If no API key is present, we keep the module importable but
    # `get_path_explanation` will return a helpful message.
    print("Warning: GEMINI_API_KEY not set. Gemma explanations will be disabled.")

# Configure the generative AI model with the API key
# It is highly recommended to use environment variables for API keys in production
# from dotenv import load_dotenv
# load_dotenv()
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# For demonstration, the API key can be set directly, but this is not secure
# Replace "YOUR_API_KEY" with your actual Google AI API key
#API_KEY = "YOUR_API_KEY"
#if API_KEY == "YOUR_API_KEY":
#   print("Warning: API key is not set. Please replace 'YOUR_API_KEY' with your actual key.")
#else:
#    genai.configure(api_key=API_KEY)


def get_path_explanation(route_data, maritime_data):
    """
    Generates an explanation for the optimal ship route using the Gemma 3 1B model.

    Args:
        route_data (dict): A dictionary containing details about the calculated route.
        maritime_data (dict): A dictionary containing the simulated maritime data used for routing.

    Returns:
        str: A string containing the explanation for the route changes.
    """
    if not API_KEY:
        return "API key not configured. Cannot generate explanation."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Analyze the following ship routing data and explain why the optimal path changes.
        The explanation should be concise, easy to understand for a non-expert, and highlight the key maritime factors influencing the route.

        Route Details:
        - Start Port: {route_data.get('start_port')}
        - End Port: {route_data.get('end_port')}
        - Total Distance: {route_data.get('distance_km', 'N/A')} km
        - Waypoints: {len(route_data.get('path', []))}

        Key Maritime Data Influencing the Route:
        - Significant Wave Height (avg): {maritime_data.get('avg_swh', 'N/A')} meters
        - Wind Speed (avg): {maritime_data.get('avg_wind_speed', 'N/A')} knots
        - Ocean Current Speed (avg): {maritime_data.get('avg_current_speed', 'N/A')} knots
        - Presence of Adverse Weather: {'Yes' if maritime_data.get('adverse_weather', False) else 'No'}

        Based on this data, explain the primary reasons for the chosen path, focusing on how the ship avoids hazards and leverages favorable conditions.
        For example: "The route deviates eastward to avoid a region of high waves (average {maritime_data.get('avg_swh')}m), then takes advantage of a favorable current..."
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"An error occurred while generating the explanation: {e}")
        return "Error: Could not generate an explanation for the route."
