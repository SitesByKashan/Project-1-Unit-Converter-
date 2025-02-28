import streamlit as st
import pint

st.set_page_config(page_title="🚀 Unit Converter")

# Pint library for unit conversion
ureg = pint.UnitRegistry()
ureg.define('square_meter = meter ** 2')
ureg.define('square_kilometer = kilometer ** 2')
ureg.define('square_centimeter = centimeter ** 2')
ureg.define('square_millimeter = millimeter ** 2')
ureg.define('square_mile = mile ** 2')
ureg.define('square_yard = yard ** 2')
ureg.define('square_foot = foot ** 2')
ureg.define('square_inch = inch ** 2')

# Session state to store conversion history
if 'history' not in st.session_state:
    st.session_state.history = []

# **Custom Styling**
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #74ebd5, #acb6e5);
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            color: white;
            font-size: 50px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .stButton>button {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 12px;
            width: 100%;
            transition: all 0.3s ease-in-out;
            border: none;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #2575fc, #6a11cb);
            transform: scale(1.05);
        }
        .stTextInput>div>div>input, .stSelectbox>div {
            border-radius: 8px;
            border: 2px solid #6a11cb;
            padding: 10px;
            background: #f4f4f4;
            font-size: 16px;
        }
        
        .stMarkdown {
            color: #2c3e50;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)


# **Unit Categories**
unit_categories = {
    "📏 Length": ["meter", "kilometer", "centimeter", "millimeter", "micrometer", "nanometer", "mile", "yard", "foot", "inch", "light_year"],
    "🌡 Temperature": ["celsius", "fahrenheit", "kelvin"],
    "📐 Area": ["square_meter", "square_kilometer", "square_centimeter", "square_millimeter", "square_mile", "square_yard", "square_foot", "square_inch"],
    "🧊 Volume": ["liter", "milliliter", "cubic_meter", "cubic_centimeter", "gallon", "quart", "pint", "cup", "fluid_ounce"],
    "⚖ Weight": ["gram", "kilogram", "milligram", "microgram", "ton", "pound", "ounce"],
    "⏳ Time": ["second", "minute", "hour", "day", "week", "month", "year"]
}

# **Category Selection**
st.subheader("Select Conversion Type")
category = st.selectbox("Category", list(unit_categories.keys()))

st.subheader("Enter Conversion Details")
col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox("From Unit", unit_categories[category])
with col2:
    to_unit = st.selectbox("To Unit", unit_categories[category])



value = st.number_input("Enter Value:", format="%.6f", step=0.1)


# **Temperature Conversion Logic**
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    elif from_unit == "celsius" and to_unit == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return (value - 32) * 5/9
    elif from_unit == "celsius" and to_unit == "kelvin":
        return value + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        return value - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return (value - 32) * 5/9 + 273.15
    elif to_unit == "fahrenheit" and from_unit == "kelvin":
        return (value - 273.15) * 9/5 + 32
    return None

# **Convert Button**
if st.button("Convert 🔄"):
    try:
        if category == "🌡 Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            result = (value * ureg(from_unit)).to(to_unit).magnitude  # Extract magnitude

        st.success(f"✅ {value} {from_unit} = {round(result, 4)} {to_unit}")

        # **Store Result in History**
        st.session_state.history.append(f"{value} {from_unit} → {round(result, 4)} {to_unit}")
    
    except Exception as e:
        st.error(f"⚠ Conversion error: {e}")


st.subheader("📜 Conversion History")

if st.session_state.history:
    for entry in st.session_state.history[::-1]:
        st.markdown(f"✅ {entry}")
    if st.button("Clear History ❌"):
        st.session_state.history = []

