# COVID-19 Dashboard

This repository contains a dynamic COVID-19 dashboard built with Python and Dash. It showcases the latest trends and statistics about COVID-19, including daily cases, deaths, and recoveries, for each country. The data used in this project is fetched from John Hopkins University, and the project includes a Dockerfile for containerization.

## Project Overview

The COVID-19 dashboard is a full-stack project utilizing data science and data visualization libraries in Python. The dashboard updates automatically to always display the latest information. This project showcases data fetching, data cleaning, data visualization, and deployment skills.

## Technologies Used

* Python
* Dash
* Docker
* Pandas
* Plotly

## Installation

To install this project, follow these steps:

1. Clone this repository: 
   ```
   git clone https://github.com/CodingwithO/Covid-19_Oregon_Analysis.git
   ```
2. Change directory into the project: 
   ```
   cd Covid-19_Oregon_Analysis
   ```
3. Install the required Python dependencies: 
   ```
   pip install -r requirements.txt
   ```

## Docker Setup

To build a Docker image of this project and run it:

1. Build the Docker image: 
   ```
   docker build -t covid19dashboard .
   ```
2. Run the Docker container: 
   ```
   docker run -p 8050:8050 covid19dashboard
   ```
After running the container, the dashboard should be accessible at http://localhost:8050.

## File Structure

* `app.py`: This is the main Python script that runs the Dash application.
* `Dockerfile`: This file is used to create a Docker image of the project.
* `requirements.txt`: This file lists the Python dependencies.
* `data`: This directory contains the data used by the application.

## Usage

You can run the project by executing the `python app.py` command from the project's root directory. If you're using the Docker container, you can simply build and run the Docker image.

Please note that you should have Jupyter notebook installed to open and run the `.ipynb` files. You can install it using `pip install jupyter`.

Once you've installed Jupyter, you can launch it by navigating to the project's directory in your Anaconda Prompt and typing `jupyter notebook`. This will start the Jupyter server and open a tab in your default web browser where you can select and run the notebook file(s) in your project.

## Contact

For any additional questions or comments, please contact Jason Ogbomoh via [ogbomohjason@gmail.com](mailto:ogbomohjason@gmail.com).