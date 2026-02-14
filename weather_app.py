import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "1ba27573c645483fb65e97e1531f74bd"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather():
    city = city_input.get().strip()
    unit = unit_choice.get()

    if city == "" or city == "Enter city":
        messagebox.showwarning("Input Error", "Please type a city name.")
        return

    parameters = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    try:
        response = requests.get(WEATHER_URL, params=parameters, timeout=10)
        weather_data = response.json()

        if str(weather_data.get("cod")) != "200":
            messagebox.showerror("Error", "City not found.")
            return

        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"].title()
        wind_speed = weather_data["wind"]["speed"]
        humidity = weather_data["main"]["humidity"]

        symbol = "°C" if unit == "metric" else "°F"

        output = (
            f"City: {city.title()}\n"
            f"Temperature: {temperature}{symbol}\n"
            f"Condition: {description}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        weather_result.config(text=output)

    except requests.exceptions.RequestException:
        messagebox.showerror("Connection Error", "Unable to connect to the weather service.")


app = tk.Tk()
app.title("My Weather Checker")
app.geometry("380x420")
app.resizable(False, False)
app.configure(bg="purple")

title_label = tk.Label(
    app,
    text="My Weather Checker",
    font=("Segoe UI", 18, "bold"),
    bg="purple",
    fg="white"
)
title_label.pack(pady=15)

input_frame = tk.Frame(app, bg="purple")
input_frame.pack(pady=10)

city_input = tk.Entry(
    input_frame,
    width=25,
    font=("Segoe UI", 12),
    justify="center",
    bd=0
)
city_input.pack(ipady=6)
city_input.insert(0, "Enter city")

unit_choice = tk.StringVar(value="metric")

unit_frame = tk.Frame(app, bg="purple")
unit_frame.pack(pady=10)

tk.Radiobutton(
    unit_frame,
    text="Celsius",
    variable=unit_choice,
    value="metric",
    bg="purple",
    fg="white",
    selectcolor="purple"
).pack(side="left", padx=10)

tk.Radiobutton(
    unit_frame,
    text="Fahrenheit",
    variable=unit_choice,
    value="imperial",
    bg="purple",
    fg="white",
    selectcolor="purple"
).pack(side="left", padx=10)


search_button = tk.Button(
    app,
    text="Check Weather",
    command=fetch_weather,
    font=("Segoe UI", 12, "bold"),
    bg="lightgreen",
    fg="white",
    bd=0,
    padx=20,
    pady=8,
    activebackground="green"
)
search_button.pack(pady=15)

result_card = tk.Frame(
    app,
    bg="white",
    bd=2,
    relief="ridge"
)
result_card.pack(padx=20, pady=10, fill="both", expand=True)

weather_result = tk.Label(
    result_card,
    text="Weather details will appear here",
    font=("Segoe UI", 12),
    bg="white",
    fg="purple",
    justify="center"
)
weather_result.pack(pady=20)

app.mainloop()
