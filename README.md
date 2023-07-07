# LOG-680 : Template for Oxygen-CS

![image](./doc/wheel.png)

This Python application continuously monitors a sensor hub and manages HVAC (Heating, Ventilation, and Air Conditioning) system actions based on received sensor data.
It leverages `signalrcore` to maintain a real-time connection to the sensor hub and utilizes `requests` to send GET requests to a remote HVAC control endpoint.
This application uses `pipenv`, a tool that aims to bring the best of all packaging worlds to the Python world.

## Requirements

- Python 3.8+
- pipenv
- Docker: Install Docker by following the instructions in the official Docker documentation.

## Getting Started

To run the project, follow these steps:

1. Create an .env file in the root directory of the project. **IMPORTANT: Add the .env file immediately to the .gitignore. This file will contain your secrets and must not be pushed in version control.**

````shell
HOST='http://0.0.0.0'
TOKEN='TokenDefaultValue'
TICKETS=5
T_MIN=50
T_MAX=100
DB_CONNECTION_STRING='DRIVER={ODBC Driver 18 for SQL Server};SERVER=ServerName;DATABASE=DBName;UID=Username;PWD=Password;TrustServerCertificate=yes;'
````
2. Set your .env file for docker-compose with the command:
````shell
$env:ENV_FILE = '.env'
````
You can verify that the value of ENV_FILE env variable is .env with:
````shell
echo $env:ENV_FILE
````

3. Running the Project with Docker Compose
   To run the project using Docker Compose, execute the following command in the terminal:

````shell
docker compose up --build

````

## Unit test
````shell
cd api/test
python -m unittest
````
### To run the test with coverage
1. Install coverage for local testing
````shell
pip install coverage
````
2. Run the tests
````shell
cd api/test
python -m coverage run -m unittest
````
3. For a report on the console, run this command
````shell
python -m coverage report  
````
4. For a report on a html page, run this command
````shell
python -m coverage html  
````

## License

MIT

## Contact

For more information, please feel free to contact the repository owner.
