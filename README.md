# Sortwise Fog Services

## Requirements

Python 3.11 and above. Exectute the following command to check the version of python installed on your system.

```
python --version
```

## Setup

1. Install Python Virtual Environment.

```
python -m venv env
```

2. Activate the virtual environment.

On Unix environments (Linux/macOS), run the following command:

```
source env/bin/activate
```

On Windows, run the following command:

```
source env/Scripts/activate
```

3. Install the required packages.

```
pip install -r requirements.txt
```

#### Notes

1. On Windows, `uvloop` cannot be installed. Comment out line 53 in `requirements.txt` before installing Python packages via pip.
2. If there are new packages installed, update the requirements.txt file by running the following command:

## Running the development server

1. Create a new `.env` file using the `.env.example` provided in the repository. Fill in the required environment variables.

```bash
# In the root directory of the repository
touch .env
```

2. Run the following command to start the development server. By default, the development process runs on port 8000.

```bash
# Add --host and --port to specify the host and port respectively
uvicorn src.main:app --reload
```

3. Open the browser and navigate to the following URL to access the API documentation

```bash
http://localhost:8000/docs
```
