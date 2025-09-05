import math
from datetime import datetime
import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Advanced Calculator",
    page_icon="🧮",
    layout="centered",
)

# -----------------------------
# Helpers & State
# -----------------------------
def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []  # list of dicts: {time, op, inputs, result, error}

def format_number(x, precision):
    if isinstance(x, (int,)):
        return str(x)
    try:
        return f"{x:.{precision}f}"
    except Exception:
        return str(x)

def to_radians(x, angle_mode):
    return math.radians(x) if angle_mode == "Degrees" else x

def from_radians(x, angle_mode):
    return math.degrees(x) if angle_mode == "Degrees" else x

def add_history(op, inputs, result=None, error=None):
    st.session_state.history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": op,
        "inputs": inputs,
        "result": result,
        "error": error
    })

init_state()

# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    angle_mode = st.radio("Angle mode (for trig):", ["Degrees", "Radians"], horizontal=True)
    precision = st.slider("Result precision (decimals):", min_value=0, max_value=12, value=6)
    st.divider()
    st.markdown("### 🧠 Memory")
    colA, colB = st.columns(2)
    if colA.button("Clear history", use_container_width=True):
        st.session_state.history = []
        st.success("History cleared.")
    if colB.button("Copy last result", use_container_width=True):
        if st.session_state.history:
            last = st.session_state.history[-1]
            if last.get("error") is None and last.get("result") is not None:
                st.code(str(last["result"]), language="text")
            else:
                st.info("Last entry has no result to copy.")
        else:
            st.info("No history yet.")
    st.caption("History persists for the session.")

# -----------------------------
# Header
# -----------------------------
st.title("🧮 Advanced Calculator")
st.caption("Make your daily calculations easy")

# -----------------------------
# Tabs
# -----------------------------
tab_calc, tab_history = st.tabs(["Calculator", "History"])

with tab_calc:
    st.subheader("Select Operation")

    # Operation groups
    group = st.selectbox(
        "Category",
        ["Basic", "Advanced", "Trigonometry", "Inverse Trig", "Misc"],
        index=0
    )

    # Dynamic operation selection
    ops = {
        "Basic": ["Add", "Subtract", "Multiply", "Divide"],
        "Advanced": ["Power (x^y)", "Square Root", "Exponential (e^x)", "Natural Log (ln)", "Log Base 10", "Log (Custom Base)"],
        "Trigonometry": ["sin", "cos", "tan"],
        "Inverse Trig": ["arcsin", "arccos", "arctan"],
        "Misc": ["Absolute", "Factorial", "Percentage (x of y)"]
    }
    op = st.selectbox("Operation", ops[group])

    # -----------------------------
    # Inputs per operation
    # -----------------------------
    col1, col2 = st.columns(2)
    x = y = None
    base = None

    if group == "Basic":
        x = col1.number_input("First number (x)", value=0.0, step=1.0, format="%.10f")
        y = col2.number_input("Second number (y)", value=0.0, step=1.0, format="%.10f")
    elif group == "Advanced":
        if op == "Power (x^y)":
            x = col1.number_input("Base (x)", value=2.0, step=1.0, format="%.10f")
            y = col2.number_input("Exponent (y)", value=3.0, step=1.0, format="%.10f")
        elif op == "Square Root":
            x = col1.number_input("Value (x ≥ 0)", value=9.0, step=1.0, format="%.10f")
        elif op == "Exponential (e^x)":
            x = col1.number_input("Value (x)", value=1.0, step=1.0, format="%.10f")
        elif op == "Natural Log (ln)":
            x = col1.number_input("Value (x > 0)", value=2.718281828, step=1.0, format="%.10f")
        elif op == "Log Base 10":
            x = col1.number_input("Value (x > 0)", value=100.0, step=1.0, format="%.10f")
        elif op == "Log (Custom Base)":
            x = col1.number_input("Value (x > 0)", value=8.0, step=1.0, format="%.10f")
            base = col2.number_input("Base (b > 0, b ≠ 1)", value=2.0, step=1.0, format="%.10f")
    elif group == "Trigonometry":
        x = col1.number_input("Angle (x)", value=30.0, step=1.0, format="%.10f")
    elif group == "Inverse Trig":
        x = col1.number_input("Ratio (x)", value=0.5, step=0.1, format="%.10f")
    elif group == "Misc":
        if op == "Absolute":
            x = col1.number_input("Value (x)", value=-5.0, step=1.0, format="%.10f")
        elif op == "Factorial":
            # factorial only accepts non-negative integers
            x = col1.number_input("Non-negative integer (n)", value=5, min_value=0, step=1)
        elif op == "Percentage (x of y)":
            x = col1.number_input("Percent (x%)", value=15.0, step=1.0, format="%.10f")
            y = col2.number_input("Number (y)", value=200.0, step=1.0, format="%.10f")

    # -----------------------------
    # Compute
    # -----------------------------
    run = st.button("Calculate", type="primary", use_container_width=True)

    if run:
        result = None
        error = None
        try:
            if group == "Basic":
                if op == "Add":
                    result = x + y
                elif op == "Subtract":
                    result = x - y
                elif op == "Multiply":
                    result = x * y
                elif op == "Divide":
                    if y == 0:
                        raise ZeroDivisionError("Division by zero is undefined.")
                    result = x / y

            elif group == "Advanced":
                if op == "Power (x^y)":
                    result = math.pow(x, y)
                elif op == "Square Root":
                    if x < 0:
                        raise ValueError("Square root domain error: x must be ≥ 0.")
                    result = math.sqrt(x)
                elif op == "Exponential (e^x)":
                    result = math.exp(x)
                elif op == "Natural Log (ln)":
                    if x <= 0:
                        raise ValueError("Log domain error: x must be > 0.")
                    result = math.log(x)
                elif op == "Log Base 10":
                    if x <= 0:
                        raise ValueError("Log domain error: x must be > 0.")
                    result = math.log10(x)
                elif op == "Log (Custom Base)":
                    if x <= 0 or base is None or base <= 0 or base == 1:
                        raise ValueError("For log_b(x): x>0, b>0, b≠1.")
                    result = math.log(x, base)

            elif group == "Trigonometry":
                r = to_radians(x, angle_mode)
                if op == "sin":
                    result = math.sin(r)
                elif op == "cos":
                    result = math.cos(r)
                elif op == "tan":
                    result = math.tan(r)

            elif group == "Inverse Trig":
                # Validate domain for inverse trig
                if op in ["arcsin", "arccos"] and not (-1.0 <= x <= 1.0):
                    raise ValueError("Domain error: input must be in [-1, 1].")
                if op == "arcsin":
                    result = from_radians(math.asin(x), angle_mode)
                elif op == "arccos":
                    result = from_radians(math.acos(x), angle_mode)
                elif op == "arctan":
                    result = from_radians(math.atan(x), angle_mode)

            elif group == "Misc":
                if op == "Absolute":
                    result = abs(x)
                elif op == "Factorial":
                    if not (isinstance(x, int) and x >= 0):
                        raise ValueError("Factorial requires a non-negative integer.")
                    result = math.factorial(x)
                elif op == "Percentage (x of y)":
                    result = (x / 100.0) * y

            add_history(
                op=f"{group} → {op}",
                inputs={"x": x, "y": y, "base": base, "angle_mode": angle_mode},
                result=result,
            )
            st.success(f"Result: **{format_number(result, precision)}**")

        except Exception as e:
            error = str(e)
            add_history(
                op=f"{group} → {op}",
                inputs={"x": x, "y": y, "base": base, "angle_mode": angle_mode},
                error=error,
            )
            st.error(f"Error: {error}")

   # Quick constants
    st.divider()
    st.markdown("#### Quick Constants")
    c1, c2, c3 = st.columns(3)
    c1.metric("π", "3.141592653589793")
    c2.metric("e", "2.718281828459045")
    c3.metric("τ (2π)", "6.283185307179586")

with tab_history:
    st.subheader("Calculation History (this session)")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            with st.expander(f"🕒 {item['time']} — {item['operation']}"):
                st.write("**Inputs:**", item["inputs"])
                if item.get("error"):
                    st.error(item["error"])
                else:
                    st.write("**Result:**", item["result"])
    else:
        st.info("No calculations yet. Your results will appear here.")

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "Tip: Switch angle mode in the sidebar for trig functions. "
    "Adjust precision to format results."
)
