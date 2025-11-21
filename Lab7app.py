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
if "raw_steps" not in st.session_state:
    # Build CSP and compute steps once
    csp = dinnerAccomodationCSP(domains, neighbors)
    result, steps = backtracking_search_display(csp, fail_reason_function=handle_dinner_fail_message)
    st.session_state.csp_result = result
    st.session_state.raw_steps = steps  # original steps from algorithm
    st.session_state.current_step_index = -1  # -1 = initial state (no steps applied yet)
    st.session_state.forward_count = 0  # "A_*_*"
    st.session_state.backward_count = 0  # counts B (backtracks) and optionally X if you prefer
    st.session_state.total_count = 0

# Expand raw steps into display steps that include explicit backtrack steps (B_...)
def expand_steps_with_backtracks(raw_steps):
    """
    Build display_steps from raw_steps by inserting a 'B_<var>_<val>_backtrack' step
    immediately after each failure 'X_...' when there is an assignment to undo.
    We simulate the assignment stack while expanding so the synthetic B steps match what
    would be undone.
    """
    display_steps = []
    assign_stack = []  # stack of (var, val) representing currently assigned in simulation

    for raw in raw_steps:
        # Keep the original failed reason (if any) after the third underscore
        parts = raw.split("_", 3)
        kind = parts[0]

        if kind == "A":
            # Format: A_var_val
            display_steps.append(raw)
            try:
                var = parts[1]
                val = int(parts[2])
            except Exception:
                # if format is unexpected, just append and continue
                continue
            assign_stack.append((var, val))

        elif kind == "X":
            # Format: X_var_val[_reason...]
            display_steps.append(raw)
            # After a fail, algorithm backtracks: undo the most recent assignment (if any)
            if assign_stack:
                last_var, last_val = assign_stack.pop()
                # Make a synthetic backtrack step; include a short reason token "backtrack"
                display_steps.append(f"B_{last_var}_{last_val}_backtrack")

        else:
            # Unknown step kind (preserve to be safe)
            display_steps.append(raw)

    return display_steps

# Build display steps and put in session (only once)
if "steps" not in st.session_state:
    st.session_state.steps = expand_steps_with_backtracks(st.session_state.raw_steps)

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
            kind = step.split("_", 1)[0]
            # Count B as backward, X as backward as well if you want; A as forward
            if kind == "A":
                st.session_state.forward_count = max(0, st.session_state.forward_count - 1)
            elif kind == "B":
                st.session_state.backward_count = max(0, st.session_state.backward_count - 1)
            elif kind == "X":
                # Optional: count X as backward as well if desired
                st.session_state.backward_count = max(0, st.session_state.backward_count - 1)
            st.session_state.total_count = max(0, st.session_state.total_count - 1)
            st.session_state.current_step_index -= 1

with col_buttons[2]:
    if st.button("Next Step ➡"):
        if st.session_state.current_step_index + 1 < len(steps):
            st.session_state.current_step_index += 1
            step = steps[st.session_state.current_step_index]
            kind = step.split("_", 1)[0]
            if kind == "A":
                st.session_state.forward_count += 1
            elif kind == "B":
                st.session_state.backward_count += 1
            elif kind == "X":
                # Optional: count X as backward as well if you want; currently treat X as backward too
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
            elif kind in ("B", "X"):
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
    """
    Interpret these step kinds:
      - A_var_val         : assign var -> val
      - X_var_val_reason  : failed attempt (no change to assignment)
      - B_var_val_backtrack: explicit undo of var=val (pop)
    """
    assignment = {}
    for i in range(up_to_index + 1):
        if i < 0:
            continue
        step = steps[i]
        parts = step.split("_", 3)
        kind = parts[0]
        # guard against malformed steps
        if len(parts) < 3:
            continue
        var = parts[1]
        try:
            val = int(parts[2])
        except Exception:
            # if synthetic reason text is in parts[2], try to ignore
            continue

        if kind == "A":
            assignment[var] = val
        elif kind == "B":
            # explicit backtrack: undo the assignment if it matches
            if assignment.get(var) == val:
                assignment.pop(var, None)
        elif kind == "X":
            # failure attempt: usually nothing to do; keep as-is
            # but if a failing step somehow left the var assigned to this value, remove it
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
    var = parts[1] if len(parts) > 1 else "?"
    val = parts[2] if len(parts) > 2 else "?"
    if kind == "A":
        st.success(f"Step {st.session_state.current_step_index + 1}: Assign **{var}** → **{val}**")
    elif kind == "X":
        reason = parts[3] if len(parts) == 4 else "No reason provided."
        st.error(
            f"Step {st.session_state.current_step_index + 1}: Cannot assign **{var}** → **{val}**\n\n"
            f"**Reason:** {reason}"
        )
    elif kind == "B":
        # show backtrack message
        st.info(f"Step {st.session_state.current_step_index + 1}: Backtrack undo **{var}** → **{val}**")

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
