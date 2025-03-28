import pytest
from src.gdpr_manager import GDPRComplianceManager, ConsentManager

def test_consent_management():
    manager = ConsentManager()
    user_id = "test_user"
    consent_type = "data_processing"
    
    # Test initial consent state
    assert not manager.check_consent(user_id, consent_type)
    
    # Update consent
    result = manager.update_consent(user_id, consent_type, datetime.utcnow())
    assert result
    
    # Check updated consent
    assert manager.check_consent(user_id, consent_type)

def test_data_anonymization():
    gdpr_manager = GDPRComplianceManager()
    test_data = {
        "user_id": "user123",
        "email": "test@example.com",
        "phone": "1234567890",
        "address": "123 Test Street"
    }
    
    anonymized_data = gdpr_manager.anonymize_personal_data(test_data)
    
    # Check email is hashed
    assert anonymized_data['email'] != test_data['email']
    
    # Check phone number is partially masked
    assert anonymized_data['phone'][-4:] == test_data['phone'][-4:]
    assert anonymized_data['phone'][:-4] == '*' * (len(test_data['phone']) - 4)
    
    # Check address is minimized
    assert anonymized_data['address'].endswith('[REDACTED]')
