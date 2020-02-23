# Programming vacancies compare

Compare average salary for different programming languages, using HeadHunter and SuperJob APIs.

## How to install

In order to get access to SuperJob api you need to get X-Api-App-Id token . To do so create an account at [api.superjob.ru](https://api.superjob.ru/) , then click [register an application](https://api.superjob.ru/info), type any urls in the fill-out form. Then create a .env file and put your token as TOKEN there.

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

	pip install -r requirements.txt

## Usage example
Create tables with data from HeadHunter and SuperJob vacancies:

    python main.py 

Output:

![](https://i.imgur.com/O7QNHVK.png)

## Project Goals
The code is written for educational purposes on online-course for web-developers dvmn.org
