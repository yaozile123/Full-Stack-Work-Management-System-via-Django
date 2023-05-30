# Work Management System
## Overview

The Work Management System is a responsive web application developed using Django, Bootstrap, and JavaScript. 
It is designed to streamline task tracking and management, featuring user authentication and CRUD (Create, Read, Update, Delete) functionality.

## Features

- User authentication with secure login
- Intuitive and engaging front-end interface using Bootstrap and JavaScript
- Task management with CRUD operations
- Robust data storage using MySQL
- Deployment on Amazon Elastic Beanstalk[(Link)](http://djangoenv.eba-43ymgqia.us-west-2.elasticbeanstalk.com/) for seamless scaling, monitoring, and maintenance

## Quick Demo
[![Alt text](https://img.youtube.com/vi/Z3WxXH5lDoA/0.jpg)](https://www.youtube.com/watch?v=Z3WxXH5lDoA)

## Getting Started

1. Clone the repository and cd into the project
```shell
git clone https://github.com/yaozile123/Full-Stack-Work-Management-System-via-Django.git
cd Full-Stack-Work-Management-System-via-Django
```
2. Create a Python virtual environment if you don't have one
```shell
python -m venv venv
```
3. Activate the virtual environment
- On Windows
```shell
venv\Scripts\activate
```
- On macOS and Linux
```shell
source venv/bin/activate
```
4. Install the required packages
```shell
pip install -r requirements.txt
```
5. Set up the MySQL database and update the DATABASES setting in settings.py accordingly.
6. Run the migrations
```shell
python manage.py migrate
```
7. You are all set! Try run the development server
```shell
python manage.py runserver
```
