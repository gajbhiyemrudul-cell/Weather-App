import requests
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

try:
    API_KEY = st.secrets["WEATHER_API_KEY"]
except Exception:
    API_KEY = os.getenv("WEATHER_API_KEY")

st.set_page_config(
    page_title = "Weather App",
    page_icon = "⛅",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>⛅ Weather App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter your city name and click the button to get the Weather</p>", unsafe_allow_html=True)


city = st.text_input("Enter the city Name")

API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"



if st.button("Fetch Weather Data"):
   if city.strip() == "":
      st.warning("Please enter a city name.")
      st.stop()
   response = requests.get(API_URL)

   if response.status_code == 200:
      data = response.json()

      icon = data["weather"][0]["icon"]
      icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

      country = data["sys"]["country"]

      st.subheader(f"📍 {city.title()}, {country}")
      st.image(icon_url, width=100)

      temperature = round(data["main"]["temp"], 1)
      humidity = data["main"]["humidity"]
      wind_speed = round(data["wind"]["speed"], 1)
      weather = data["weather"][0]["description"].title()
      feels_like = data["main"]["feels_like"]

      sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
      sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")

      col1, col2, col3, col4, col5 = st.columns(5)

      col1.metric("Temperature", f"🌡️ {temperature}°C")
      col2.metric("Humidity", f"💧{humidity}%")
      col3.metric("Wind Speed", f"🌬️{wind_speed} m/s")
      col4.metric("Condition", weather)
      col5.metric("Feels Like", f"🙂‍↔️{feels_like}°C")

      st.write(f"📅 {datetime.now().strftime('%A, %d %B %Y')}")
      st.write(f"🕒 Last Updated: {datetime.now().strftime('%I:%M:%S %p')}")

      st.write(f"🌅 Sunrise: {sunrise}")
      st.write(f"🌇 Sunset: {sunset}")

   else:
      st.error("❌ City not found. Please enter a valid city name.")



st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Made with ❤️ by Mrudul Gajbhiye")



