from pydantic import BaseModel, Field

class WeatherDescription(BaseModel):
    description: str

class MainWeather(BaseModel):
    temp: float = Field(..., description="Current temperature in Celsius")
    feels_like: float = Field(..., description="Feels like temperature in Celsius")
    humidity: int = Field(..., description="Humidity percentage")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")

class WindWeather(BaseModel):
    speed: float = Field(..., description="Wind speed in m/s")
    deg: int = Field(..., description="Wind direction in degrees")

class WeatherResponse(BaseModel):
    name: str = Field(..., description="City name")
    weather: list[WeatherDescription] = Field(..., description="Weather conditions")
    main: MainWeather = Field(..., description="Main weather data")
    wind: WindWeather = Field(..., description="Wind data")
