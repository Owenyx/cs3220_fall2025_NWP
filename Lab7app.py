import streamlit as st
from src.algorithms import backtracking_search_display
from src.CSPS import dinnerAccomodationCSP
from src.utils import UniversalDict, handle_dinner_fail_message


neighbors = {
  'A': ['B', 'C', 'D', 'E'],
  'B': ['A', 'C', 'D', 'E'],
  'C': ['A', 'B', 'D', 'E'],
  'D': ['A', 'B', 'C', 'E'],
  'E': ['A', 'B', 'C', 'D']
}

domains = UniversalDict([1, 2, 3, 4, 5, 6])


st.set_page_config(page_title="CSP Backtracking Visualizer", layout="wide")
st.title("Dinner Table CSP Backtracking Visualizer")

# Initialize session state
if "steps" not in st.session_state:
    # Build CSP and compute steps once
    csp = dinnerAccomodationCSP(domains, neighbors)
    result, steps = backtracking_search_display(csp, fail_reason_function=handle_dinner_fail_message)
    st.session_state.csp_result = result
    st.session_state.steps = steps
    st.session_state.current_step_index = -1  # -1 = initial state (no steps applied yet)
    st.session_state.forward_count = 0  # "A_*_*"
    st.session_state.backward_count = 0  # "X_*_*"
    st.session_state.total_count = 0


steps = st.session_state.steps

# ------------------------------------------
# Controls
# ------------------------------------------
col_buttons = st.columns([1, 1, 1, 1])

with col_buttons[0]:
    if st.button("⏮ Reset to Start"):
        st.session_state.current_step_index = -1
        st.session_state.forward_count = 0
        st.session_state.backward_count = 0
        st.session_state.total_count = 0

with col_buttons[1]:
    if st.button("⬅ Previous Step"):
        if st.session_state.current_step_index >= 0:
            # Undo the effect of this step on counters
            step = steps[st.session_state.current_step_index]
            parts = step.split("_", 3)
            kind = parts[0]
            if kind == "A":
                st.session_state.forward_count = max(0, st.session_state.forward_count - 1)
            elif kind == "X":
                st.session_state.backward_count = max(0, st.session_state.backward_count - 1)
            st.session_state.total_count = max(0, st.session_state.total_count - 1)
            st.session_state.current_step_index -= 1

with col_buttons[2]:
    if st.button("Next Step ➡"):
        if st.session_state.current_step_index + 1 < len(steps):
            st.session_state.current_step_index += 1
            step = steps[st.session_state.current_step_index]
            parts = step.split("_", 3)
            kind = parts[0]
            if kind == "A":
                st.session_state.forward_count += 1
            elif kind == "X":
                st.session_state.backward_count += 1
            st.session_state.total_count += 1

with col_buttons[3]:
    if st.button("▶ Play All"):
        # Jump to final step and recompute counters
        st.session_state.current_step_index = len(steps) - 1
        forward = 0
        backward = 0
        for s in steps:
            kind = s.split("_", 1)[0]
            if kind == "A":
                forward += 1
            elif kind == "X":
                backward += 1
        st.session_state.forward_count = forward
        st.session_state.backward_count = backward
        st.session_state.total_count = len(steps)

# ------------------------------------------
# Step counters
# ------------------------------------------
st.subheader("Step Counters")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Forward steps", st.session_state.forward_count)
with c2:
    st.metric("Backward steps", st.session_state.backward_count)
with c3:
    st.metric("Total steps", st.session_state.total_count)

# ------------------------------------------
# Rebuild assignment from steps up to current index
# ------------------------------------------
def build_assignment_from_steps(steps, up_to_index):
    assignment = {}
    for i in range(up_to_index + 1):
        if i < 0:
            continue
        step = steps[i]
        # Possible formats:
        # "A_B_3"
        # "X_C_2"
        # "X_B_3_some reason"
        parts = step.split("_", 3)
        kind = parts[0]
        var = parts[1]
        val = int(parts[2])

        if kind == "A":
            assignment[var] = val
        elif kind == "X":
            # Failed attempt: ensure that if this was previously assigned, we undo it
            # but normally, assignments are undone by later steps in the algorithm.
            if assignment.get(var) == val:
                assignment.pop(var, None)
    return assignment


current_assignment = build_assignment_from_steps(steps, st.session_state.current_step_index)

# ------------------------------------------
# Current step info + reason
# ------------------------------------------
if st.session_state.current_step_index == -1:
    st.info("Initial state: no steps have been applied yet.")
else:
    step = steps[st.session_state.current_step_index]
    parts = step.split("_", 3)
    kind = parts[0]
    var = parts[1]
    val = parts[2]

    if kind == "A":
        st.success(f"Step {st.session_state.current_step_index + 1}: Assign **{var}** → **{val}**")
    elif kind == "X":
        reason = parts[3] if len(parts) == 4 else "No reason provided."
        st.error(
            f"Step {st.session_state.current_step_index + 1}: Cannot assign **{var}** → **{val}**\n\n"
            f"**Reason:** {reason}"
        )

# ------------------------------------------
# Dinner table layout with 6 boxes
# ------------------------------------------
st.subheader("Dinner Table Seating")

# Map seat number -> list of variables assigned there
seat_to_vars = {i: [] for i in range(1, 7)}
for v, seat in current_assignment.items():
    if seat in seat_to_vars:
        seat_to_vars[seat].append(v)

# Helper to render a seat as a box
def seat_box(seat_num, vars_here):
    label = f"Seat {seat_num}"
    if vars_here:
        content = ", ".join(sorted(vars_here))
    else:
        content = "—"
    st.markdown(
        f"""
        <div style="
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 0.5rem;
            text-align: center;
            min-width: 3rem;
        ">
            <div style="font-size: 0.8rem; color: #555;">{label}</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Layout:
#     [1]
#  [6]   [2]
#  [5]   [3]
#     [4]
top = st.columns([4, 1, 4])
with top[1]:
    seat_box(1, seat_to_vars[1])

mid1 = st.columns([1, 1])
with mid1[0]:
    seat_box(6, seat_to_vars[6])
with mid1[1]:
    seat_box(2, seat_to_vars[2])

mid2 = st.columns([1, 1])
with mid2[0]:
    seat_box(5, seat_to_vars[5])
with mid2[1]:
    seat_box(3, seat_to_vars[3])

bottom = st.columns([4, 1, 4])
with bottom[1]:
    seat_box(4, seat_to_vars[4])