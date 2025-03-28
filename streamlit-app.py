import streamlit as st
import pandas as pd
from src.gdpr_manager import GDPRComplianceManager
from src.data_protection import EncryptoDataProtectionEngine

def main():
    st.title("GDPR Compliance Management Dashboard")
    
    # Initialize GDPR Compliance Manager
    gdpr_manager = GDPRComplianceManager()
    
    # Sidebar navigation
    menu = ["Data Access Request", "Consent Management", "Right to Be Forgotten"]
    choice = st.sidebar.selectbox("Select Operation", menu)
    
    if choice == "Data Access Request":
        st.subheader("Data Access Request")
        user_id = st.text_input("Enter User ID")
        
        if st.button("Process Data Access Request"):
            result = gdpr_manager.process_data_access_request(user_id)
            
            if result['status'] == 'success':
                st.success("Data Access Request Processed Successfully")
                st.json(result['data'])
            else:
                st.error(result['message'])
    
    elif choice == "Consent Management":
        st.subheader("Consent Management")
        user_id = st.text_input("Enter User ID")
        consent_type = st.selectbox("Consent Type", 
            ["data_processing", "marketing", "analytics"]
        )
        
        if st.button("Update Consent"):
            result = gdpr_manager.manage_user_consent(user_id, consent_type)
            
            if result:
                st.success("Consent Updated Successfully")
            else:
                st.error("Consent Update Failed")
    
    elif choice == "Right to Be Forgotten":
        st.subheader("Right to Be Forgotten")
        user_id = st.text_input("Enter User ID")
        
        if st.button("Erase User Data"):
            # Use a database engine for actual implementation
            database_url = "sqlite:///gdpr_compliance.db"
            data_protection_engine = EncryptoDataProtectionEngine(database_url)
            
            result = data_protection_engine.right_to_be_forgotten(user_id)
            
            if result['status'] == 'success':
                st.success("User Data Successfully Erased")
            else:
                st.error("Data Erasure Failed")

if __name__ == "__main__":
    main()
