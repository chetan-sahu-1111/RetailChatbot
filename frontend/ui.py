import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Retail Chatbot", layout="wide")

st.title("🛒 Retail Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.chat_input("Ask about your shop...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "https://retailchatbot-p8pa.onrender.com/chat",
                json={"query": user_input}
            )

            data = response.json()

            st.session_state.messages.append({
                "role": "assistant",
                "content": data
            })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": {"error": str(e)}
            })

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        
        # USER MESSAGE
        if msg["role"] == "user":
            st.write(msg["content"])
        
        # BOT MESSAGE
        else:
            content = msg["content"]

            if "error" in content:
                st.error(content["error"])
            else:
                # Show SQL Query
                st.subheader("🧾 Generated SQL")
                st.code(content.get("final_sql", ""), language="sql")

                # Show Result Table
                st.subheader("📊 Result")
                result = content.get("result", [])

                if result:
                    df = pd.DataFrame(result)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No data found")
