# Flask Project

A simple Flask application to demonstrate the setup and usage of Flask for web development.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Running the Application](#debugging)
4. [Project Structure](#project-structure)
5. [License](#license)

---

## Getting Started

Create environmental variables:

```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

```

Setup/Configure the MySQL database

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/) installed
- [pip](https://pip.pypa.io/en/stable/installation/) for package management
- A virtual environment (recommended)

### Installation

1. Clone the repository:

```bash
 git clone https://github.com/delly876/876promotions.git
 cd your-flask-project
```

2. Create a virtual environment - [how to setup virtual environment](https://dev.to/mursalfk/setup-flask-on-windows-system-using-vs-code-4p9j)
3. Install Requirements:

```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
pip install setuptools --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

```

### Running the Application

1. Activate the virtual environment
2. Run the application using python app.py
3. The application will be available at http://localhost:5000
4. run: flask run

### Notes

1. To generate the models from the database:

```bash
sqlacodegen_v2 "mysql+mysqldb://promo:TestPassword1!@127.0.0.1/promoti5_promotions" --outfile app/database/models/models.py
```
