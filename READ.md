Hospital Management REST API
📌 Project Overview

This project is a CRUD REST API developed using Flask and MySQL for managing hospital-related data. It allows clients to perform Create, Read, Update, and Delete (CRUD) operations on patients, view related doctors and diagnoses, search patient records, and securely modify data using JWT authentication.

The API supports JSON and XML response formats and was fully tested using Postman.
This project was created as the Final Project for CSE1.

## 🛠️ Technologies Used

Python 3
Flask
Flask-MySQLdb
Flask-JWT-Extended
MySQL
Postman (API testing)
dicttoxml (XML formatting)

## Installation & Setup
1️⃣ Clone the Repository git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

## Create & Activate Virtual Environment
source venv/Scripts/activate

## Install Dependencies
pip install -r requirements.txt

## Setup MySQL Database
hospital.sql

## Update Database Credentials
Edit app.py if needed:
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "your_password"
app.config["MYSQL_DB"] = "hospital"

## Run the Application
python app.py
http://127.0.0.1:5000
