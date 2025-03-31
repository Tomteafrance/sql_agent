import json
import yaml
import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from database.sqldatabase import SQLDBConnector
from sql_agent.agent import SQLAgent
from loader.dataloader import DataLoader
from utils import Utils

def reset_conversation():
  st.session_state.conversation = None
  st.session_state.messages = []

st.set_page_config(
    page_title = "SQLDatabase",
    page_icon = "✨",
    initial_sidebar_state = "expanded",
    layout = "wide"
)

st.title('🦜 Chat with the SQL Assistant! 💬')
with st.expander("🤖 SQL Assistant Features"):
    st.caption("Leverage the power of generative AI to easily execute SQL Query on your data")
    st.caption(''' If you want to connect to your SQL Database, follow the instructions :

    ### Json File to upload to connect to your SQL Database : 
        {
        "config": {
            "username": "username",
            "password": "password",
            "host": "host",
            "port": "port",
            "database_name": "database_name",
            "table_list": ["table_1", "table_2", "table_3"] or []
            }
        }

    Precise the tables if you want to filter on some tables, if you want to get all tables just put "table_list" : []

    **You could ask the following**:           
    
    - Give a query in natural language to get the translation in SQL: What are the least sold wine in France ? 
                   
    **Please note:**
    - Your data should be in a single table format, either as a "dataset" with features as columns, and observations as rows.
    - We assume that your data is accurate and correclty formatted.''')

st.sidebar.header("✨ Upload Config")
uploaded_file = st.sidebar.file_uploader("Upload json files", type=['json'])
             
st.sidebar.header("Parameters :")
model = st.sidebar.selectbox('model', tuple(Utils.get_model_list()), index=0, help='💡LLM models available, each model has its advantages and drawbacks: \n\n Mistral-7B-Instruct & Mixtral-8x7b-Instruct will be more verbose but with a moderate risk of hallucinations.\n\n Meta-llama-3-8b-instruct will be the most creative model, but with higher risk of hallucinations.')
sampling = st.sidebar.selectbox('sampling',("true", "false"), index=1, help='💡Needs to be true if you intend to leverage temperature..')
temperature = st.sidebar.slider('temperature', min_value=0.0, max_value=1.0, step=0.1, value=0.0, help='A higher temperature will result in more creative and imaginative text. Must be used in conjunction with Sampling = True')
max_new_tokens = st.sidebar.selectbox('max new tokens',(64, 128, 256, 512, 768, 1024, 2048, 4096, 8192), index=5, help ='💡Number of tokens that can be generated in output. In english 1,000 tokens is about 750 words')

with open('../config_template.yaml', 'r') as file:
    config = yaml.safe_load(file)

application_name = config['sogenai_api_credentials']['app_name']
key_name = config['sogenai_api_credentials']['key_name']
client_id = config['sogenai_api_credentials']['client_id']
client_secret = config['sogenai_api_credentials']['client_secret']
sg_connect_access_token = None
database = None

if uploaded_file is not None:
    config_db: dict = DataLoader.load_config(uploaded_file)
    username = config_db['config']['username']
    password = config_db['config']['password']
    database_name = config_db['config']['database_name']
    host = config_db['config']['host']
    port = config_db['config']['port']
    table_list = config_db['config']['table_list']
    sql_connector = SQLDBConnector(username=username, password=password, database_name=database_name, host=host, port=port, table_list=table_list)
    engine = sql_connector.connect()

    with st.expander("### Afficher les tables disponibles"):
        for table in table_list:
            st.write(f"- {table}")

    database = sql_connector.get_database()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history", input_key="input", return_messages=True)

conversational_memory = st.session_state.memory

if database is not None:
    agent_init = SQLAgent(  
        database=database, 
        model_name=model, 
        sampling=sampling, 
        temperature=temperature, 
        max_new_tokens=max_new_tokens, 
        application_name=application_name,
        key_name=key_name,
        client_id=client_id,
        client_secret=client_secret,
    )

    sql_agent = agent_init.create_agent(conversational_memory)

if ('messages' not in st.session_state):
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
prompt = st.chat_input("Please enter your query")
if prompt:    
    st.session_state.messages.append({'role':'user', 'content': prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.spinner("Processing"):
        with st.chat_message('assistant', avatar="🦜"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = sql_agent.run(prompt, callbacks = [st_callback])  
    
    st.session_state.messages.append({'role':'assistant', 'content': response})

st.button('Reset Chat', on_click=reset_conversation)