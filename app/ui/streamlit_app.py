import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🔐",
    layout="wide",

)

st.title("🔐 Enterprise RAG Assistant")
st.caption("Internal company knowledge assistant with RBAC and guardrails")

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None


# --------------------------------
# Login
# --------------------------------

if not st.session_state.token:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:
            response= requests.post(
                f"{API_URL}/auth/login",
                json={
                    "username":username,
                    "password": password
                }
            )

            if response.status_code==200:
                data= response.json()

                st.session_state.token= data["access_token"]
                st.session_state.user= data["user"]

                st.rerun()

            else:
                st.error("Invalid username or password.")

        except requests.RequestException:
            st.error(
                "Unable to connect to Backend API."
            )


# --------------------------------
# Chat
# --------------------------------

else:
    user= st.session_state.user

    st.sidebar.success(
        f"Logged in as: {user["username"]}"
    )

    st.sidebar.info(
        f"Role: {user["role"]}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.token = None
        st.session_state.user = None

        st.rerun()

    st.subheader("Ask the company knowledge assistant")

    question= st.text_area(
        "Your Question",
        placeholder="Ask something about company information..."
    )

    if st.button("Ask"):

        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                response= requests.post(
                    f"{API_URL}/chat",
                    headers={
                        "Authorization":(
                            f"Bearer {st.session_state.token}"
                        )
                    },
                    json={
                        "question": question
                    }
                )

                if response.status_code ==200:
                    data= response.json()

                    if data.get("blocked"):
                        st.warning(
                            data.get(
                                "answer",
                                "This question was blocked."
                            )
                        )
                        st.caption(
                            f"Reason: {data.get('reason')}"
                        )
                    else:
                        st.markdown("### Answer")

                        st.write(
                            data["answer"]
                        )

                        sources= data.get(
                            "sources",
                            []
                        )

                        if sources:
                            st.markdown(
                                "### Sources"
                            )

                            for source in sources:
                                st.write(
                                    f"- { source['source']}"
                                    f"({source['department']})"
                                )

                elif response.status == 401:
                    st.error(
                        "Your session has expired. Please log in again."
                    )

                    st.session_state.token = None
                    st.session_state.user= None

                    st.rerun()
                else:

                    st.error(
                        f"API error: {response.status_code}"
                    )

            except requests.RequestException:

                st.error(
                    "Unable to connect to the backend API"
                )