## Tech Stack

 1. Python 3.11
	 - Flask
	-  Flask-RestX
	-  Flask-SQLAlchemy
	-  Pandas
	- PyTest
2. Docker

## Setup Locally
1. Install Python 3.11
2. Create virtuanlenv via `python -m venv venv`
3. Activate environment:
	- Windows :  `venv\Scripts\activate`
	- Linux:  `source venv/bin/activate`
4. Install requirements via `pip install -r requirements.txt`
5. To run:
	-	test : `pytest`
	-	app : `python app.py`

## GCP Secret Manager
1. Store sensitive data to secret manager.
2. Grant access to a service account.
3. Access the variables via API or via configuration in cloud.
