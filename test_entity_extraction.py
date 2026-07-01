"""
Test Script for Entity Extraction
Run this to see step-by-step how entity extraction works
"""

from entity_extractor import extract_entities
import json

def print_step(step_num, description):
    """Print a formatted step header"""
    print("\n" + "="*60)
    print(f"STEP {step_num}: {description}")
    print("="*60)

def demonstrate_entity_extraction():
    """Demonstrate entity extraction step by step"""
    
    # Sample OCR text (simulating what we get from OCR)
    ocr_text = """
    Name:- Saurabh R. Kshirsgar.
    DOB:- 02/04/1990
    
    City:- Pune
    
    Pan: abcde1234Z
    
    Adhar:- 1234 5678 9101
    
    Mobile: 9876543210
    Email: saurabh.kshirsgar@example.com
    """
    
    print_step(1, "INPUT - OCR Text (Unstructured)")
    print("Raw OCR text received:")
    print("-" * 60)
    print(ocr_text)
    print("-" * 60)
    
    print_step(2, "TEXT NORMALIZATION")
    print("Converting to uppercase for pattern matching:")
    print("-" * 60)
    normalized = ocr_text.upper()
    print(normalized)
    print("-" * 60)
    
    print_step(3, "PATTERN MATCHING")
    print("Applying regex patterns to extract entities...")
    print("-" * 60)
    
    # Show individual pattern matches
    import re
    
    # Name pattern
    name_pattern = r'NAME[:\s-]+([A-Z][A-Z\s\.]+)'
    name_match = re.search(name_pattern, normalized)
    if name_match:
        print(f"[OK] Name found: {name_match.group(1).strip()}")
    
    # DOB pattern
    dob_pattern = r'DOB[:\s-]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    dob_match = re.search(dob_pattern, normalized)
    if dob_match:
        print(f"[OK] DOB found: {dob_match.group(1)}")
    
    # PAN pattern
    pan_pattern = r'PAN[:\s-]+([A-Z]{5}\d{4}[A-Z])'
    pan_match = re.search(pan_pattern, normalized)
    if pan_match:
        print(f"[OK] PAN found: {pan_match.group(1)}")
    
    # Aadhaar pattern
    aadhaar_pattern = r'AADHAR[:\s-]+(\d{4}\s?\d{4}\s?\d{4})'
    aadhaar_match = re.search(aadhaar_pattern, normalized)
    if aadhaar_match:
        print(f"[OK] Aadhaar found: {aadhaar_match.group(1)}")
    
    # City pattern
    city_pattern = r'CITY[:\s-]+([A-Z][A-Z\s]+?)(?:\n|$|PAN|AADHAAR|DOB)'
    city_match = re.search(city_pattern, normalized)
    if city_match:
        print(f"[OK] City found: {city_match.group(1).strip()}")
    
    # Mobile pattern
    mobile_pattern = r'MOBILE[:\s-]+(\d{10})'
    mobile_match = re.search(mobile_pattern, normalized)
    if mobile_match:
        print(f"[OK] Mobile found: {mobile_match.group(1)}")
    
    # Email pattern
    email_pattern = r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})'
    email_match = re.search(email_pattern, normalized)
    if email_match:
        print(f"[OK] Email found: {email_match.group(1)}")
    
    print("-" * 60)
    
    print_step(4, "EXTRACTING ENTITIES")
    print("Running extract_entities() function...")
    print("-" * 60)
    
    # Extract entities
    entities = extract_entities(ocr_text)
    
    print_step(5, "OUTPUT - Structured JSON")
    print("Extracted entities:")
    print("-" * 60)
    print(json.dumps(entities, indent=2, ensure_ascii=False))
    print("-" * 60)
    
    print_step(6, "SUMMARY")
    print("Fields successfully extracted:")
    print("-" * 60)
    
    extracted_count = 0
    total_fields = 0
    
    # Count extracted fields
    if entities.get("name"):
        print(f"[OK] Name: {entities['name']}")
        extracted_count += 1
    total_fields += 1
    
    if entities.get("dob"):
        print(f"[OK] DOB: {entities['dob']}")
        extracted_count += 1
    total_fields += 1
    
    if entities.get("pan_number"):
        print(f"[OK] PAN: {entities['pan_number']}")
        extracted_count += 1
    total_fields += 1
    
    if entities.get("aadhaar_number"):
        print(f"[OK] Aadhaar: {entities['aadhaar_number']}")
        extracted_count += 1
    total_fields += 1
    
    if entities.get("address", {}).get("city"):
        print(f"[OK] City: {entities['address']['city']}")
        extracted_count += 1
    total_fields += 1
    
    if entities.get("mobile"):
        print(f"[OK] Mobile: {entities['mobile']}")
        extracted_count += 1
    total_fields += 1
    
    if entities.get("email"):
        print(f"[OK] Email: {entities['email']}")
        extracted_count += 1
    total_fields += 1
    
    print("-" * 60)
    print(f"Extracted: {extracted_count} out of {total_fields} common fields")
    print("=" * 60)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("ENTITY EXTRACTION DEMONSTRATION")
    print("="*60)
    demonstrate_entity_extraction()
    print("\n[SUCCESS] Demonstration complete!")
    print("\nTo test with your own text, modify the 'ocr_text' variable")
    print("or use the API endpoint: POST /extract-entities")

