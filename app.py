import streamlit as st
from dotenv import load_dotenv
import requests, os
from langchain_google_genai import ChatGoogleGenerativeAI
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['key'] = os.getenv("WEATHER_API")

try:
    api_instance = swagger_client.APIsApi(swagger_client.ApiClient(configuration))
except ApiException as e:
    raise e

load_dotenv()

def get_weather_data(city,days):
    api_response = api_instance.forecast_weather(q=city, days=days, aqi="yes")
    current_weather_data = {
        "temperature": api_response['current']['temp_c'],
        "windspeed": api_response['current']['wind_kph'],
        "humidity": api_response['current']['humidity'],
        "air_qual_pm": api_response['current']['air_quality']['pm2_5'],
        "air_qual_co2": api_response['current']['air_quality']['co'],
        "country": api_response['location']['country'],
        "region": api_response['location']['region'],
        "latitude": api_response['location']['lat'],
        "longitude": api_response['location']['lon'],
        "localtime": api_response['location']['localtime']
    }
    forecast_data={
        "timings": api_response['forecast']['forecastday'][0]['hour'][-1]['time'],
        "temperature": api_response['forecast']['forecastday'][0]['hour'][-1]['temp_c'],
        "windspeed": api_response['forecast']['forecastday'][0]['hour'][-1]['wind_kph'],
        "chance_rain": api_response['forecast']['forecastday'][0]['hour'][-1]['chance_of_rain']
    }
    
    return current_weather_data, forecast_data

def generate_weather_desc(current_weather_data,api_key):
    
    try:
        
        prompt= f"""
        
                    You are a weather assistant providing detailed weather information along with necessary precautions and actionable steps for the day. 
                    Based on the following attributes: temperature, windspeed, humidity, air_qual_pm, and air_qual_co2, generate a comprehensive weather report and advice for the user.

            Attributes:
            - Temperature: {current_weather_data['temperature']}°C
            - Windspeed: {current_weather_data['windspeed']} km/h
            - Humidity: {current_weather_data['humidity']}%
            - Air Quality (PM): {current_weather_data['air_qual_pm']} μg/m³
            - Air Quality (CO2): {current_weather_data['air_qual_co2']} ppm

            Generate the weather report as follows:

            ---

            **Weather Report for Today:**

            - **Temperature:** {current_weather_data['temperature']}°C
                - [Precaution/Actionable Step: Generate a nuanced and dynamic actionable steps based on the temperature.]

            - **Windspeed:** {current_weather_data['windspeed']} km/h
                - [Precaution/Actionable Step: Generate a nuanced and dynamic actionable steps based on the windspeed .]

            - **Humidity:** {current_weather_data['humidity']}%
                - [Precaution/Actionable Step: Generate a nuanced and dynamic actionable steps based on the humidity.]

            - **Air Quality (PM):** {current_weather_data['air_qual_pm']} μg/m³
                - [Precaution/Actionable Step: Generate a nuanced and dynamic actionable steps based on air quality.]

            - **Air Quality (CO2):** {current_weather_data['air_qual_co2']} ppm
                - [Precaution/Actionable Step: Generate a nuanced and dynamic actionable steps based on CO2 levels.]

        """

        llm= ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
        result=llm.invoke(prompt)
        return result.content
    except Exception as e:
        return str(e)


def main():


    st.sidebar.title("Weather app")
    city=st.sidebar.text_input("Enter text input","london")
    submit= st.sidebar.button("Get weather")

   

    if submit:
        with st.spinner("fetching weather data.."):
            current_weather_data,forecast_weather_data= get_weather_data(city, days=2)
            st.title("Weather updates for "+ city)
            tab1, tab2 = st.tabs(["Current weather", "Forecast weather"])
            
            with tab1:
                with st.expander("See location details"):
                    container = st.container(border=True)
                    container.write(f"Country: {current_weather_data['country']}")
                    container.write(f"Region: {current_weather_data['region']}")
                    container.write("Latitude: "+str(current_weather_data['latitude'])+" and  Longitude:" + str(current_weather_data['longitude']))
                    container.write(str(f"Local time: {current_weather_data['localtime']}"))

                col1,col2= st.columns(2)
                with col1:
                    st.metric("Temperature", f"{current_weather_data['temperature']} C")
                    st.metric("Humidity", f"{current_weather_data['humidity']} %")

                with col2:
                    st.metric("Air quality(PM)",f"{current_weather_data['air_qual_pm']} μg/m³")
                    st.metric("Wind Speed",f"{current_weather_data['windspeed']} kph")

                generated_weather_report= generate_weather_desc(current_weather_data,api_key=os.getenv("GOOGLE_GEMINI_API"))
                st.write(generated_weather_report)
            
            with tab2:
                st.metric("Timing", f"{forecast_weather_data['timings']}")
                st.metric("Temperature", f"{forecast_weather_data['temperature']} C")
                st.metric("Wind Speed", f"{forecast_weather_data['windspeed']} kph")
                st.metric("Chance of Rain", f"{forecast_weather_data['chance_rain']} %")
                        


if __name__=="__main__":
    main()