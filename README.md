# Installation
After cloning you will have to install the dependencies. 
This project is provided as an installable Python module.
This means that you can simply go to the root of the project and run
```shell
pip install -e .
# -e installs the project as editable, which means that you can make changes to the source code without reinstalling
```
Alternatively you can simply use PyCharm to install dependencies from the `requirements.txt` file.

# Plotly documentation
Plotly documentation
- [https://plotly.com/python/](https://plotly.com/python/)

Dash documentation
- https://dash.plotly.com/sharing-data-between-callbacks

Pandas documentation
- https://www.w3schools.com/python/pandas/default.asp
- https://pandas.pydata.org/docs/user_guide/index.html


# Running the app on prod
Currently it is not entirely production complete since it does not run using a real production wsgi server.
I dont care.

Run the bastard using:
```shell
docker compose up
```
Boom badabing you got it running using port 8080. 
If you want port 80 on the server uncomment it in the docker compose file.
