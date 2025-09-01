# tools.py
import requests

class CalculatorTool:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


class WeatherTool:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = f"https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,weatherCode&units=metric&timesteps=1d&apikey={self.api_key}"
        try:
            response = requests.get(url)
            data = response.json()
        except Exception as e:
            return f"Error fetching weather data: {e}"

        try:
            timelines = data.get('data', {}).get('timelines', [])
            if not timelines:
                return f"No weather data found for {city}"

            intervals = timelines[0].get('intervals', [])
            if not intervals:
                return f"No weather data found for {city}"

            values = intervals[0].get('values', {})
            temp = values.get('temperature', 'N/A')
            weather = values.get('weatherCode', 'N/A')

            return f"The weather in {city} is {weather} with {temp}°C."
        except Exception as e:
            return f"Error parsing weather data: {e}"


class StringTool:
    def reverse(self, text):
        return text[::-1]

    def uppercase(self, text):
        return text.upper()
