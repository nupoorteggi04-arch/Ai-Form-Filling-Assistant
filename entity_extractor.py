import re
from typing import Dict, Any, Optional
from datetime import datetime

def extract_entities(ocr_text: str) -> Dict[str, Any]:
    """
    Extract structured entities from OCR text.
    Returns a dictionary with extracted fields.
    """
    text = ocr_text.upper()  # Normalize to uppercase for pattern matching
    
    entities = {
        "name": None,
        "dob": None,
        "date_of_birth": None,
        "gender": None,
        "father_name": None,
        "mother_name": None,
        "address": {
            "line1": None,
            "line2": None,
            "city": None,
            "district": None,
            "state": None,
            "pincode": None,
            "full_address": None
        },
        "aadhaar_number": None,
        "pan_number": None,
        "voter_id": None,
        "mobile": None,
        "email": None,
    }
    
    # Extract Name
    # Patterns include English and transliterated versions (e.g., NAAM for नाम in Hindi)
    name_patterns = [
        r'NAME[:\s-]+([A-Z][A-Z\s\.]+)',
        r'NAAM[:\s-]+([A-Z][A-Z\s\.]+)',  # Hindi transliteration
        r'NAME\s*[:\-]?\s*([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|PAN|AADHAAR|$)',
        r'FULL\s*NAME[:\s-]+([A-Z][A-Z\s\.]+)',
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Clean up common OCR errors
            name = re.sub(r'\s+', ' ', name)
            entities["name"] = name.title()
            break
    
    # Extract Date of Birth (DOB)
    # Patterns include English and transliterated versions
    dob_patterns = [
        r'DOB[:\s-]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'JANM\s*TITHI[:\s-]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Hindi transliteration
        r'DATE\s*OF\s*BIRTH[:\s-]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'BIRTH\s*DATE[:\s-]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Generic date pattern
    ]
    for pattern in dob_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            dob_str = match.group(1).strip()
            # Normalize date format
            try:
                # Try to parse and format date
                if '/' in dob_str:
                    parts = dob_str.split('/')
                elif '-' in dob_str:
                    parts = dob_str.split('-')
                else:
                    continue
                
                if len(parts) == 3:
                    day, month, year = parts
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    # Format as YYYY-MM-DD
                    entities["dob"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    entities["date_of_birth"] = entities["dob"]
            except:
                entities["dob"] = dob_str
                entities["date_of_birth"] = dob_str
            break
    
    # Extract PAN Number (format: AAAAA9999A)
    pan_patterns = [
        r'PAN[:\s-]+([A-Z]{5}\d{4}[A-Z])',
        r'PAN\s*NO[:\s-]+([A-Z]{5}\d{4}[A-Z])',
        r'([A-Z]{5}\d{4}[A-Z])',  # Generic PAN pattern
    ]
    for pattern in pan_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            pan = match.group(1).strip().upper()
            entities["pan_number"] = pan
            break
    
    # Extract Aadhaar Number (12 digits, may have spaces, dashes, or be continuous)
    # Handle various formats: XXXX XXXX XXXX, XXXX-XXXX-XXXX, XXXXXXXXXXXX
    aadhaar_patterns = [
        r'AADHAAR\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{4}[\s-]?\d{4}[\s-]?\d{4})',
        r'AADHAR\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{4}[\s-]?\d{4}[\s-]?\d{4})',
        r'UID\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{4}[\s-]?\d{4}[\s-]?\d{4})',
        r'(\d{4}[\s-]+\d{4}[\s-]+\d{4})',  # Pattern with spaces or dashes
        r'(\d{4}\s\d{4}\s\d{4})',  # Pattern with spaces (explicit)
        r'(\d{4}-\d{4}-\d{4})',  # Pattern with dashes
        r'(\d{12})',  # 12 consecutive digits (no spaces)
    ]
    
    for pattern in aadhaar_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            aadhaar = match.group(1).strip()
            # Remove all spaces, dashes, and other separators
            aadhaar = re.sub(r'[\s\-]', '', aadhaar)
            # Validate: must be exactly 12 digits
            if len(aadhaar) == 12 and aadhaar.isdigit():
                entities["aadhaar_number"] = aadhaar
                break
        if entities["aadhaar_number"]:
            break
    
    # Extract City
    # Patterns include English and transliterated versions
    city_patterns = [
        r'CITY[:\s-]+([A-Z][A-Z\s]+?)(?:\n|$|PAN|AADHAAR|DOB)',
        r'SHAHAR[:\s-]+([A-Z][A-Z\s]+?)(?:\n|$|PAN|AADHAAR|DOB)',  # Hindi transliteration
        r'CITY\s*[:\-]?\s*([A-Z][A-Z\s]+)',
    ]
    for pattern in city_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            entities["address"]["city"] = city.title()
            break
    
    # Extract Mobile Number (10 digits)
    # Handle various formats: +91 XXXXXXXXXX, 91 XXXXXXXXXX, 0XXXXXXXXXX, XXXXXXXXXX
    mobile_patterns = [
        r'MOBILE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\+?91[\s-]?\d{10})',
        r'PHONE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\+?91[\s-]?\d{10})',
        r'CONTACT\s*(?:NO|NUMBER|NUM)?[:\s-]*(\+?91[\s-]?\d{10})',
        r'MOBILE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{10})',
        r'PHONE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{10})',
        r'CONTACT\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{10})',
        r'(\+91[\s-]?\d{10})',  # +91 prefix
        r'(91[\s-]?\d{10})',  # 91 prefix without +
        r'(0\d{10})',  # 0 prefix (11 digits total, starts with 0)
        r'(\d{10})',  # Generic 10-digit pattern (last resort)
    ]
    
    for pattern in mobile_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            mobile = match.group(1).strip()
            # Remove spaces, dashes, and country code
            mobile = re.sub(r'[\s\-]', '', mobile)
            mobile = re.sub(r'^\+?91', '', mobile)  # Remove +91 or 91 prefix
            
            # Handle 0-prefixed numbers (11 digits starting with 0)
            if len(mobile) == 11 and mobile.startswith('0'):
                mobile = mobile[1:]  # Remove leading 0
            
            # Validate: must be exactly 10 digits and start with 6-9 (Indian mobile number format)
            if len(mobile) == 10 and mobile.isdigit() and mobile[0] in '6789':
                entities["mobile"] = mobile
                break
        if entities["mobile"]:
            break
    
    # Extract Email
    email_pattern = r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})'
    match = re.search(email_pattern, text, re.IGNORECASE)
    if match:
        entities["email"] = match.group(1).lower()
    
    # Extract Gender
    gender_patterns = [
        r'GENDER[:\s-]+(MALE|FEMALE|OTHER|M|F)',
        r'SEX[:\s-]+(MALE|FEMALE|OTHER|M|F)',
    ]
    for pattern in gender_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            gender = match.group(1).strip().upper()
            if gender in ['M', 'MALE']:
                entities["gender"] = "Male"
            elif gender in ['F', 'FEMALE']:
                entities["gender"] = "Female"
            else:
                entities["gender"] = gender.title()
            break
    
    # Extract Father's Name
    father_patterns = [
        r'FATHER[:\s-]+([A-Z][A-Z\s\.]+)',
        r'FATHER\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+)',
    ]
    for pattern in father_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            father_name = match.group(1).strip()
            entities["father_name"] = father_name.title()
            break
    
    # Extract Mother's Name
    mother_patterns = [
        r'MOTHER[:\s-]+([A-Z][A-Z\s\.]+)',
        r'MOTHER\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+)',
    ]
    for pattern in mother_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            mother_name = match.group(1).strip()
            entities["mother_name"] = mother_name.title()
            break
    
    # Extract Pincode (6 digits)
    # Handle various formats: PIN CODE, PINCODE, POSTAL CODE, or standalone 6-digit number
    pincode_patterns = [
        r'PIN\s*(?:CODE|NO|NUMBER)?[:\s-]*(\d{6})',
        r'PINCODE[:\s-]*(\d{6})',
        r'POSTAL\s*(?:CODE|NO|NUMBER)?[:\s-]*(\d{6})',
        r'ZIP\s*(?:CODE)?[:\s-]*(\d{6})',
        r'(\d{6})',  # Standalone 6-digit number (last resort, might match other numbers)
    ]
    
    for pattern in pincode_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            pincode = match.group(1).strip()
            # Validate: must be exactly 6 digits
            if len(pincode) == 6 and pincode.isdigit():
                # Additional validation: Indian pincodes start with 1-9 (not 0)
                if pincode[0] in '123456789':
                    entities["address"]["pincode"] = pincode
                    break
        if entities["address"]["pincode"]:
            break
    
    # Extract State
    state_pattern = r'STATE[:\s-]+([A-Z][A-Z\s]+?)(?:\n|$|PIN|CITY)'
    match = re.search(state_pattern, text, re.IGNORECASE)
    if match:
        entities["address"]["state"] = match.group(1).strip().title()
    
    return entities





