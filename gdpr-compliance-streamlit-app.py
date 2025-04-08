import streamlit as st
import pandas as pd
import hashlib
import uuid
from datetime import datetime, timedelta
import logging
import os
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)

# Core GDPR and Data Protection Classes
class DataProtectionPolicy:
    def __init__(self):
        pass
    
    def get_policy_details(self):
        return {
            "last_updated": "April 8, 2025",
            "retention_period": "2 years",
            "data_access_process": "Users can request their data through the Data Access tab",
            "erasure_process": "Users can request data deletion through the Right to be Forgotten tab"
        }

class ConsentManager:
    def check_consent(self, user_id):
        # In a real application, this would query a database
        # Here we'll use session state to simulate persistence
        if 'consents' not in st.session_state:
            st.session_state.consents = {}
        
        return st.session_state.consents.get(user_id, False)

    def update_consent(self, user_id, consent_type, status, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()
            
        if 'consents' not in st.session_state:
            st.session_state.consents = {}
            
        if user_id not in st.session_state.consents:
            st.session_state.consents[user_id] = {}
            
        st.session_state.consents[user_id] = {
            'status': status,
            'type': consent_type,
            'timestamp': timestamp
        }
        
        return True

class DataSubjectRightsHandler:
    def retrieve_personal_data(self, user_id):
        # In a real app, this would fetch from a database
        # Here we'll simulate with session state
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
            
        # Return stored data or default data if not found
        if user_id in st.session_state.user_data:
            return st.session_state.user_data[user_id]
        else:
            return {
                "user_id": user_id,
                "email": f"{user_id}@example.com",
                "phone": "1234567890",
                "address": "123 Privacy Street",
                "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def store_personal_data(self, user_id, data):
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
            
        st.session_state.user_data[user_id] = data
        return True

class GDPRComplianceManager:
    def __init__(self):
        self.data_protection_policy = DataProtectionPolicy()
        self.consent_manager = ConsentManager()
        self.data_subject_rights = DataSubjectRightsHandler()

    def process_data_access_request(self, user_id: str) -> Dict[str, Any]:
        try:
            user_data = self.data_subject_rights.retrieve_personal_data(user_id)
            anonymized_data = self.anonymize_personal_data(user_data)

            return {
                'status': 'success',
                'data': anonymized_data,
                'timestamp': datetime.utcnow()
            }
        except Exception as e:
            logging.error(f"Data Access Request Error: {e}")
            return {
                'status': 'error',
                'message': 'Unable to process data access request'
            }

    def anonymize_personal_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        anonymized = data.copy()

        if 'email' in anonymized:
            anonymized['email'] = hashlib.sha256(anonymized['email'].encode()).hexdigest()

        if 'phone' in anonymized:
            anonymized['phone'] = '*' * len(anonymized['phone'])
            
        if 'address' in anonymized:
            anonymized['address'] = '*** REDACTED ***'

        return anonymized

    def manage_user_consent(self, user_id: str, consent_type: str, status: bool) -> bool:
        try:
            return self.consent_manager.update_consent(
                user_id,
                consent_type,
                status,
                datetime.utcnow()
            )
        except Exception as e:
            logging.error(f"Consent Management Error: {e}")
            return False

class DataProcessingLog:
    def __init__(self):
        # Initialize an empty list if not already in session state
        if 'data_processing_logs' not in st.session_state:
            st.session_state.data_processing_logs = []
    
    def log_activity(self, user_id, activity_type, data_processed, consent_given=False):
        log_entry = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'activity_type': activity_type,
            'timestamp': datetime.utcnow(),
            'data_processed': data_processed,
            'is_consent_given': consent_given,
            'retention_period': datetime.utcnow() + timedelta(days=730)
        }
        
        st.session_state.data_processing_logs.append(log_entry)
        return log_entry
    
    def get_logs(self, user_id=None):
        if user_id:
            return [log for log in st.session_state.data_processing_logs if log['user_id'] == user_id]
        return st.session_state.data_processing_logs
    
    def delete_logs(self, user_id):
        if 'data_processing_logs' in st.session_state:
            st.session_state.data_processing_logs = [
                log for log in st.session_state.data_processing_logs 
                if log['user_id'] != user_id
            ]
        return True

class DataminimizationEngine:
    def __init__(self):
        self.allowed_purposes = [
            'authentication',
            'transaction_processing',
            'fraud_prevention',
            'customer_support'
        ]

    def validate_data_processing(self, purpose: str, data: Dict[str, Any]) -> bool:
        if purpose not in self.allowed_purposes:
            return False

        minimized_data = self.minimize_data(purpose, data)
        return True

    def minimize_data(self, purpose: str, data: Dict[str, Any]) -> Dict[str, Any]:
        minimization_rules = {
            'authentication': ['username', 'email'],
            'transaction_processing': ['user_id', 'transaction_details'],
            'fraud_prevention': ['user_id', 'transaction_history'],
            'customer_support': ['user_id', 'contact_information']
        }

        allowed_fields = minimization_rules.get(purpose, [])
        return {k: v for k, v in data.items() if k in allowed_fields}

class EncryptoDataProtectionEngine:
    def __init__(self):
        self.gdpr_manager = GDPRComplianceManager()
        self.data_processing_log = DataProcessingLog()
        self.data_minimization = DataminimizationEngine()

    def log_data_processing_activity(self, user_id, activity_type, data_processed):
        consent_given = self.gdpr_manager.consent_manager.check_consent(user_id)
        return self.data_processing_log.log_activity(
            user_id=user_id,
            activity_type=activity_type,
            data_processed=data_processed,
            consent_given=consent_given
        )

    def right_to_be_forgotten(self, user_id):
        try:
            # Delete processing logs
            self.data_processing_log.delete_logs(user_id)
            
            # Remove consent records
            if 'consents' in st.session_state and user_id in st.session_state.consents:
                del st.session_state.consents[user_id]
                
            # Remove user data
            if 'user_data' in st.session_state and user_id in st.session_state.user_data:
                del st.session_state.user_data[user_id]

            return {
                'status': 'success',
                'message': 'User data successfully erased'
            }
        except Exception as e:
            logging.error(f"Right to be Forgotten Error: {e}")
            return {
                'status': 'error',
                'message': f'Unable to erase user data: {str(e)}'
            }

# Streamlit UI Functions
def render_home_page():
    st.title("GDPR Compliance Management System")
    
    st.markdown("""
    ### Welcome to the Data Protection and GDPR Compliance Portal
    
    This application helps organizations manage data protection responsibilities and comply with GDPR regulations.
    
    #### Features:
    - **User Consent Management**: Track and manage user consent for data processing
    - **Data Subject Rights**: Process data access and erasure requests
    - **Data Minimization**: Ensure only necessary data is processed
    - **Activity Logging**: Maintain records of data processing activities
    
    Navigate through the sidebar to access different features.
    """)
    
    st.info("This is a demonstration application. In a production environment, additional security measures and proper database integration would be required.")

def render_consent_management(data_protection_engine):
    st.title("Consent Management")
    
    with st.form("consent_form"):
        user_id = st.text_input("User ID", key="consent_user_id")
        consent_type = st.selectbox(
            "Consent Type", 
            ["data_processing", "marketing", "analytics", "third_party_sharing"]
        )
        consent_status = st.checkbox("I give consent for the selected purpose")
        
        submit_button = st.form_submit_button("Update Consent")
        
    if submit_button and user_id:
        result = data_protection_engine.gdpr_manager.manage_user_consent(
            user_id, 
            consent_type,
            consent_status
        )
        
        if result:
            st.success(f"Consent {'given' if consent_status else 'withdrawn'} successfully!")
            
            # Log the consent activity
            data_protection_engine.log_data_processing_activity(
                user_id=user_id,
                activity_type=f"consent_{consent_type}",
                data_processed={"consent_type": consent_type, "status": consent_status}
            )
        else:
            st.error("Failed to update consent. Please try again.")
    
    st.subheader("Check Existing Consent")
    
    with st.form("check_consent_form"):
        check_user_id = st.text_input("User ID", key="check_consent_user_id")
        check_button = st.form_submit_button("Check Consent Status")
        
    if check_button and check_user_id:
        consent_status = data_protection_engine.gdpr_manager.consent_manager.check_consent(check_user_id)
        
        if 'consents' in st.session_state and check_user_id in st.session_state.consents:
            consent_data = st.session_state.consents[check_user_id]
            st.info(f"Consent Status: {consent_data['status']}")
            st.info(f"Consent Type: {consent_data['type']}")
            st.info(f"Last Updated: {consent_data['timestamp']}")
        else:
            st.warning("No consent records found for this user.")

def render_data_subject_rights(data_protection_engine):
    st.title("Data Subject Rights")
    
    tabs = st.tabs(["Data Access Request", "Right to be Forgotten"])
    
    with tabs[0]:
        st.subheader("Request Data Access")
        
        with st.form("data_access_form"):
            user_id = st.text_input("User ID", key="access_user_id")
            access_button = st.form_submit_button("Request My Data")
            
        if access_button and user_id:
            result = data_protection_engine.gdpr_manager.process_data_access_request(user_id)
            
            if result['status'] == 'success':
                st.success("Data access request processed successfully")
                st.json(result['data'])
                
                # Log the data access activity
                data_protection_engine.log_data_processing_activity(
                    user_id=user_id,
                    activity_type="data_access_request",
                    data_processed={"request_time": datetime.utcnow().isoformat()}
                )
            else:
                st.error(f"Error processing request: {result.get('message', 'Unknown error')}")
    
    with tabs[1]:
        st.subheader("Request Data Erasure")
        
        with st.form("erasure_form"):
            user_id = st.text_input("User ID", key="erasure_user_id")
            confirmation = st.checkbox("I understand this will permanently delete all my data")
            erasure_button = st.form_submit_button("Delete My Data")
            
        if erasure_button:
            if not user_id:
                st.error("Please enter a User ID")
            elif not confirmation:
                st.error("Please confirm that you understand the implications of this action")
            else:
                result = data_protection_engine.right_to_be_forgotten(user_id)
                
                if result['status'] == 'success':
                    st.success("Your data has been successfully deleted")
                else:
                    st.error(f"Error processing erasure request: {result.get('message', 'Unknown error')}")

def render_data_processing_logs(data_protection_engine):
    st.title("Data Processing Activities")
    
    # Filter options
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        filter_user = st.text_input("Filter by User ID (leave empty for all)", "")
    
    with filter_col2:
        # Get unique activity types
        activity_types = []
        if 'data_processing_logs' in st.session_state:
            activity_types = list(set(log['activity_type'] for log in st.session_state.data_processing_logs))
        
        filter_activity = st.selectbox("Filter by Activity Type", ["All"] + activity_types)
    
    # Get logs with filters applied
    logs = data_protection_engine.data_processing_log.get_logs(
        user_id=filter_user if filter_user else None
    )
    
    # Apply activity type filter
    if filter_activity != "All":
        logs = [log for log in logs if log['activity_type'] == filter_activity]
    
    # Convert to DataFrame for display
    if logs:
        df = pd.DataFrame(logs)
        
        # Format timestamp
        df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        df['retention_period'] = df['retention_period'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Select columns to display
        display_cols = ['id', 'user_id', 'activity_type', 'timestamp', 'is_consent_given', 'retention_period']
        
        st.dataframe(df[display_cols])
        
        # Allow log export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Logs as CSV",
            csv,
            "data_processing_logs.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No processing logs found. Activity logs will appear here when data is processed.")
    
    # Demo data generation
    st.subheader("Generate Demo Data")
    
    with st.form("demo_data_form"):
        demo_user_id = st.text_input("User ID for Demo Data", "user123")
        demo_activity = st.selectbox(
            "Activity Type", 
            ["authentication", "transaction_processing", "data_access_request", "consent_update"]
        )
        
        demo_button = st.form_submit_button("Generate Demo Log Entry")
    
    if demo_button:
        sample_data = {
            "authentication": {"username": "jdoe", "login_time": datetime.utcnow().isoformat()},
            "transaction_processing": {"amount": "$250.00", "item_count": 3, "transaction_id": str(uuid.uuid4())},
            "data_access_request": {"request_time": datetime.utcnow().isoformat()},
            "consent_update": {"consent_type": "marketing", "status": True}
        }
        
        log_entry = data_protection_engine.log_data_processing_activity(
            user_id=demo_user_id,
            activity_type=demo_activity,
            data_processed=sample_data.get(demo_activity, {})
        )
        
        st.success(f"Demo log entry created with ID: {log_entry['id']}")
        st.experimental_rerun()

def render_data_minimization(data_protection_engine):
    st.title("Data Minimization")
    
    st.markdown("""
    Data minimization is a core principle of GDPR that requires organizations to collect 
    and process only the personal data that is necessary for a specific purpose.
    """)
    
    with st.form("minimization_form"):
        user_id = st.text_input("User ID", "user123")
        purpose = st.selectbox(
            "Processing Purpose", 
            data_protection_engine.data_minimization.allowed_purposes
        )
        
        # Dynamic form fields based on purpose
        data_fields = {}
        
        if purpose == "authentication":
            data_fields["username"] = st.text_input("Username")
            data_fields["email"] = st.text_input("Email")
            data_fields["phone"] = st.text_input("Phone Number (not required)")
            data_fields["address"] = st.text_input("Address (not required)")
            
        elif purpose == "transaction_processing":
            data_fields["transaction_details"] = st.text_area("Transaction Details")
            data_fields["shipping_address"] = st.text_input("Shipping Address (not required)")
            
        elif purpose == "fraud_prevention":
            data_fields["transaction_history"] = st.text_area("Transaction History")
            data_fields["ip_address"] = st.text_input("IP Address (not required)")
            
        elif purpose == "customer_support":
            data_fields["contact_information"] = st.text_input("Contact Information")
            data_fields["issue_description"] = st.text_area("Issue Description (not required)")
        
        submit_button = st.form_submit_button("Process Data")
    
    if submit_button:
        # Check if any field has data
        if any(data_fields.values()):
            # Validate and minimize data
            is_valid = data_protection_engine.data_minimization.validate_data_processing(purpose, data_fields)
            minimized_data = data_protection_engine.data_minimization.minimize_data(purpose, data_fields)
            
            if is_valid:
                st.success("Data processing validated successfully!")
                
                # Log the activity
                data_protection_engine.log_data_processing_activity(
                    user_id=user_id,
                    activity_type=purpose,
                    data_processed=minimized_data
                )
                
                # Show minimized data
                st.subheader("Minimized Data (Only Required Fields)")
                st.json(minimized_data)
                
                # Show fields that were excluded
                excluded_fields = {k: v for k, v in data_fields.items() if k not in minimized_data and v}
                if excluded_fields:
                    st.subheader("Excluded Fields (Not Required for Purpose)")
                    st.json(excluded_fields)
            else:
                st.error("Invalid processing purpose or data fields!")
        else:
            st.warning("Please enter data in at least one field")

def render_policy_details(data_protection_engine):
    st.title("Data Protection Policy")
    
    policy = data_protection_engine.gdpr_manager.data_protection_policy.get_policy_details()
    
    st.markdown("""
    ### Company Data Protection Policy
    
    This policy outlines how we collect, process, and protect personal data in compliance with GDPR
    and other applicable data protection regulations.
    """)
    
    st.subheader("Key Policy Points")
    
    for key, value in policy.items():
        st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")
    
    st.subheader("Data Subject Rights")
    
    st.markdown("""
    Under the GDPR, individuals have the following rights:
    
    1. **Right to be informed** about how their data is collected and used
    2. **Right of access** to their personal data
    3. **Right to rectification** of inaccurate personal data
    4. **Right to erasure** (or 'right to be forgotten')
    5. **Right to restrict processing** of their personal data
    6. **Right to data portability** to obtain and reuse their data
    7. **Right to object** to processing of their data
    8. **Rights related to automated decision making and profiling**
    
    These rights can be exercised using the tools provided in the Data Subject Rights section of this application.
    """)

# Main Streamlit Application
def main():
    st.set_page_config(
        page_title="GDPR Compliance Manager",
        page_icon="🔒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize the data protection engine
    data_protection_engine = EncryptoDataProtectionEngine()
    
    # Sidebar navigation
    st.sidebar.title("GDPR Compliance Suite")
    
    pages = {
        "Home": render_home_page,
        "Consent Management": render_consent_management,
        "Data Subject Rights": render_data_subject_rights,
        "Data Processing Logs": render_data_processing_logs,
        "Data Minimization": render_data_minimization,
        "Policy Details": render_policy_details
    }
    
    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
    
    # Display current user info in sidebar
    st.sidebar.markdown("---")
    
    with st.sidebar.expander("Quick Stats"):
        log_count = len(st.session_state.get('data_processing_logs', []))
        consent_count = len(st.session_state.get('consents', {}))
        user_count = len(st.session_state.get('user_data', {}))
        
        st.markdown(f"**Activity Logs**: {log_count}")
        st.markdown(f"**Consent Records**: {consent_count}")
        st.markdown(f"**Registered Users**: {user_count}")
    
    # Render the selected page
    if selected_page == "Home":
        pages[selected_page]()
    else:
        pages[selected_page](data_protection_engine)

if __name__ == "__main__":
    main()
