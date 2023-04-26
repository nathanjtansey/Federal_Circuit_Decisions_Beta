# Federal_Circuit_Decisions_Beta

This repository is used for hosting the Beta version of the Federal Circuit Decision Database website.

## Data
* This folder contains the tab delimited data files downloaded from the Harvard dataverse. Any updates of this data will require pushing new files to this folder.

## Home.py
* This is the main page of the website. It is also the reference point for Streamlit when the app was deployed. It must stay on the main page of the repository in order for Streamlit to function properly.

## Pages
* This folder contains all of the pages (besides the home page) that users can navigate to in the website. Each page is simply its own Python script. The names of each page as they appear on the website are the names of each respective Python file with "_" replaced with spaces.

## config.py
* This file contains all of the constants (links, data types, etc.) that need to be imported to multiple pages. It also contains functions that are used across multiple pages. The goal is that any future updates will require only changes to this file. 

## requirements.txt
* This text file contains the packages and their versions that Streamlit will need to run in order to display the website. If any packages are updated or added to the Python files, the requirements file will need to be updated as well to reflect that change.
