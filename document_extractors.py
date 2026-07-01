import re
from typing import Dict, Any, Optional, Literal
from entity_extractor import extract_entities


def detect_document_type(ocr_text: str) -> Optional[Literal["aadhar", "pan", "voter_id", "unknown"]]:
    """
    Detect the type of document from OCR text.
    
    Returns:
        "aadhar", "pan", "voter_id", or "unknown"
    """
    text = ocr_text.upper()
    
    # Aadhar card indicators
    aadhar_indicators = [
        r'GOVERNMENT\s+OF\s+INDIA',
        r'आधार',
        r'AADHAAR',
        r'UIDAI',
        r'ENROLMENT\s+NO',
        r'ENROLMENT\s+NUMBER',
        r'DOB[:\s-]+\d{2}[/-]\d{2}[/-]\d{4}',  # DOB near Aadhar number
    ]
    
    # PAN card indicators
    pan_indicators = [
        r'INCOME\s+TAX\s+DEPARTMENT',
        r'GOVT\.?\s+OF\s+INDIA',
        r'INCOME\s+TAX',
        r'Permanent\s+Account\s+Number',
        r'Permanent\s+Account\s+No',
        r'PAN',
    ]
    
    # Voter ID indicators
    voter_id_indicators = [
        r'ELECTION\s+COMMISSION\s+OF\s+INDIA',
        r'ELECTOR\'?S\s+PHOTO\s+IDENTITY\s+CARD',
        r'EPIC',
        r'VOTER\s+ID',
        r'ELECTION\s+CARD',
        r'ELECTORAL\s+ROLL',
    ]
    
    aadhar_score = sum(1 for pattern in aadhar_indicators if re.search(pattern, text, re.IGNORECASE))
    pan_score = sum(1 for pattern in pan_indicators if re.search(pattern, text, re.IGNORECASE))
    voter_score = sum(1 for pattern in voter_id_indicators if re.search(pattern, text, re.IGNORECASE))
    
    # Also check for document-specific number patterns
    if re.search(r'\d{4}\s?\d{4}\s?\d{4}', text) and aadhar_score > 0:
        aadhar_score += 2
    if re.search(r'[A-Z]{5}\d{4}[A-Z]', text) and pan_score > 0:
        pan_score += 2
    
    if aadhar_score > pan_score and aadhar_score > voter_score and aadhar_score > 0:
        return "aadhar"
    elif pan_score > voter_score and pan_score > 0:
        return "pan"
    elif voter_score > 0:
        return "voter_id"
    else:
        return "unknown"


def extract_aadhar_entities(ocr_text: str) -> Dict[str, Any]:
    """
    Extract entities specifically from Aadhar card.
    
    Aadhar card typically contains:
    - Name (in English and sometimes regional language)
    - Date of Birth (DOB)
    - Gender
    - Aadhar Number (12 digits)
    - Address
    - Father's/Husband's Name (sometimes)
    """
    text = ocr_text.upper()
    
    entities = {
        "name": None,
        "dob": None,
        "date_of_birth": None,
        "gender": None,
        "father_name": None,
        "husband_name": None,
        "aadhaar_number": None,
        "mobile": None,
        "address": {
            "line1": None,
            "line2": None,
            "city": None,
            "district": None,
            "state": None,
            "pincode": None,
            "full_address": None
        },
        "document_type": "aadhar"
    }
    
    # Extract Aadhar Number (12 digits, may be formatted as XXXX XXXX XXXX, XXXX-XXXX-XXXX, or continuous)
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
    
    # Extract Name - Aadhar cards usually have name prominently displayed
    # Look for name patterns that appear before DOB or other fields
    name_patterns = [
        # Pattern 1: NAME label followed by name
        r'NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|GENDER|MALE|FEMALE|YEAR|FATHER|HUSBAND|ADDRESS)',
        r'NAME\s*[:\-]?\s*([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|GENDER|MALE|FEMALE|YEAR|FATHER|HUSBAND|ADDRESS)',
        r'FULL\s*NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|GENDER|MALE|FEMALE|YEAR)',
        
        # Pattern 2: Name followed by DOB (common in Aadhar cards)
        r'([A-Z][A-Z\s\.]{3,40})(?:\n\s*DOB|\n\s*DATE|\n\s*YEAR|\n\s*GENDER|\n\s*MALE|\n\s*FEMALE)',
        r'([A-Z][A-Z\s\.]{3,40})\n\s*(\d{2}[/-]\d{2}[/-]\d{4})',  # Name on line before date
        
        # Pattern 3: Name after "GOVERNMENT OF INDIA" or "AADHAAR" header
        r'(?:GOVERNMENT\s+OF\s+INDIA|AADHAAR|AADHAR|UIDAI)\s+([A-Z][A-Z\s\.]{3,40})(?:\n|DOB|DATE|YEAR)',
        
        # Pattern 4: Name on its own line (between header and DOB)
        r'(?:GOVERNMENT|AADHAAR|AADHAR)\s+[^\n]+\n\s*([A-Z][A-Z\s\.]{3,40})\n\s*(?:DOB|DATE|YEAR|\d{2}[/-])',
        
        # Pattern 5: Name before gender or other fields
        r'([A-Z][A-Z\s\.]{3,40})(?:\s+(?:MALE|FEMALE|OTHER|M|F)\s|GENDER)',
        
        # Pattern 6: Name that's not a number, date, or common label
        r'^([A-Z][A-Z\s\.]{3,40})$',  # Standalone line with just name
        
        # Pattern 7: Name after photo area (common layout)
        r'(?:PHOTO|PHOTOGRAPH|IMAGE)\s+([A-Z][A-Z\s\.]{3,40})(?:\n|DOB|DATE)',
    ]
    
    # Try each pattern and validate the result
    for pattern in name_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            name = match.group(1).strip()
            # Clean up common OCR errors
            name = re.sub(r'\s+', ' ', name)
            name = re.sub(r'[^\w\s\.]', '', name)  # Remove special chars except dots
            
            # Additional validation: exclude common false positives
            false_positives = [
                'GOVERNMENT', 'INDIA', 'AADHAAR', 'AADHAR', 'UIDAI', 
                'ENROLMENT', 'NUMBER', 'DOB', 'DATE', 'BIRTH', 'GENDER',
                'MALE', 'FEMALE', 'FATHER', 'MOTHER', 'HUSBAND', 'ADDRESS',
                'PIN', 'PINCODE', 'POSTAL', 'CODE', 'STATE', 'CITY', 'DISTRICT'
            ]
            
            # Check if it's not a false positive and has reasonable length
            if (len(name) > 2 and len(name) < 50 and 
                not any(fp in name.upper() for fp in false_positives) and
                not name.isdigit() and  # Not just digits
                not re.match(r'^\d+[/-]\d+[/-]\d+', name)):  # Not a date
                entities["name"] = name.title()
                break
        if entities["name"]:
            break
    
    # Fallback: If no name found, try to find the longest capitalized word sequence
    # that appears before DOB and is not a common label
    if not entities["name"]:
        # Find DOB position
        dob_match = re.search(r'DOB[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})', text)
        if dob_match:
            # Get text before DOB
            text_before_dob = text[:dob_match.start()]
            # Find capitalized sequences
            name_candidates = re.findall(r'([A-Z][A-Z\s\.]{3,40})', text_before_dob)
            for candidate in reversed(name_candidates):  # Start from end (closest to DOB)
                candidate = candidate.strip()
                candidate = re.sub(r'\s+', ' ', candidate)
                candidate = re.sub(r'[^\w\s\.]', '', candidate)
                
                # Validate candidate
                if (len(candidate) > 2 and len(candidate) < 50 and
                    not any(fp in candidate.upper() for fp in false_positives) and
                    not candidate.isdigit()):
                    entities["name"] = candidate.title()
                    break
    
    # Extract Date of Birth - Aadhar format is usually DD/MM/YYYY or DD-MM-YYYY
    dob_patterns = [
        r'DOB[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})',
        r'DATE\s+OF\s+BIRTH[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})',
        r'YEAR\s+OF\s+BIRTH[:\s-]+(\d{4})',
        r'(\d{2}[/-]\d{2}[/-]\d{4})',  # Generic DD/MM/YYYY or DD-MM-YYYY
    ]
    
    for pattern in dob_patterns:
        match = re.search(pattern, text)
        if match:
            dob_str = match.group(1).strip()
            try:
                if '/' in dob_str:
                    parts = dob_str.split('/')
                elif '-' in dob_str:
                    parts = dob_str.split('-')
                else:
                    # Just year
                    if len(dob_str) == 4:
                        entities["dob"] = f"{dob_str}-01-01"
                        entities["date_of_birth"] = entities["dob"]
                    continue
                
                if len(parts) == 3:
                    day, month, year = parts
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    # Format as YYYY-MM-DD
                    entities["dob"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    entities["date_of_birth"] = entities["dob"]
                    break
            except:
                entities["dob"] = dob_str
                entities["date_of_birth"] = dob_str
                break
    
    # Extract Gender
    gender_patterns = [
        r'GENDER[:\s-]+(MALE|FEMALE|OTHER|M|F)',
        r'SEX[:\s-]+(MALE|FEMALE|OTHER|M|F)',
        r'(MALE|FEMALE|OTHER)\s*(?:\n|GENDER|$)',
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
    
    # Extract Father's/Husband's Name
    father_patterns = [
        r'FATHER[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|ADDRESS|$)',
        r'FATHER\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|ADDRESS|$)',
        r'GUARDIAN[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|ADDRESS|$)',
    ]
    
    for pattern in father_patterns:
        match = re.search(pattern, text)
        if match:
            father_name = match.group(1).strip()
            father_name = re.sub(r'\s+', ' ', father_name)
            entities["father_name"] = father_name.title()
            break
    
    husband_patterns = [
        r'HUSBAND[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|ADDRESS|$)',
        r'HUSBAND\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|ADDRESS|$)',
    ]
    
    for pattern in husband_patterns:
        match = re.search(pattern, text)
        if match:
            husband_name = match.group(1).strip()
            husband_name = re.sub(r'\s+', ' ', husband_name)
            entities["husband_name"] = husband_name.title()
            break
    
    # Extract Address - Aadhar cards have structured addresses
    # Look for address lines
    address_patterns = [
        r'ADDRESS[:\s-]+(.*?)(?:\n\s*\n|PIN|PINCODE|$)',
        r'ADDRESS[:\s-]+(.*?)(?:\d{6})',  # Address until pincode
    ]
    
    for pattern in address_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            address_text = match.group(1).strip()
            # Split address into lines
            address_lines = [line.strip() for line in address_text.split('\n') if line.strip()]
            if address_lines:
                entities["address"]["full_address"] = ', '.join(address_lines)
                if len(address_lines) > 0:
                    entities["address"]["line1"] = address_lines[0]
                if len(address_lines) > 1:
                    entities["address"]["line2"] = address_lines[1]
                if len(address_lines) > 2:
                    entities["address"]["city"] = address_lines[-2] if not re.search(r'\d{6}', address_lines[-2]) else address_lines[-3]
    
    # Extract Pincode (6 digits)
    pincode_patterns = [
        r'PIN\s*(?:CODE|NO|NUMBER)?[:\s-]*(\d{6})',
        r'PINCODE[:\s-]*(\d{6})',
        r'POSTAL\s*(?:CODE|NO|NUMBER)?[:\s-]*(\d{6})',
        r'ZIP\s*(?:CODE)?[:\s-]*(\d{6})',
        r'(\d{6})(?:\s*$|\s*\n)',  # Standalone 6-digit number at end of line
    ]
    
    for pattern in pincode_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            pincode = match.group(1).strip()
            # Validate: must be exactly 6 digits and start with 1-9 (Indian pincode format)
            if len(pincode) == 6 and pincode.isdigit() and pincode[0] in '123456789':
                entities["address"]["pincode"] = pincode
                break
        if entities["address"]["pincode"]:
            break
    
    # Extract Mobile Number (if present on Aadhar card)
    mobile_patterns = [
        r'MOBILE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\+?91[\s-]?\d{10})',
        r'PHONE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\+?91[\s-]?\d{10})',
        r'CONTACT\s*(?:NO|NUMBER|NUM)?[:\s-]*(\+?91[\s-]?\d{10})',
        r'MOBILE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{10})',
        r'PHONE\s*(?:NO|NUMBER|NUM)?[:\s-]*(\d{10})',
        r'(\+91[\s-]?\d{10})',
        r'(91[\s-]?\d{10})',
        r'(0\d{10})',  # 0 prefix
        r'(\d{10})',  # Generic 10-digit
    ]
    
    for pattern in mobile_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            mobile = match.group(1).strip()
            mobile = re.sub(r'[\s\-]', '', mobile)
            mobile = re.sub(r'^\+?91', '', mobile)
            
            if len(mobile) == 11 and mobile.startswith('0'):
                mobile = mobile[1:]
            
            if len(mobile) == 10 and mobile.isdigit() and mobile[0] in '6789':
                entities["mobile"] = mobile
                break
        if entities.get("mobile"):
            break
    
    # Extract State
    state_pattern = r'STATE[:\s-]+([A-Z][A-Z\s]+?)(?:\n|PIN|CITY|$)'
    match = re.search(state_pattern, text)
    if match:
        entities["address"]["state"] = match.group(1).strip().title()
    
    # Extract City/District
    city_pattern = r'(?:CITY|DISTRICT)[:\s-]+([A-Z][A-Z\s]+?)(?:\n|STATE|PIN|$)'
    match = re.search(city_pattern, text)
    if match:
        city = match.group(1).strip()
        entities["address"]["city"] = city.title()
    
    return entities


def extract_pan_entities(ocr_text: str) -> Dict[str, Any]:
    """
    Extract entities specifically from PAN card.
    
    PAN card typically contains:
    - Name
    - Father's Name
    - Date of Birth (DOB)
    - PAN Number (format: AAAAA9999A)
    """
    text = ocr_text.upper()
    
    entities = {
        "name": None,
        "father_name": None,
        "dob": None,
        "date_of_birth": None,
        "pan_number": None,
        "signature": None,
        "document_type": "pan"
    }
    
    # Extract PAN Number (format: AAAAA9999A - 5 letters, 4 digits, 1 letter)
    # Handle various formats and OCR errors
    pan_patterns = [
        r'PAN\s*(?:NO|NUMBER|NUM)?[:\s-]*([A-Z]{5}\d{4}[A-Z])',
        r'Permanent\s+Account\s+Number[:\s-]*([A-Z]{5}\d{4}[A-Z])',
        r'Permanent\s+Account\s+No[:\s-]*([A-Z]{5}\d{4}[A-Z])',
        r'([A-Z]{5}\d{4}[A-Z])',  # Generic PAN pattern (most common)
    ]
    
    for pattern in pan_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            pan = match.group(1).strip().upper()
            # Remove any spaces that might have been OCR'd incorrectly
            pan = re.sub(r'\s', '', pan)
            # Validate PAN format: 5 letters, 4 digits, 1 letter
            if len(pan) == 10 and pan[:5].isalpha() and pan[5:9].isdigit() and pan[9].isalpha():
                entities["pan_number"] = pan
                break
        if entities["pan_number"]:
            break
    
    # Extract Name - PAN cards have name prominently displayed
    # PAN cards typically have: INCOME TAX DEPARTMENT, GOVT OF INDIA, then NAME
    name_patterns = [
        # Pattern 1: NAME label followed by name
        r'NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|FATHER|MOTHER|DOB|DATE|YEAR|$)',
        r'NAME\s*[:\-]?\s*([A-Z][A-Z\s\.]+?)(?:\n|FATHER|MOTHER|DOB|DATE|YEAR|$)',
        
        # Pattern 2: Name after "INCOME TAX DEPARTMENT" or "GOVT OF INDIA"
        r'INCOME\s+TAX\s+DEPARTMENT\s+(?:GOVT\.?\s+OF\s+INDIA\s+)?([A-Z][A-Z\s\.]{3,40})(?:\n|FATHER|MOTHER|DOB)',
        r'GOVT\.?\s+OF\s+INDIA\s+([A-Z][A-Z\s\.]{3,40})(?:\n|FATHER|MOTHER|DOB)',
        
        # Pattern 3: Name on line before FATHER/MOTHER
        r'([A-Z][A-Z\s\.]{3,40})\n\s*(?:FATHER|MOTHER)',
        r'([A-Z][A-Z\s\.]{3,40})\s+(?:FATHER|MOTHER)',
        
        # Pattern 4: Name before DOB (common layout)
        r'([A-Z][A-Z\s\.]{3,40})\n\s*DOB',
        r'([A-Z][A-Z\s\.]{3,40})\s+DOB',
        
        # Pattern 5: Standalone capitalized name (not a label)
        r'^([A-Z][A-Z\s\.]{3,40})$',  # Full line with just name
    ]
    
    false_positives = [
        'INCOME', 'TAX', 'DEPARTMENT', 'GOVT', 'GOVERNMENT', 'INDIA', 
        'PAN', 'PERMANENT', 'ACCOUNT', 'NUMBER', 'NO', 'NAME',
        'FATHER', 'MOTHER', 'DOB', 'DATE', 'BIRTH', 'YEAR'
    ]
    
    for pattern in name_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            name = match.group(1).strip()
            name = re.sub(r'\s+', ' ', name)
            name = re.sub(r'[^\w\s\.]', '', name)
            
            # Validate: not a false positive, reasonable length, not just digits
            if (len(name) > 2 and len(name) < 50 and
                not any(fp in name.upper() for fp in false_positives) and
                not name.isdigit() and
                not re.match(r'^\d+[/-]\d+[/-]\d+', name)):  # Not a date
                entities["name"] = name.title()
                break
        if entities["name"]:
            break
    
    # Fallback: If no name found, look for text between header and FATHER/DOB
    if not entities["name"]:
        # Find position of FATHER or DOB
        father_match = re.search(r'FATHER', text)
        dob_match = re.search(r'DOB[:\s-]+', text)
        
        if father_match or dob_match:
            end_pos = father_match.start() if father_match else dob_match.start()
            # Get text before FATHER/DOB, after any headers
            text_before = text[:end_pos]
            # Remove common headers
            text_before = re.sub(r'INCOME\s+TAX\s+DEPARTMENT.*?', '', text_before, flags=re.IGNORECASE)
            text_before = re.sub(r'GOVT\.?\s+OF\s+INDIA.*?', '', text_before, flags=re.IGNORECASE)
            # Find capitalized sequences
            name_candidates = re.findall(r'([A-Z][A-Z\s\.]{3,40})', text_before)
            for candidate in reversed(name_candidates):  # Start from end (closest to FATHER/DOB)
                candidate = candidate.strip()
                candidate = re.sub(r'\s+', ' ', candidate)
                candidate = re.sub(r'[^\w\s\.]', '', candidate)
                
                if (len(candidate) > 2 and len(candidate) < 50 and
                    not any(fp in candidate.upper() for fp in false_positives) and
                    not candidate.isdigit()):
                    entities["name"] = candidate.title()
                    break
    
    # Extract Father's Name
    father_patterns = [
        r'FATHER\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|YEAR|$|PAN)',
        r'FATHER[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|YEAR|$|PAN)',
        r'FATHER\'?S?\s*NAME\s*[:\-]?\s*([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|YEAR|$|PAN)',
        # Name on line after FATHER label
        r'FATHER[:\s-]+\n\s*([A-Z][A-Z\s\.]{3,40})(?:\n|DOB|DATE|YEAR|$)',
    ]
    
    false_positives_father = [
        'FATHER', 'MOTHER', 'NAME', 'DOB', 'DATE', 'BIRTH', 'YEAR',
        'INCOME', 'TAX', 'DEPARTMENT', 'GOVT', 'INDIA', 'PAN'
    ]
    
    for pattern in father_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            father_name = match.group(1).strip()
            father_name = re.sub(r'\s+', ' ', father_name)
            father_name = re.sub(r'[^\w\s\.]', '', father_name)
            
            # Validate: not a false positive, reasonable length
            if (len(father_name) > 2 and len(father_name) < 50 and
                not any(fp in father_name.upper() for fp in false_positives_father) and
                not father_name.isdigit() and
                not re.match(r'^\d+[/-]\d+[/-]\d+', father_name)):  # Not a date
                entities["father_name"] = father_name.title()
                break
        if entities["father_name"]:
            break
    
    # Fallback: If name is already extracted and we have DOB, 
    # the text between name and DOB might be father's name
    if not entities["father_name"] and entities["name"]:
        name_pos = text.find(entities["name"].upper())
        dob_match = re.search(r'DOB[:\s-]+', text)
        if name_pos != -1 and dob_match:
            text_between = text[name_pos + len(entities["name"]):dob_match.start()]
            # Look for capitalized sequences
            father_candidates = re.findall(r'([A-Z][A-Z\s\.]{3,40})', text_between)
            for candidate in father_candidates:
                candidate = candidate.strip()
                candidate = re.sub(r'\s+', ' ', candidate)
                candidate = re.sub(r'[^\w\s\.]', '', candidate)
                
                if (len(candidate) > 2 and len(candidate) < 50 and
                    not any(fp in candidate.upper() for fp in false_positives_father) and
                    candidate.upper() != entities["name"].upper() and  # Not the same as name
                    not candidate.isdigit()):
                    entities["father_name"] = candidate.title()
                    break
    
    # Extract Date of Birth
    dob_patterns = [
        r'DOB[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})',
        r'DATE\s+OF\s+BIRTH[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})',
        r'YEAR\s+OF\s+BIRTH[:\s-]+(\d{4})',
        r'(\d{2}[/-]\d{2}[/-]\d{4})',  # Generic date pattern
    ]
    
    for pattern in dob_patterns:
        match = re.search(pattern, text)
        if match:
            dob_str = match.group(1).strip()
            try:
                if '/' in dob_str:
                    parts = dob_str.split('/')
                elif '-' in dob_str:
                    parts = dob_str.split('-')
                else:
                    if len(dob_str) == 4:
                        entities["dob"] = f"{dob_str}-01-01"
                        entities["date_of_birth"] = entities["dob"]
                    continue
                
                if len(parts) == 3:
                    day, month, year = parts
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    entities["dob"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    entities["date_of_birth"] = entities["dob"]
                    break
            except:
                entities["dob"] = dob_str
                entities["date_of_birth"] = dob_str
                break
    
    return entities


def extract_voter_id_entities(ocr_text: str) -> Dict[str, Any]:
    """
    Extract entities specifically from Voter ID card (EPIC).
    
    Voter ID card typically contains:
    - Name
    - Father's/Husband's Name
    - Date of Birth (DOB)
    - Gender
    - Address
    - Voter ID Number (EPIC number)
    - Photo
    """
    text = ocr_text.upper()
    
    entities = {
        "name": None,
        "father_name": None,
        "husband_name": None,
        "dob": None,
        "date_of_birth": None,
        "gender": None,
        "voter_id": None,
        "epic_number": None,
        "address": {
            "line1": None,
            "line2": None,
            "city": None,
            "district": None,
            "state": None,
            "pincode": None,
            "full_address": None
        },
        "constituency": None,
        "document_type": "voter_id"
    }
    
    # Extract Voter ID / EPIC Number
    epic_patterns = [
        r'EPIC\s*NO[:\s-]*([A-Z]{3}\d{7})',
        r'EPIC\s*NUMBER[:\s-]*([A-Z]{3}\d{7})',
        r'ELECTOR\'?S\s+PHOTO\s+IDENTITY\s+CARD\s+NO[:\s-]*([A-Z]{3}\d{7})',
        r'VOTER\s+ID[:\s-]*([A-Z]{3}\d{7})',
        r'([A-Z]{3}\d{7})',  # Generic EPIC pattern (3 letters + 7 digits)
    ]
    
    for pattern in epic_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            epic = str(match).strip().upper()
            if len(epic) == 10 and epic[:3].isalpha() and epic[3:].isdigit():
                entities["voter_id"] = epic
                entities["epic_number"] = epic
                break
        if entities["voter_id"]:
            break
    
    # Extract Name
    name_patterns = [
        r'NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|FATHER|HUSBAND|DOB|DATE|GENDER)',
        r'ELECTOR\'?S\s+NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|FATHER|HUSBAND|DOB)',
        r'([A-Z][A-Z\s]{3,40})\n\s*(?:FATHER|HUSBAND)',  # Name before FATHER/HUSBAND
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            name = match.group(1).strip()
            name = re.sub(r'\s+', ' ', name)
            name = re.sub(r'[^\w\s\.]', '', name)
            if len(name) > 2 and len(name) < 50:
                entities["name"] = name.title()
                break
    
    # Extract Father's Name
    father_patterns = [
        r'FATHER\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|HUSBAND|DOB|DATE|GENDER|ADDRESS)',
        r'FATHER[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|HUSBAND|DOB|DATE|GENDER|ADDRESS)',
    ]
    
    for pattern in father_patterns:
        match = re.search(pattern, text)
        if match:
            father_name = match.group(1).strip()
            father_name = re.sub(r'\s+', ' ', father_name)
            father_name = re.sub(r'[^\w\s\.]', '', father_name)
            if len(father_name) > 2 and len(father_name) < 50:
                entities["father_name"] = father_name.title()
                break
    
    # Extract Husband's Name
    husband_patterns = [
        r'HUSBAND\'?S?\s*NAME[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|GENDER|ADDRESS)',
        r'HUSBAND[:\s-]+([A-Z][A-Z\s\.]+?)(?:\n|DOB|DATE|GENDER|ADDRESS)',
    ]
    
    for pattern in husband_patterns:
        match = re.search(pattern, text)
        if match:
            husband_name = match.group(1).strip()
            husband_name = re.sub(r'\s+', ' ', husband_name)
            husband_name = re.sub(r'[^\w\s\.]', '', husband_name)
            if len(husband_name) > 2 and len(husband_name) < 50:
                entities["husband_name"] = husband_name.title()
                break
    
    # Extract Date of Birth
    dob_patterns = [
        r'DOB[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})',
        r'DATE\s+OF\s+BIRTH[:\s-]+(\d{2}[/-]\d{2}[/-]\d{4})',
        r'YEAR\s+OF\s+BIRTH[:\s-]+(\d{4})',
        r'(\d{2}[/-]\d{2}[/-]\d{4})',  # Generic date pattern
    ]
    
    for pattern in dob_patterns:
        match = re.search(pattern, text)
        if match:
            dob_str = match.group(1).strip()
            try:
                if '/' in dob_str:
                    parts = dob_str.split('/')
                elif '-' in dob_str:
                    parts = dob_str.split('-')
                else:
                    if len(dob_str) == 4:
                        entities["dob"] = f"{dob_str}-01-01"
                        entities["date_of_birth"] = entities["dob"]
                    continue
                
                if len(parts) == 3:
                    day, month, year = parts
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    entities["dob"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    entities["date_of_birth"] = entities["dob"]
                    break
            except:
                entities["dob"] = dob_str
                entities["date_of_birth"] = dob_str
                break
    
    # Extract Gender
    gender_patterns = [
        r'GENDER[:\s-]+(MALE|FEMALE|OTHER|M|F)',
        r'SEX[:\s-]+(MALE|FEMALE|OTHER|M|F)',
        r'(MALE|FEMALE|OTHER)\s*(?:\n|GENDER|ADDRESS|$)',
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
    
    # Extract Address
    address_patterns = [
        r'ADDRESS[:\s-]+(.*?)(?:\n\s*\n|CONSTITUENCY|PIN|PINCODE|$)',
        r'ADDRESS[:\s-]+(.*?)(?:\d{6})',  # Address until pincode
    ]
    
    for pattern in address_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            address_text = match.group(1).strip()
            address_lines = [line.strip() for line in address_text.split('\n') if line.strip()]
            if address_lines:
                entities["address"]["full_address"] = ', '.join(address_lines)
                if len(address_lines) > 0:
                    entities["address"]["line1"] = address_lines[0]
                if len(address_lines) > 1:
                    entities["address"]["line2"] = address_lines[1]
                if len(address_lines) > 2:
                    entities["address"]["city"] = address_lines[-2] if not re.search(r'\d{6}', address_lines[-2]) else address_lines[-3]
    
    # Extract Pincode (6 digits)
    pincode_patterns = [
        r'PIN\s*(?:CODE|NO|NUMBER)?[:\s-]*(\d{6})',
        r'PINCODE[:\s-]*(\d{6})',
        r'POSTAL\s*(?:CODE|NO|NUMBER)?[:\s-]*(\d{6})',
        r'ZIP\s*(?:CODE)?[:\s-]*(\d{6})',
        r'(\d{6})(?:\s*$|\s*\n)',  # Standalone 6-digit number at end of line
    ]
    
    for pattern in pincode_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            pincode = match.group(1).strip()
            # Validate: must be exactly 6 digits and start with 1-9 (Indian pincode format)
            if len(pincode) == 6 and pincode.isdigit() and pincode[0] in '123456789':
                entities["address"]["pincode"] = pincode
                break
        if entities["address"]["pincode"]:
            break
    
    # Extract State
    state_pattern = r'STATE[:\s-]+([A-Z][A-Z\s]+?)(?:\n|PIN|CITY|CONSTITUENCY|$)'
    match = re.search(state_pattern, text)
    if match:
        entities["address"]["state"] = match.group(1).strip().title()
    
    # Extract District
    district_pattern = r'DISTRICT[:\s-]+([A-Z][A-Z\s]+?)(?:\n|STATE|PIN|CITY|$)'
    match = re.search(district_pattern, text)
    if match:
        entities["address"]["district"] = match.group(1).strip().title()
    
    # Extract Constituency
    constituency_pattern = r'CONSTITUENCY[:\s-]+([A-Z][A-Z\s]+?)(?:\n|$)'
    match = re.search(constituency_pattern, text)
    if match:
        entities["constituency"] = match.group(1).strip().title()
    
    return entities


def extract_document_entities(ocr_text: str) -> Dict[str, Any]:
    """
    Main function to extract entities from document.
    Automatically detects document type and uses appropriate extractor.
    
    Returns:
        Dictionary with extracted entities and document_type field
    """
    # Detect document type
    doc_type = detect_document_type(ocr_text)
    
    # Use specialized extractor based on document type
    if doc_type == "aadhar":
        entities = extract_aadhar_entities(ocr_text)
    elif doc_type == "pan":
        entities = extract_pan_entities(ocr_text)
    elif doc_type == "voter_id":
        entities = extract_voter_id_entities(ocr_text)
    else:
        # Fallback to generic extractor
        entities = extract_entities(ocr_text)
        entities["document_type"] = "unknown"
    
    return entities

