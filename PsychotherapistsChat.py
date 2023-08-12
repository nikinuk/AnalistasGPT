import streamlit as st
from PIL import Image
import openai
import json
ASSISTENT_MEMORY = 10 #defines how many chat iterations is kept in the "assistent" role for context

def update_assistant(old, new):
    # Adds new "assistent" entries in the chat context, limited by choosen ASSISTENT_MEMORY
    if len(old) <= ASSISTENT_MEMORY:
        old = old + [ { "role": "assistant", "content": new } ]
    else:
        old = old.pop(0) + [ { "role": "assistant", "content": new } ] 
    return old

autentication_type = st.sidebar.radio(
    "Please choose autentication type:",
    ("password", "my own OPENAI_API_KEY")
    )
if "autentication_type" not in st.session_state:
    st.session_state.autentication_type = autentication_type
pwd = st.sidebar.text_input("type your password or APY key", type="password")
if st.session_state.autentication_type == "password":
    if pwd == st.secrets["PASSWORD"]:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    OPENAI_API_KEY = pwd
    
#LOAD persona list
if "personas" not in st.session_state:
    # Opening JSON file
    with open('personas.json', 'r') as openfile:
        # Reading from json file
        p = json.load(openfile)
    #Create radio buttons
    butt_name = []
    for i in range(len(p)):
        butt_name.append(p[str(i)]["name"])
    st.session_state.personas = p
    st.session_state.names = tuple(butt_name)
p = st.session_state.personas
# CHOOSE ROLES - on side bar, radio buttond
psycho = st.sidebar.radio(
    "Please choose you therapist for the day:",
    st.session_state.names
    )
psycho = str(st.session_state.names.index(psycho))
if "persona" not in st.session_state: # initialize state
        st.session_state.persona = "0"

if st.session_state.persona != psycho:  # when the persona changes, reset messages 
        # RESET MESSAGES 
        del st.session_state.messages
        st.session_state.persona = psycho
        
# SETUP MODEL FOR PERSONA
#model, system_content, avatar, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, openning_statement, picture, intro, promptstamp = role_setup(st.session_state.persona)

# point tô the differnt persona
st.write("⬅ check out the diferent therapists available on sidebar")

# FIXED SITE HEADER
col1, col2 = st.columns([0.2,0.8])
image = Image.open(p[psycho]["picture"])

with col1:
   st.write('##')
   st.image(image)
with col2:
    st.title(p[psycho]["name"])
    st.write(p[psycho]["intro"])

# IF KEY IS AVAILABLE
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY 

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.gpt_assistant = []
        # Iniciar terapia com boas vindas do analista - run GPT
        completion = openai.ChatCompletion.create(
                    model=p[psycho]["model"],
                    messages = [ { "role": "system",
                                  "content": p[psycho]["system_content"]
                                  } ] + [ { "role": "user", "content": p[psycho]["openning_statement"] } ],
                    temperature = p[psycho]["temperature"],
                    max_tokens = p[psycho]["max_tokens"],
                    top_p = p[psycho]["top_p"],
                    frequency_penalty = p[psycho]["frequency_penalty"],
                    presence_penalty = p[psycho]["presence_penalty"]
                    )
        chat_response = completion.choices[0].message.content

        # Display assistant response in chat message container
        with st.chat_message("Assistant", avatar=p[psycho]["avatar"]):
            st.markdown(chat_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": chat_response})
        st.session_state.gpt_assistant = update_assistant(st.session_state.gpt_assistant, chat_response)
   
    # populate chat screen
    else:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=p[psycho]["avatar"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(p[psycho]["promptstamp"]):
        # Display user message in chat message container
        with st.chat_message("User", avatar="😟"):
            st.write(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # RUN GPT
        completion = openai.ChatCompletion.create(
                    model=p[psycho]["model"],
                    messages = [ { "role": "system",
                                  "content": p[psycho]["system_content"]
                                  } ] + st.session_state.gpt_assistant + [ { "role": "user", "content": prompt } ],
                    temperature = p[psycho]["temperature"],
                    max_tokens = p[psycho]["max_tokens"],
                    top_p = p[psycho]["top_p"],
                    frequency_penalty = p[psycho]["frequency_penalty"],
                    presence_penalty = p[psycho]["presence_penalty"]
                    )
        chat_response = completion.choices[0].message.content
        
        # Display assistant response in chat message container
        with st.chat_message("Assistant", avatar=p[psycho]["avatar"]):
            st.markdown(chat_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": chat_response})
        st.session_state.gpt_assistant = update_assistant(st.session_state.gpt_assistant, chat_response)
# in case API key unavailable
else:
    with st.chat_message("Assistant", avatar="🤖"):
        st.markdown("please provide API key to start your therapy")
