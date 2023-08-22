import pandas as pd 
import streamlit as st 
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from my_functions import load_csv, generate_response, other_inputs
import my_functions as mf 
from tempfile import NamedTemporaryFile
import statistics
import plotly 
import matplotlib
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
import bokeh
import altair

# Documentation  https://platform.openai.com/docs/api-reference/fine-tunes/create?lang=python

# Todo list
# See how he gets more outputs for llms
# Create a plotting page for charts 
# Create a mapping page 
# Create an illustration page



# We will use this to satiate the other inputs function.
question_list = [
    "How many rows are in this dataset?",
    "How many columns are in this dataset?",
    "Other"
]



st.title("Robo-Analytical Assistant 🤖📈")
st.write("""This project will show the power of utilizing Language Learning Models (LLMs) in jumpstarting data analytics.
         We will be using OpenAI to enable the LLM's capability. In order for this project to work you will need an OpenAI key.
         This key can be generated by visiting OpenAI's platform at this [link](https://platform.openai.com/account/api-keys). 
         """)

with st.expander("Pros and Cons of Using LLM for Analytics❕❗"):
    st.write("There are pro and cons for using Generated Pretained Transformers (GPT) for helps in data analytics. (GPT is a specific type of LLM that was created by OpenAI). A pro would be that certain questions can easily be answered without having to write a single line of code. Another benefit about GPT is that stakeholders can derive additional insight from datasets even if they do not have advanced technology skills nor deep analytical acumen when it comes to data.")
    st.write("There are some downsides when it comes to using LLMs for data analytics. A con is that there are some rudimentary questions that the LLMs are not able to answer. Also it is possible for the llms to give erroneous answers occassionally. Despite the aforementioned and other drawbacks utlizing LLM and other forms of artificial intelligence (AI) can improve the lives of analysts and stakeholders alike.")

# Collect CSV From User Here
input_file = st.file_uploader("Browse for a CSV file:", type = ["csv"])



# This Boolean stops the generate_response line from breaking.
# We will see that the llm generator will only become ready when the df is both loaded and configured.
generator_ready = False


# Loading the file for analytics 
# Note streamlit allows users to upload files however once they are utilized once the dataframe is deleted 
# This is why it is best to make a copy of the dataframe and to utilize the copy instead to prevent errors in this case it is df2.

if input_file is not None:
    dataframe = load_csv(input_file)
    
 
    # NOTE testing to see if we can get rid of these two lines of code
    input_file.seek(0)
    df = pd.read_csv(input_file, low_memory= False)
    df2 = df

    generator_ready = True
elif input_file is None: 
    st.info("Please upload a file on the above line to get started.")
    

# NOTE the necessary function is embedded in the previous if statement and is triggered once the file is uploaded.
# The uploading the file modifies the boolean and renders it true, allowing the next code to proceed without throwing an error.

if generator_ready is True:
    other_inputs(question_list, df2)
#other_inputs(question_list, f.name)





   
   

