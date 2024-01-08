# Travel Go

My task involved developing two distinct APIs to enhance user experiences with weather-related insights. The first API aims to assist users in uncovering the coolest 10 districts, providing average temperature forecasts at 2 pm for the upcoming 7 days. The second API is designed to assist users in making well-informed travel decisions by comparing temperatures between two locations on a specified date and offering advice on the suitability of each destination for travel.
## Description
### Coolest Districts API:
To discover the coolest districts, make a `GET` request to the `/getCoolestDistricts` endpoint. The API will respond with a list of 10 coolest districts considering average temperature data for the next 7 days at 2 pm.<br><br>
**Endpoint** &nbsp;&nbsp;&nbsp;&nbsp;: &nbsp;&nbsp;http://127.0.0.1:8000/getCoolestDistricts/<br>
**Method** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: &nbsp;&nbsp;GET

### Travel Decision API:
To decide weather the destined place is suitable to cool you down or not make a `POST` request to `/travelRecommendation` endpoint. The API will compare the temperature at 2 pm for the given location and destination on the provided date and return a boolean response advising whether it's suitable to travel.<br><br>
**Endpoint** &nbsp;&nbsp;&nbsp;&nbsp;: &nbsp;&nbsp;http://127.0.0.1:8000/travelRecommendation/<br>
**Method** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: &nbsp;&nbsp;POST<br>
### Parameters
- `departure_latitude` (float): The latitude of the user's current location.
- `departure_longitude` (float): The longitude of the user's current location.
- `destination_latitude` (float): The latitude of the desired travel destination.
- `destination_longitude` (float): The longitude of the desired travel destination.
- `travelling_date` (string): The date of travel (format: YYYY-MM-DD).

### Example

```json
{
  "departure_latitude": 23.7104,
  "departure_longitude": 90.4074,
  "destination_latitude": 24.3745,
  "destination_longitude": 88.6042,
  "travelling_date": "2024-01-10"
}
```

## Setup Guide
You can follow these instructions to set up the project in your local machine:

1. #### Clone the Repository or down Zip file.
    ```
    git clone https://github.com/esdeath28/travel-go.git
    ```
2. #### Install pipenv environment
    You need to set up a virtual environment for the project. It'll automatically manages project packages through the Pipfile file as you install or uninstall packages.<br>

    ```
    pip install pipenv
    ```
2. #### Navigate to Project Directory
    ```
    cd travel-go
    ```
3. #### Install dependencies in virtual environment 
    ```
    pipenv install --python 3.11
    ```
    ```
    pipenv install requests
    ```
5. #### Activate Virtual Environment
    ```
    pipenv shell
    ```
6. #### Start the Development Server
    ```
    python manage.py runserver
    ```
**Remarks**: You can take a look into my dependency tree for more clarifications in case of dependencies installation error.

```
cattrs==23.2.3
└── attrs [required: >=23.1.0, installed: 23.2.0]
djangorestframework==3.14.0
├── django [required: >=3.0, installed: 5.0.1]
│   ├── asgiref [required: >=3.7.0,<4, installed: 3.7.2]
│   ├── sqlparse [required: >=0.3.1, installed: 0.4.4]
│   └── tzdata [required: Any, installed: 2023.4]
└── pytz [required: Any, installed: 2023.3.post1]
flatbuffers==23.5.26
platformdirs==4.1.0
python-dateutil==2.8.2
└── six [required: >=1.5, installed: 1.16.0]
requests==2.31.0
├── certifi [required: >=2017.4.17, installed: 2023.11.17]
├── charset-normalizer [required: >=2,<4, installed: 3.3.2]
├── idna [required: >=2.5,<4, installed: 3.6]
└── urllib3 [required: >=1.21.1,<3, installed: 2.1.0]
url-normalize==1.4.3
└── six [required: Any, installed: 1.16.0]
```

## API Response Time

### Successful Response Time
For the **Coolest Districts API** the best response time I got is `530ms`. And for the **Travel Decision API** the best response time I got is `486ms`.
![alt text.](/postman/api_01_530.png "image1.")
![alt text.](/postman/api_02_486.png "image3.")

**N.B.** The response time varies over time. This variability can be influenced by factors such as server load, network conditions, and other external dependencies.  Observations indicate that the least response times are typically captured after midnight.<br>
To reduce Resource Overhead, Scalability, Speed and Efficiency I tried to use less dependencies.

### Postman Collections and Environment
I have provided Postman collections and environment for easy API testing. Use the following files to import them into your Postman workspace:
* Postman Collections
* Postman Environment

### Extra Features
Thought it'd look cooler if there was some kind of interface to interact with the API. There's always a smol happiness in seeing your work in a live environment. Anyway, the endpoint takes you can see the list of 10 coolest districts as only the Coolest Districts API is integrated. Hope I'll do the same for the Travel Decision API too. :D <br>
**Endpoint** &nbsp;&nbsp;&nbsp;&nbsp;: &nbsp;&nbsp;http://127.0.0.1:8000/home/ <br><br>
![alt text.](/postman/live.png "image1.")

**Note**: Beware as you hit home page it immedietly send request to the Coolest Districts API making several calls and as your daily requests limit are suggested to remain below 10,000 calls you might not want to refresh the page too often.
