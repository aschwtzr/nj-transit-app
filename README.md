## NJ Transit App
Find trains headed to your destination. 

### To run: 
1. clone the repo with `git@github.com:aschwtzr/nj-transit-app.git`.
2. set up the environment by running `pipenv install` (if you don't have pipenv installed [see here](https://pypi.org/project/pipenv/).).
3. run the script with `sh run_api.sh`.

### Usage
 - the API will be running at `localhost:5000`.
 - `/stations` returns a list of stations and information about them, including the `stop_id`.
 - `/routes` takes two parameters: origing and destination. Enter your desired `stop_id`s to see the potential trains and times.
 - To update the transit data, head to the [NJ Transit developer portal](https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevLoginSubmitTo), download rail data and replace the contents of the directory `./rail_data`.
