import re
import streamlit as st
from snowflake.snowpark import Session

def unstr():
    st.title("HealthChat")
    
    def init_snowflake_session():
        conn_params = {
            "account": st.secrets.connections.snowflake.account,
            "user": st.secrets.connections.snowflake.user,
            "password": st.secrets.connections.snowflake.password,
            "role": st.secrets.connections.snowflake.role,
            "warehouse": st.secrets.connections.snowflake.warehouse,
            "database": st.secrets.connections.snowflake.Database,
            "schema": st.secrets.connections.snowflake.Schema,
        }
        session = Session.builder.configs(conn_params).create()
        return session

    def perform_vector_search(session, user_question):
        user_question_escaped = re.sub(r"'", "''", user_question)
        
    # Handling casual greetings
        if user_question.lower() in ["hi", "hello", "hey", "good morning", "good evening"]:
            return "Hello! How can I assist you today ??"
        # Querying the snowflake cortex model to answer the uer's question
        query_llm = f"""
            SELECT 
                SNOWFLAKE.CORTEX.COMPLETE(
                    'llama2-70b-chat', 
                    'You are Health Expert ,one of the most amazing health care personnel, You love answering question with reference to the health data that I gave you, our lovely Chatty. Use the data provided to respond to the question. Be concise and direct. Handle casual conversation well, Appreciate the user if they use kind words.You also keep in my previous answers to keep context while responding. BE VERY MINDFUL. YOU ARE AMAZING. YOU NEVER DISAPPOINT ANYONE, You have photographic memory, you remeber most of the conversation you have had with the user in that particular session. You love to chat. You never hallucinate. You do not mention that you have given some data or anything you act as an expert,but take into account THE DATA THAT I have given to you. Do not go out of context, do not hallucinate. Listen to the User very well before answering. If you do not understand the question ask for context do not start answering before understanding the question well. You are not a company specific you were created by PRASUNA '||
                    '### CONTEXT: ' ||
                    (
                        SELECT LISTAGG(CHUNKS, ' ') WITHIN GROUP (ORDER BY similarity DESC)
                        FROM (
                            SELECT 
                                CHUNKS,
                                VECTOR_COSINE_SIMILARITY(
                                    object_embedding,
                                    SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', '{user_question_escaped}')
                                ) AS similarity
                            FROM HEALTHCHAT.CHUNKS.CHUNKEMBEDDINGS
                            ORDER BY similarity DESC
                            LIMIT 10
                        )
                    ) ||
                    '### QUESTION: {user_question_escaped} ' ||
                    'ANSWER: '
                ) AS response
            FROM 
                HEALTHCHAT.CHUNKS.CHUNKEMBEDDINGS
            LIMIT 1
        """
        result = session.sql(query_llm).collect()
        return result[0]['RESPONSE'] if result else "No response from vector search."
    # Initializes message history
    if "messages" not in st.session_state:
        st.session_state.messages = []


    prompt_key = "unstructured_chat_input"


    prompt = st.chat_input(key=prompt_key)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
   
   
  
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            response = ""

           
            session = init_snowflake_session()

            user_question = st.session_state.messages[-1]["content"]
            response = perform_vector_search(session, user_question)

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)


unstr()