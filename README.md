# Grant Compass

# To run locally:
- Run: `uvicorn api:app --reload`
- Navigate to the frontend folder `cd frontend`
- Run: `npm start` (see the frontend Readme for more details)

# Getting the data
- Download the GrantsDBExtract20230926v2.zip XML extract: https://www.grants.gov/xml-extract.html
- Create a folder called `data` at root and put the xml file in the folder created in the previous step
- Run `cp .env.tpl .env`
- Fill in your OpenAI API key into the newly created .env file

# Creating a virtual environment
- python -m venv .venv
- Activate your virtual environment https://docs.python.org/3/library/venv.html
- `pip install -r requirements.txt`
