import streamlit as st
from FinancialAnalyst import multi_ai_agent

st.set_page_config(page_title="Financial Analyst Chat", page_icon="📊")

st.title("📊 Financial Analyst AI")
st.markdown("Ask me about stock prices, analyst recommendations, or the latest company news.")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask about NVDA, TSLA, AAPL, MSFT..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    response = ""
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response_obj = multi_ai_agent.run(prompt)  # returns a RunResponse
                response = response_obj.content            # extract text
                st.markdown(response)
            except Exception as e:
                response = f"⚠️ Error: {e}"
                st.error(response)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": response})