import streamlit as st
from src.algorithms import backtracking_search_display
from src.CSPS import AsteriskSudokuCSP
from src.utils import handle_sudoku_fail_message
from src.task2utils import sameCol, sameRow, sameHouse, asteriskNeighbours, given, allVals
import ast
import streamlit.components.v1 as components


# Set up neighbors
neighbors = {}


for i in range(1, 10):
  for j in range(1, 10):
    key = (i, j)
    neighbors[key] = set(sameCol(key) + sameRow(key) + sameHouse(key) + asteriskNeighbours(key))


# Set up domains
domains = {}

for i in range(1, 10):
  for j in range(1, 10):
    key = (i, j)
    domains[key] = allVals

# Set Pre-filled values
for key in given:
  domains[key] = given[key]


given_vars = set(given.keys())


st.set_page_config(page_title="CSP Backtracking Visualizer", layout="wide")
st.title("Asterisk Sudoku CSP Backtracking Visualizer")

# Initialize session state
if "steps" not in st.session_state:
    # Build CSP and compute steps once
    csp = AsteriskSudokuCSP(domains, neighbors)
    result, steps = backtracking_search_display(csp, fail_reason_function=handle_sudoku_fail_message)
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

            # Both A and X are assignments
            st.session_state.forward_count = max(0, st.session_state.forward_count - 1)

            # X is also backtracks after
            if kind == "X":
                st.session_state.backward_count = max(0, st.session_state.backward_count - 1)
                st.session_state.total_count = max(0, st.session_state.total_count - 1)

            st.session_state.total_count = max(0, st.session_state.total_count - 1)
            st.session_state.current_step_index -= 1

with col_buttons[2]:
    if st.button("Next Step ➡"):
        if st.session_state.current_step_index + 1 < len(steps):
            st.session_state.current_step_index += 1
            step = steps[st.session_state.current_step_index]
            parts = step.split("_", 3)
            kind = parts[0]

            st.session_state.forward_count += 1

            if kind == "X":
                st.session_state.backward_count += 1
                st.session_state.total_count += 1

            st.session_state.total_count += 1

with col_buttons[3]:
    if st.button("▶ Play All"):
        # Jump to final step and recompute counters
        st.session_state.current_step_index = len(steps) - 1
        forward = 0
        backward = 0
        total = 0
        for s in steps:
            kind = s.split("_", 1)[0]
            forward += 1
            total += 1
            if kind == "X":
                backward += 1
                total += 1
        st.session_state.forward_count = forward
        st.session_state.backward_count = backward
        st.session_state.total_count = total

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
    assignment = {var: val[0] for var, val in given.items()}  # start with givens

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

         # var is stored as a string like "(1, 1)" – convert back to tuple
        var_str = parts[1]
        var = ast.literal_eval(var_str)  # (row, col)

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
        st.success(f"Step {st.session_state.current_step_index + 1}: Assign **{val}** → **{var}**")
    elif kind == "X":
        reason = parts[3] if len(parts) == 4 else "No reason provided."
        st.error(
            f"Step {st.session_state.current_step_index + 1}: Cannot assign **{val}** → **{var}**\n\n"
            f"**Reason:** {reason}"
        )

# ------------------------------------------
# Sudoku board layout (9x9 grid)
# ------------------------------------------
st.subheader("Sudoku Board")

# Map from (row, col) -> value, where current_assignment keys are tuples like (r, c)
board = {}
for var, val in current_assignment.items():
    row, col = var
    board[(row, col)] = val

# Build HTML table for the whole board
rows_html = ""
for row in range(1, 10):
    row_cells = ""
    for col in range(1, 10):
        value = board.get((row, col))
        display_val = value if value is not None else ""

        # Thick borders for 3x3 boxes
        border_top = "2px solid #000" if row in (1,4,7) else "1px solid #999"
        border_left = "2px solid #000" if col in (1,4,7) else "1px solid #999"
        border_bottom = "2px solid #000" if row == 9 else "1px solid #999"
        border_right = "2px solid #000" if col == 9 else "1px solid #999"

        # Different background for given cells
        if (row, col) in given_vars:
            bg_color = "#444"  # dark gray for given
            font_weight = "bold"
        else:
            bg_color = "#222"  # slightly darker for CSP-assigned
            font_weight = "normal"

        row_cells += f"""
            <td style="
                width: 2.4rem;
                height: 2.4rem;
                text-align: center;
                vertical-align: middle;
                font-size: 1.2rem;
                color: white;
                border-top: {border_top};
                border-left: {border_left};
                border-right: {border_right};
                border-bottom: {border_bottom};
            ">
                {display_val}
            </td>
        """
    rows_html += f"<tr>{row_cells}</tr>"

board_html = f"""
<table cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
    {rows_html}
</table>
"""

# Render properly in Streamlit
components.html(board_html, height=400)  # adjust height as needed