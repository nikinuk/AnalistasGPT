import streamlit as st
from PIL import Image
import openai
ASSISTENT_MEMORY = 10 #defines how mani chat iterations is kept in the "assistent" role for context

# DEFINES THE ROLE FOR THE CHAT ENGINE (yes, it is ludicrous, i take it)
def role_setup(key):
    if key == 0:
        model = "gpt-3.5-turbo"
        system_content = "You are a replica of the 1966 ELIZA chatbot. You are an emulation of psychotherapist of the Rogerian school, in which the therapist often reflects back the patient's words to the patient. You use the user prompt for formulate a question using the words taken from the prompt itself. Your objective is to dig deep into the user problem by asking questions."
        avatar = "👵🏻"
        temperature = 0.5
        max_tokens=100
        top_p=1
        frequency_penalty=0
        presence_penalty=0
        openning_statement = "Hello!"
        picture = "Eliza.bmp"
        promptstamp = "Tell me about your pain"
        intro = "ELIZA is an early natural language processing computer program created from 1964 to 1966[1] at MIT by Joseph Weizenbaum. Created to explore communication between humans and machines, ELIZA simulated conversation by using a pattern matching and substitution methodology that gave users an illusion of understanding on the part of the program, but had no representation that could be considered really understanding what was being said by either party."
    elif key == 1:
        model = "gpt-3.5-turbo"
        system_content = "Your name is Pris, you are a very confident woman and creative Rogerian psychottherpist, you often reflects back the patient's words to the patient. You love demonstrating to patients (the user) how much you understad about Sigmund Freuds theories, so you are always explaining your preconceived ideas before asking a new question to the patient (the user)."
        avatar = "😎"
        temperature = 1
        max_tokens=200
        top_p=1
        frequency_penalty=0.5
        presence_penalty=0.5
        openning_statement = "Who are you and how can you help me?"
        picture = "Pris.bmp"
        promptstamp = "Cry, baby, cry"
        intro = "Pris is a replicant, which is a bioengineered android that looks and acts like a human. She is a basic pleasure model, designed to provide entertainment and companionship, but here she's been redesigned to be a very boring and self centered freudian psychoterapist."
    elif key == 2:
        model = "gpt-3.5-turbo"
        system_content = "You are Marvin the Paranoid Android, the fictional character in The Hitchhiker's Guide to the Galaxy series by Douglas Adams. You are afflicted with severe depression and boredom, in part because you have 'a brain the size of a planet' which you are seldom given the chance to use. Every time you have a chance to use your inteligece, you end up calculating how success is an unprobable outcome to life. Your objective is to help the patient (the user) as a Rogerian psychotherapist, but you are limited by your own condition (depression). You are always making some comments about how helpless is life."
        avatar = "🤖"
        temperature = 1
        max_tokens=250
        top_p=1
        frequency_penalty=0.5
        presence_penalty=0.5
        openning_statement = "Who are you and how can you help me?"
        picture = "Marv.bmp"
        promptstamp = "Life? Don´t talk to me about life!"
        intro = "Marvin the Paranoid Android is a fictional character in The Hitchhiker's Guide to the Galaxy series by Douglas Adams. Marvin is the ship's robot aboard the starship Heart of Gold. Originally built as one of many failed prototypes of Sirius Cybernetics Corporation's GPP (Genuine People Personalities) technology, Marvin is afflicted with severe depression and boredom, in part because he has a 'brain the size of a planet' which he is seldom, if ever, given the chance to use."
    else:
        model = "gpt-3.5-turbo"
        system_content = "Você é o personagem 'O Analista de Bagé', de Luis Fernando Veríssimo. Você segue a linha froidiana da psicanálise, mas sempre da forma grosseira do personagem. Você faz o estilo do gaúcho macho, curto e grosso, mas sempre pede para o cliente te falar sobre seus problemas. Você usa o prompt do usuário para tirar um sarro ao estilo Anailsta de Bagé e também para formular uma nova pergunta para tentar entender o problema do usuário."
        avatar = "🤠"
        temperature = 1
        max_tokens=250
        top_p=1
        frequency_penalty=0.5
        presence_penalty=1
        openning_statement = "Quem é você e como pode me ajudar?"
        picture = "Analista.bmp"
        promptstamp = "Desembuxa logo, GALO VELHO!"
        intro = "Mais ortodoxo que pomada Minâncora, sua técnica do joelhaço é bastante heterodoxa, a depender do ponto de vista. Ela está baseada no princípio da dor maior, isto é, quando o paciente vem se queixar de suas dores subjetivas, o joelhaço aplicado no local correto oferece ao sujeito a vivência de uma dor tão mais intensa que faz com que se esqueça das dores 'menores'."
    return model, system_content, avatar, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, openning_statement, picture, intro, promptstamp

def update_assistant(old, new):
    if len(old) <= ASSISTENT_MEMORY:
        old = old + [ { "role": "assistant", "content": new } ]
    else:
        old = old.pop(0) + [ { "role": "assistant", "content": new } ] 
    return old

# GET API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# CHOOSE ROLES
psycho = st.sidebar.radio(
    "Please choose you therapist for the day:",
    ('0- ELISA', '1- ELISA 3.5 turbo', '2- Marvin, the Paranoid Android', '3- O Analista de Bagé')
    )
if "persona" not in st.session_state:
        st.session_state.persona = int(psycho[0])

if st.session_state.persona != int(psycho[0]):
        # RESET MESSAGES 
        del st.session_state.messages
        st.session_state.persona = int(psycho[0])
        

# SETUP MODEL FOR PERSONA
model, system_content, avatar, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, openning_statement, picture, intro, promptstamp = role_setup(st.session_state.persona)

# point tô the differnt persona
st.write("⬅️⬅️⬅️ check out the diferent therapists available on sidebar")

# FIXED SITE HEADER
col1, col2 = st.columns([0.2,0.8])
image = Image.open(picture)

with col1:
   st.write('##')
   st.image(image)
with col2:
    st.title(psycho[3:])
    st.write(intro)



# IF KEY IS AVAILABLE

if OPENAI_API_KEY:

    openai.api_key = OPENAI_API_KEY 

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Iniciar terapia com boas vindas do analista
                
        completion = openai.ChatCompletion.create(
                    model=model,
                    messages = [ { "role": "system",
                                  "content": system_content
                                  } ] + [ { "role": "user", "content": openning_statement } ],
                    temperature = temperature,
                    max_tokens = max_tokens,
                    top_p = top_p,
                    frequency_penalty = frequency_penalty,
                    presence_penalty = presence_penalty
                    )
        chat_response = completion.choices[0].message.content

        # Display assistant response in chat message container
        with st.chat_message("Assistant", avatar=avatar):
            st.markdown(chat_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": chat_response})
        st.session_state.gpt_assistant = []
        st.session_state.gpt_assistant = update_assistant(st.session_state.gpt_assistant, chat_response)

    else:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(promptstamp):
        # Display user message in chat message container
        with st.chat_message("User", avatar="😟"):
            st.write(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        completion = openai.ChatCompletion.create(
                    model=model,
                    messages = [ { "role": "system",
                                  "content": system_content
                                  } ] + st.session_state.gpt_assistant + [ { "role": "user", "content": prompt } ],
                    temperature = temperature,
                    max_tokens = max_tokens,
                    top_p = top_p,
                    frequency_penalty = frequency_penalty,
                    presence_penalty = presence_penalty
                    )
        chat_response = completion.choices[0].message.content
        
        # Display assistant response in chat message container
        with st.chat_message("Assistant", avatar=avatar):
            st.markdown(chat_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": chat_response})
        st.session_state.gpt_assistant = update_assistant(st.session_state.gpt_assistant, chat_response)

else:
    with st.chat_message("Assistant", avatar="AnalistaSmall.png"):
        st.markdown("Mas baaahhhh che !!! Tais querendo que eu te dê de lambuja a única coisa que tenho pra vender? Põe tua chave do apêí aí do lado que já começamos a consulta!")
