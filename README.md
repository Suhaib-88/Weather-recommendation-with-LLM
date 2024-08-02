# Weather AI
Welcome to the Weather AI project! This repository contains the code and resources for developing an AI-powered WhatsApp Business chatbot that provides interactive and efficient customer support by leveraging advanced natural language processing techniques.

## Features
Enhanced Customer Interaction: Understands and responds to customer inquiries in natural language.
Personalized Support: Provides tailored responses and suggestions based on customer data.
User-Friendly Interface: Offers an intuitive and easy-to-use interface for interacting with the bot.
Scalability: Handles multiple customer inquiries simultaneously with quick and accurate responses.
Cost Efficiency: Reduces the need for a large human support team.
Technologies Used
Large Language Model (LLM): Groq LLM, llama3-8b-8192
Twilio API: For sending and receiving WhatsApp messages
FastAPI: For backend services
Ngrok: For local development and testing

## Prerequisites
- Google gemini api key [](https://makersuite.google.com/)
- WEATHER API [](https://www.weatherapi.com/)

## Getting Started

### Clone the Repository:

```git clone https://github.com/Suhaib-88/Weather-AI.git```

```cd Weather-AI```

### Install Dependencies:

```python setup.py install --user ```

### Set Up Environment Variables:
- Create a .env file in the root directory and add the following variables:
  - LANGUAGE_MODEL_API_KEY=your_language_model_api_key
  - WEATHER_API=  your_weather_api
    
### Running the Application

```streamlit run app.py```
