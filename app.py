import streamlit as st
import random
import schemdraw
import schemdraw.logic as logic
import matplotlib.pyplot as plt
import sympy
from sympy.logic import SOPform, simplify_logic

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Digital Logic Design", layout="wide")

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("Classroom Tools")
app_mode = st.sidebar.radio("Select a Practice Mode:", ["Visual Logic Gates", "Sum of Minterms"])

# ==========================================
# MODE 1: VISUAL LOGIC GATES
# ==========================================
def page_logic_gates():
    st.title("🔌 Visual Logic Gates")
    st.write("Determine the output of the logic gate shown below.")

    # 1. State Management
    if 'gate_input_a' not in st.session_state:
        st.session_state['gate_input_a'] = random.choice([0, 1])
        st.session_state['gate_input_b'] = random.choice([0, 1])
        st.session_state['gate_type'] = random.choice(["AND", "OR", "XOR", "NAND"])

    def new_gate_problem():
        st.session_state['gate_input_a'] = random.choice([0, 1])
        st.session_state['gate_input_b'] = random.choice([0, 1])
        st.session_state['gate_type'] = random.choice(["AND", "OR", "XOR", "NAND"])

    # 2. Logic Calculation
    gate_logic = {
        "AND": lambda a, b: a & b,
        "OR":  lambda a, b: a | b,
        "XOR": lambda a, b: a ^ b,
        "NAND": lambda a, b: int(not(a & b))
    }
    
    correct_answer = gate_logic[st.session_state['gate_type']](
        st.session_state['gate_input_a'], 
        st.session_state['gate_input_b']
    )

    # 3. Draw Circuit (The Safe Way)
    fig, ax = plt.subplots(figsize=(4, 2)) 
    ax.axis('off')
    
    d = schemdraw.Drawing(canvas=ax)
    d.config(fontsize=14)

    if st.session_state['gate_type'] == "AND": gate_element = logic.And()
    elif st.session_state['gate_type'] == "OR": gate_element = logic.Or()
    elif st.session_state['gate_type'] == "XOR": gate_element = logic.Xor()
    elif st.session_state['gate_type'] == "NAND": gate_element = logic.Nand()

    G = d.add(gate_element)
    d.add(logic.Line().left(1).at(G.in1).label(f"A={st.session_state['gate_input_a']}", 'left'))
    d.add(logic.Line().left(1).at(G.in2).label(f"B={st.session_state['gate_input_b']}", 'left'))
    d.add(logic.Line().right(1).at(G.out).label("?", 'right'))
    
    d.draw(show=False)
    st.pyplot(fig)

    # 4. User Input
    col1, col2 = st.columns([1, 2]) # Make input small
    with col1:
        with st.form("gate_form"):
            user_ans = st.number_input("Output (0 or 1):", min_value=0, max_value=1)
            submitted = st.form_submit_button("Check Answer")

            if submitted:
                if user_ans == correct_answer:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect.")

    st.button("New Gate Problem", on_click=new_gate_problem)

# ==========================================
# MODE 2: SUM OF MINTERMS
# ==========================================
def page_minterms():
    st.title("∑ Sum of Minterms")
    st.markdown("Given the simplified function, select all **Minterms**.")

    x, y, z = sympy.symbols('x y z')

    # 1. State Management
    if 'target_minterms' not in st.session_state:
        num_terms = random.randint(1, 6)
        st.session_state['target_minterms'] = sorted(random.sample(range(8), num_terms))

    def new_minterm_problem():
        num_terms = random.randint(1, 6)
        st.session_state['target_minterms'] = sorted(random.sample(range(8), num_terms))

    # 2. Generate Question
    minterms = st.session_state['target_minterms']
    full_expr = SOPform([x, y, z], minterms)
    simplified_expr = simplify_logic(full_expr)

    st.markdown("### Problem:")
    st.latex(f"F(x, y, z) = {sympy.latex(simplified_expr)}")

    st.write("Select the minterms:")
    
    # 3. Form Interface
    cols = st.columns(4)
    user_selection = []
    for i in range(8):
        col_index = i % 4
        with cols[col_index]:
            bin_rep = format(i, '03b')
            if st.checkbox(f"m{i} ({bin_rep})", key=f"minterm_{i}"):
                user_selection.append(i)

    st.write("---")
    if st.button("Check Minterms"):
        user_selection.sort()
        minterms.sort()
        if user_selection == minterms:
            st.success("✅ Correct!")
            st.balloons()
        else:
            st.error("❌ Incorrect.")
            st.write(f"**Correct Answer:** $\sum m({', '.join(map(str, minterms))})$")

    st.button("New Minterm Problem", on_click=new_minterm_problem)

# ==========================================
# MAIN EXECUTION
# ==========================================
if app_mode == "Visual Logic Gates":
    page_logic_gates()
elif app_mode == "Sum of Minterms":
    page_minterms()