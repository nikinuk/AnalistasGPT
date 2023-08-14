import streamlit as st
from PIL import Image
import openai
import json
ASSISTENT_MEMORY = 10 #defines how many chat iterations is kept in the "assistent" role for context
OPENAI_API_KEY = ""

def update_assistant(old, new):
    # Adds new "assistent" entries in the chat context, limited by choosen ASSISTENT_MEMORY
    if len(old) > ASSISTENT_MEMORY:
        old.pop(0)
    old = old + [ { "role": "assistant", "content": new } ] 
    return old
def set_avatar(user):
    if user == "user":
        return "😟"
    else:
        return p[psycho]["avatar"]

autentication_type = st.sidebar.radio(
    "Choose autentication type:",
    ("password", "my own OPENAI_API_KEY")
    )
if "autentication" not in st.session_state:
    st.session_state.autentication = autentication_type
st.session_state.autentication = autentication_type
pwd = st.sidebar.text_input("type your password or APY key", type="password")
if st.session_state.autentication == "password":
    if pwd == st.secrets["PASSWORD"]:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    OPENAI_API_KEY = pwd
    
#LOAD persona list
if "personas" not in st.session_state:
    # Opening JSON file
    with open('personas.json', encoding='utf-8') as openfile:
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
    "Choose you therapist for the day:",
    st.session_state.names
    )
psycho = str(st.session_state.names.index(psycho))
if "persona" not in st.session_state: # initialize state
        st.session_state.persona = "0"

if st.session_state.persona != psycho:  # when the persona changes, reset messages 
        # RESET MESSAGES 
        if "messages" in st.session_state:
            del st.session_state.messages
        st.session_state.persona = psycho

#Credits 
nikinuk = Image.open("nikinuk.png")
i2a2 = Image.open("i2a2.jpg")
oai = Image.open("OIP.jpg")
sml = Image.open("stm.jpg")
st.sidebar.write("##\n##")

cr1, cr2, cr3, cr4 = st.sidebar.columns(4)
cr1.image(nikinuk, width=40)
cr2.image(i2a2, width=40)
cr3.image(oai, width=40)
cr4.image(sml, width=40)
st.sidebar.write("*-Psycho Clinic by [Nich Arand](https://www.linkedin.com/in/nicholas-arand-233a911/)* \n *-Dominando Redes Generativas [i2a2](https://www.i2a2.academy/dominando-redes-generativas)* \n *-Powered by [OPENAI_GPT3.5 turbo](https://openai.com/)* \n *-Hosted by [Streamlit](https://streamlit.io/)*")

#MAIN PAGE
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
   
    # populate chat screen after first iteration
    else:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=set_avatar(message["role"])):
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
        st.markdown("please provide a valid password or a valid OPENAI API key to start your therapy")
