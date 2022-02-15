Python library called Streamlit will allow us to develop a simple data-driven application for this project

Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.

### Create conda environment
Firstly, we will create a conda environment called *big_data*
```
conda create -n big_data 
```
Secondly, we will login to the *big_data* environement
```
conda activate big_data
```
### Install prerequisite libraries

For this project we will need to install the following  libraries

Pip install
```
streamlit
pandas
base64
subprocess
os
pickle

```
### Explaning the use of these libraries
```
streamlit - we are making use of streamlit as the web framework
pandas - we are using pandas in order to display the data frame
base64 - will be used for encoding, decoding the file, when we will make the file available for downloading the prediction results
subprocess - the descriptor calculation will be made possibile using the subprocess library
os - we are using the 'os' library in order to perform file handeling
pickle - will be used for loading up the picked file of the model
```

###  Launch the app
First we have to navigate to the folder were the app.py is
Second to launch the app we have to type the following  commands in conda environement.

```
streamlit run app.py
```
