import streamlit as st

def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            font-family: Arial, sans-serif;
        }}
        .title-text {{
            text-align: center;
            color: white;
            font-size: 36px;
            font-weight: bold;
        }}
        .result-box {{
            padding: 15px;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            font-size: 20px;
            text-align: center;
            font-weight: bold;
            color: #333;
            margin-top: 20px;
        }}
        .label-text {{
            font-size: 18px;
            font-weight: bold;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def convert_units(value, from_unit, to_unit, conversion_dict):
    if from_unit in conversion_dict and to_unit in conversion_dict:
        return value * conversion_dict[to_unit] / conversion_dict[from_unit]
    return None

def main():
    add_bg_from_url()
    st.markdown("<div class='title-text'>🌍 Unit Converter Project Made By Abdullah Kashif 🌐</div>", unsafe_allow_html=True)
    
    categories = {
        "Length": {"Meter": 1, "Kilometer": 1000, "Centimeter": 0.01, "Millimeter": 0.001, "Mile": 1609.34, "Yard": 0.9144, "Foot": 0.3048, "Inch": 0.0254},
        "Weight": {"Kilogram": 1, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495},
        "Temperature": {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"}
    }
    
    category = st.selectbox("**Select Category**", list(categories.keys()))
    col1, col2 = st.columns(2)
    from_unit = col1.selectbox("**From**", list(categories[category].keys()))
    to_unit = col2.selectbox("**To**", list(categories[category].keys()))
    value = st.number_input("**Enter Value**", min_value=0.0, format="%.4f")
    
    if st.button("Convert ✅"):
        if category == "Temperature":
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                result = value + 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (value - 32) * 5/9
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                result = value - 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                result = value
        else:
            result = convert_units(value, from_unit, to_unit, categories[category])
        
        st.markdown(f"<div class='result-box'>{value} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()