# agents.py
import re
from tools import CalculatorTool, WeatherTool, StringTool
from transformers import pipeline

# ---------------- Calculator Agent ----------------
class CalculatorAgent:
    def __init__(self):
        self.tool = CalculatorTool()

    def perform_task(self, request: str):
        if any(word in request.lower() for word in ["add", "plus", "+", "multiply", "times", "*"]):
            numbers = list(map(int, re.findall(r'\d+', request)))
            if len(numbers) < 2:
                return "Not enough numbers for calculator"
            if any(word in request.lower() for word in ["add", "+", "sum", "plus"]):
                return self.tool.add(*numbers[:2])
            if any(word in request.lower() for word in ["multiply", "*", "times"]):
                return self.tool.multiply(*numbers[:2])
        return None


# ---------------- Weather Agent ----------------
class WeatherAgent:
    def __init__(self, api_key: str):
        self.tool = WeatherTool(api_key)

    def perform_task(self, request: str):
        if "weather" in request.lower():
            city_match = re.search(r'weather in ([\w\s]+)', request, re.IGNORECASE)
            if city_match:
                city = city_match.group(1).strip()
                return self.tool.get_weather(city)
            else:
                return "Please specify a city."
        return None


# ---------------- String Agent ----------------
class StringAgent:
    def __init__(self):
        self.tool = StringTool()

    def perform_task(self, request: str):
        if "reverse" in request.lower():
            text = request.replace("reverse", "").strip()
            return self.tool.reverse(text)
        elif "uppercase" in request.lower():
            text = request.replace("uppercase", "").strip()
            return self.tool.uppercase(text)
        return None


# ---------------- LLM Agent (Fallback) ----------------
class LLMAgent:
    def __init__(self):
        self.pipe = None  # lazy load

    def perform_task(self, request: str):
        try:
            if self.pipe is None:
                from transformers import pipeline
                self.pipe = pipeline("text2text-generation", model="google/flan-t5-base")

            response = self.pipe(request, max_length=200, num_return_sequences=1)

            # 🔹 Debugging: print raw Hugging Face output to terminal
            print("LLM raw response:", response)

            # Safely extract text
            if response and "generated_text" in response[0]:
                return response[0]["generated_text"]
            elif response and "summary_text" in response[0]:  # sometimes used
                return response[0]["summary_text"]
            else:
                return str(response)
        except Exception as e:
            return f"LLM error: {e}"



# ---------------- Master Agent ----------------
class MasterAgent:
    def __init__(self, weather_api_key: str):
        self.agents = [
            CalculatorAgent(),
            WeatherAgent(weather_api_key),
            StringAgent(),
            LLMAgent()  # ✅ add fallback
        ]

    def perform_task(self, request: str):
        for agent in self.agents:
            result = agent.perform_task(request)
            if result is not None:
                return result
        return "No agent could handle this request."
