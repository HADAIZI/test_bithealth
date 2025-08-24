import streamlit as st
import requests
import json

st.set_page_config(page_title="Hospital Triage System", page_icon="🏥")

st.title("🏥 Hospital Triage System")
st.markdown("Get department recommendations based on patient symptoms")

# Create the form
with st.form("patient_form"):
    st.subheader("Patient Information")
    
    # Gender input
    gender = st.selectbox(
        "Gender",
        ["male", "female", "other"]
    )
    
    # Age input
    age = st.number_input(
        "Age", 
        min_value=0, 
        max_value=120, 
        value=30,
        help="Enter patient age in years"
    )
    
    # Symptoms input
    symptoms_text = st.text_area(
        "Symptoms", 
        placeholder="Enter symptoms separated by commas (e.g., pusing, mual, sulit berjalan)",
        help="Separate multiple symptoms with commas"
    )
    
    # Submit button
    submitted = st.form_submit_button("Get Recommendation", type="primary")

# Process form submission
if submitted:
    if not symptoms_text.strip():
        st.error("Please enter at least one symptom!")
    else:
        # Parse symptoms
        symptoms = [symptom.strip() for symptom in symptoms_text.split(",") if symptom.strip()]
        
        # Prepare request data
        patient_data = {
            "gender": gender,
            "age": age,
            "symptoms": symptoms
        }
        
        # Show loading spinner
        with st.spinner("Getting recommendation..."):
            try:
                # Make API call
                response = requests.post(
                    "http://localhost:8000/recommend",
                    json=patient_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    recommended_dept = result.get("recommended_department", "Unknown")
                    
                    # Show success result
                    st.success(f"**Recommended Department:** {recommended_dept}")
                    
                    # Show patient info summary
                    st.subheader("Patient Summary")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Gender:** {gender}")
                        st.write(f"**Age:** {age} years")
                    with col2:
                        st.write(f"**Symptoms:** {', '.join(symptoms)}")
                        st.write(f"**Department:** {recommended_dept}")
                    
                    # Download JSON button
                    complete_response = {
                        "patient_info": patient_data,
                        "recommendation": result
                    }
                    
                    json_str = json.dumps(complete_response, indent=2)
                    
                    st.download_button(
                        label="📥 Download JSON Response",
                        data=json_str,
                        file_name=f"triage_recommendation_{age}_{gender}.json",
                        mime="application/json"
                    )
                    
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                st.error("Could not connect to the API. Make sure your FastAPI server is running on localhost:8000")
                st.code(str(e))

# Instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Select patient gender
2. Enter patient age
3. Enter symptoms separated by commas
4. Click 'Get Recommendation'
5. Download the JSON response if needed

**Make sure your FastAPI server is running:**
```bash
python main.py
```
""")

st.sidebar.header("Example Symptoms")
st.sidebar.markdown("""
- pusing, mual, sulit berjalan
- demam, batuk, sesak napas
- sakit perut, mual
- susah tidur
""")