Instructions:
- Prerequisites:
	- Install python 3 in the machine running the application
	- Install mysql connector using the pip install mysql-connector-python command from terminal
	- Install Stripe third party checkout module using the pip install stripe command from terminal

1. Set up the DATABASE
	- Reference the readme file in the Database Scripts Folder.
2. Configure Flask:
	- Open the flaskr folder
	- Find the Flask.py file and open it.
	2.1 Configure Database Connection:
		- Find the "Connect to MySQL Database" section
		- Replace the values of the MySQL Database fields to connect to the local Database Instance
			db = mysql.connector.connect(
			host="localhost",
			user="root",
			password="YourPassword",
			database="pathfinders"
			)
	2.2 Configure Stripe Checkout Keys
		- Find the "Stripes Checkout API and Private Keys" section
		- Update the Private and API Keys for creating Checkout Sessions from Stripes module
3. Run Flasky.py 

