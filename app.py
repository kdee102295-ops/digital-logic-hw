import streamlit as st
import random
import schemdraw
import schemdraw.logic as logic
import matplotlib.pyplot as plt

# Title of the App
st.title("Digital Logic Practice")
st.write("Solve the circuit below. Refresh or click 'New Problem' to try again.")

# --- 1. State Management ---
# We need to store the problem so it doesn't disappear when you click "Submit"
if 'input_a' not in st.session_state:
    st.session_state['input_a'] = random.choice([0, 1])
    st.session_state['input_b'] = random.choice([0, 1])
    st.session_state['gate_type'] = random.choice(["AND", "OR", "XOR", "NAND"])

# Helper function to reset the problem
def new_problem():
    st.session_state['input_a'] = random.choice([0, 1])
    st.session_state['input_b'] = random.choice([0, 1])
    st.session_state['gate_type'] = random.choice(["AND", "OR", "XOR", "NAND"])
    # Clear previous user input if possible or just let them overwrite

# --- 2. Draw the Circuit ---
# Define logic for calculation
gate_logic = {
    "AND": lambda a, b: a & b,
    "OR":  lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
    "NAND": lambda a, b: int(not(a & b))
}

# Calculate correct answer based on stored state
correct_answer = gate_logic[st.session_state['gate_type']](
    st.session_state['input_a'], 
    st.session_state['input_b']
)

# Drawing logic
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14)
    
    # Select the correct gate element dynamically
    if st.session_state['gate_type'] == "AND":
        gate_element = logic.And()
    elif st.session_state['gate_type'] == "OR":
        gate_element = logic.Or()
    elif st.session_state['gate_type'] == "XOR":
        gate_element = logic.Xor()
    elif st.session_state['gate_type'] == "NAND":
        gate_element = logic.Nand()
        
    G = d.add(gate_element)
    
    # Add inputs
    d.add(logic.Line().left(1).at(G.in1).label(f"A={st.session_state['input_a']}", 'left'))
    d.add(logic.Line().left(1).at(G.in2).label(f"B={st.session_state['input_b']}", 'left'))
    
    # Add output
    d.add(logic.Line().right(1).at(G.out).label("?", 'right'))
    
    # Render the drawing into Streamlit
    st.pyplot(d.fig)

# --- 3. Student Interaction ---
with st.form("answer_form"):
    user_ans = st.number_input("Output (0 or 1):", min_value=0, max_value=1)
    submitted = st.form_submit_button("Check Answer")

    if submitted:
        if user_ans == correct_answer:
            st.success("✅ Correct! Take a screenshot if you need to submit this.")
        else:
            st.error("❌ Incorrect. Try again.")

# Button to generate next problem
st.button("Generate New Problem", on_click=new_problem)