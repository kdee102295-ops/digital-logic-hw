import streamlit as st
import random
import schemdraw
import schemdraw.logic as logic
import matplotlib.pyplot as plt

# Title of the App
st.title("Digital Logic Practice")
st.write("Solve the circuit below. Refresh or click 'New Problem' to try again.")

# --- 1. State Management ---
if 'input_a' not in st.session_state:
    st.session_state['input_a'] = random.choice([0, 1])
    st.session_state['input_b'] = random.choice([0, 1])
    st.session_state['gate_type'] = random.choice(["AND", "OR", "XOR", "NAND"])

def new_problem():
    st.session_state['input_a'] = random.choice([0, 1])
    st.session_state['input_b'] = random.choice([0, 1])
    st.session_state['gate_type'] = random.choice(["AND", "OR", "XOR", "NAND"])

# --- 2. Draw the Circuit (FIXED METHOD) ---
# Define logic for calculation
gate_logic = {
    "AND": lambda a, b: a & b,
    "OR":  lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
    "NAND": lambda a, b: int(not(a & b))
}

correct_answer = gate_logic[st.session_state['gate_type']](
    st.session_state['input_a'], 
    st.session_state['input_b']
)

# THE FIX: Create the Matplotlib Figure explicitly first
# This guarantees 'fig' exists and is valid.
fig, ax = plt.subplots() 
ax.axis('off') # Turn off the X/Y axis borders

# Tell Schemdraw to draw ON TOP OF the axis we just created
d = schemdraw.Drawing(canvas=ax)
d.config(fontsize=14)

# Select the correct gate
if st.session_state['gate_type'] == "AND":
    gate_element = logic.And()
elif st.session_state['gate_type'] == "OR":
    gate_element = logic.Or()
elif st.session_state['gate_type'] == "XOR":
    gate_element = logic.Xor()
elif st.session_state['gate_type'] == "NAND":
    gate_element = logic.Nand()

# Add elements
G = d.add(gate_element)
d.add(logic.Line().left(1).at(G.in1).label(f"A={st.session_state['input_a']}", 'left'))
d.add(logic.Line().left(1).at(G.in2).label(f"B={st.session_state['input_b']}", 'left'))
d.add(logic.Line().right(1).at(G.out).label("?", 'right'))

# Render the drawing onto our 'fig'
d.draw(show=False)

# Pass the explicit figure to Streamlit
st.pyplot(fig)

# --- 3. Student Interaction ---
with st.form("answer_form"):
    user_ans = st.number_input("Output (0 or 1):", min_value=0, max_value=1)
    submitted = st.form_submit_button("Check Answer")

    if submitted:
        if user_ans == correct_answer:
            st.success("✅ Correct! Take a screenshot if you need to submit this.")
        else:
            st.error("❌ Incorrect. Try again.")

st.button("Generate New Problem", on_click=new_problem)