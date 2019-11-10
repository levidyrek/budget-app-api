# Budget App REST API

Django REST API for creating/maintaining a personal budget.

See [https://github.com/levidyrek/budget-app](https://github.com/levidyrek/budget-app) for the React web app.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [Install Docker](https://docs.docker.com/install/)
* [Install Docker Compose](https://docs.docker.com/compose/install/)

### Development Setup

Clone this repository.

```
git clone git@github.com:levidyrek/budget-app-api.git
```

Copy the sample config file for development to a `dev.env` file.

```
cp dev.sample.env dev.env
```

Start the development server with Docker Compose.

```
docker-compose up
```

Access the browsable API in your browser at [http://localhost:8000](http://localhost:8000).


## Deployment

Clone this repository.

```
git clone git@github.com:levidyrek/budget-app-api.git
```

Copy the sample config file for production to a `production.env` file.

```
cp prod.sample.env production.env
```

Update `production.env` settings, including `SECRET_KEY`, database credentials, known host settings, and CORS settings, according to your environment. See sample `.env` files for examples.

Start the development server with Docker Compose.

```
docker-compose -f docker-compose.yml -f production.yml up
```

## Usage

Most endpoints require authentication. To create a user via the browsable API, use the `/users/register/` endpoint. You can log in with the credentials you create there. If log in via the browsable API, you will need to clear your browser's cookies before you will be able to log in via the React app.

## Built With

* [Python](https://www.python.org/) - The language used
* [Django](https://www.djangoproject.com/) - The web framework and ORM
* [Django REST](https://www.django-rest-framework.org/) - REST API framework for Django
* [PostgreSQL](https://www.postgresql.org/) - The database
* [Docker](https://www.docker.com/) - Containerization engine
* [Docker Compose](https://docs.docker.com/compose/) - Deployment tool

## Acknowledgments

* Website design inspired by [YNAB](https://www.youneedabudget.com/).
