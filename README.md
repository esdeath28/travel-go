<h1>Travel Go Setup Readme</h1>

This README file provides instructions on setting up a Django project 'Travel Go'. The APIs are designed to help users discover the coolest districts based on the average temperature at 2 pm for the next 7 days as well as assisting users in making informed decisions about travel plans by comparing the temperatures of two locations on a specific date and advising whether it's a suitable day for travel.

### Features
### Coolest Districts API:
<p>Description: Fetches the list of the coolest 10 districts based on the average temperature at 2 pm for the next 7 days.</p>
<p>Endpoint: /getCoolestDistricts/</p>
<p>Method: GET</p>

### Travel Decision API:
<p>Description: Compares the temperature at 2 pm for the given origin and destination on the specified date. Returns a response advising whether it's suitable to travel.</p>
<p>Endpoint: /travelRecommendation/</p>
<p>Method: POST</p>
<p>Parameters</p>
- `departure_latitude` (float): The latitude of the user's current location.
- `departure_longitude` (float): The longitude of the user's current location.
- `destination_latitude` (float): The latitude of the desired travel destination.
- `destination_longitude` (float): The longitude of the desired travel destination.
- `travelling_date` (string): The date of travel (format: YYYY-MM-DD).
<p>Request Example</p>
{
  "departure_latitude": 23.7104,
  "departure_longitude": 90.4074,
  "destination_latitude": 24.3745,
  "destination_longitude": 88.6042,
  "travelling_date": "2024-01-10"
}

### Extra Features
Endpoint: /home/ takes you to an interactive ui where you can get an enhanced experience. This template is for testing purposes and provides a user-friendly interface to interact with the APIs.
-- Beware as you hit home page it immedietly send request to the Coolest Districts API making several calls and as your daily requests limits are suggested to remain below 10,000 calls you might not want to refresh the page too often.
Usage:
1. Fill in the Form:
   - Input your departure and destination coordinates along with the travel date.
3. Submit the Form:
   - Click the submit button to send a request to the Travel Decision API.
4. View Results:
   - The website will display the API's response, including an advisory message about the travel suitability.


