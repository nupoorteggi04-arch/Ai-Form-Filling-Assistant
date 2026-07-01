"""
Test Script for Form Mapping
Demonstrates how entities are mapped to form fields
"""

from entity_extractor import extract_entities
from form_mapper import map_entities_to_form, get_mapping_suggestions, get_form_preview
from form_templates import get_all_form_templates
import json

def print_step(step_num, description):
    """Print a formatted step header"""
    print("\n" + "="*70)
    print(f"STEP {step_num}: {description}")
    print("="*70)

def demonstrate_form_mapping():
    """Demonstrate form mapping step by step"""
    
    # Sample extracted entities (simulating what we get from entity extraction)
    sample_entities = {
        "name": "Saurabh R. Kshirsgar",
        "dob": "1990-04-02",
        "date_of_birth": "1990-04-02",
        "gender": None,
        "father_name": None,
        "mother_name": None,
        "address": {
            "line1": None,
            "line2": None,
            "city": "Pune",
            "district": None,
            "state": None,
            "pincode": None,
            "full_address": None
        },
        "aadhaar_number": "123456789101",
        "pan_number": "ABCDE1234Z",
        "voter_id": None,
        "mobile": "9876543210",
        "email": "saurabh.kshirsgar@example.com"
    }
    
    print_step(1, "AVAILABLE FORM TEMPLATES")
    print("Forms available in the system:")
    print("-" * 70)
    forms = get_all_form_templates()
    for form in forms:
        print(f"[{form['form_id']}] {form['form_name']}")
        print(f"  Description: {form['description']}")
        print(f"  Fields: {len(form['fields'])}")
        print()
    print("-" * 70)
    
    print_step(2, "INPUT - EXTRACTED ENTITIES")
    print("Entities extracted from document:")
    print("-" * 70)
    print(json.dumps(sample_entities, indent=2, ensure_ascii=False))
    print("-" * 70)
    
    # Test mapping to Domicile Certificate form
    form_id = "domicile_certificate"
    
    print_step(3, f"MAPPING TO FORM: {form_id.upper().replace('_', ' ')}")
    print(f"Mapping entities to '{form_id}' form template...")
    print("-" * 70)
    
    mapped_form = map_entities_to_form(sample_entities, form_id)
    
    print_step(4, "MAPPED FORM FIELDS")
    print("Fields in the form and their mapped values:")
    print("-" * 70)
    
    for field_id, field_data in mapped_form["fields"].items():
        status = "[FILLED]" if field_data["filled"] else "[EMPTY]"
        required = "[REQUIRED]" if field_data["required"] else "[OPTIONAL]"
        value = field_data["value"] if field_data["value"] is not None else "(not found)"
        mapping = f" <- {field_data['entity_mapping']}" if field_data["entity_mapping"] else " (manual entry)"
        
        print(f"{status} {required} {field_data['label']}")
        print(f"    Value: {value}{mapping}")
        print()
    
    print("-" * 70)
    
    print_step(5, "MAPPING STATISTICS")
    print("Form completion statistics:")
    print("-" * 70)
    stats = mapped_form["statistics"]
    print(f"Total fields: {stats['total_fields']}")
    print(f"Filled fields: {stats['filled_fields']}")
    print(f"Required fields: {stats['required_fields']}")
    print(f"Filled required fields: {stats['filled_required_fields']}")
    print(f"Overall completion: {stats['completion_percentage']}%")
    print(f"Required fields completion: {stats['required_completion_percentage']}%")
    print("-" * 70)
    
    print_step(6, "MISSING FIELDS SUGGESTIONS")
    suggestions = get_mapping_suggestions(sample_entities, form_id)
    if suggestions:
        print("Fields that need to be filled manually:")
        print("-" * 70)
        for suggestion in suggestions:
            print(f"[REQUIRED] {suggestion['label']}")
            print(f"    Reason: {suggestion['suggestion']}")
            print(f"    Expected mapping: {suggestion['entity_mapping']}")
            print()
    else:
        print("All required fields have been mapped!")
    print("-" * 70)
    
    print_step(7, "FORM PREVIEW")
    print("Simplified preview of the mapped form:")
    print("-" * 70)
    preview = get_form_preview(mapped_form)
    print(f"Form: {preview['form_name']}")
    print(f"\nFilled Fields ({len(preview['filled_fields'])}):")
    for field_id, field_data in preview["filled_fields"].items():
        print(f"  - {field_data['label']}: {field_data['value']}")
    
    if preview["missing_required_fields"]:
        print(f"\nMissing Required Fields ({len(preview['missing_required_fields'])}):")
        for field in preview["missing_required_fields"]:
            print(f"  - {field['label']} ({field['type']})")
    print("-" * 70)
    
    print_step(8, "COMPLETE MAPPED FORM JSON")
    print("Full mapped form structure:")
    print("-" * 70)
    print(json.dumps(mapped_form, indent=2, ensure_ascii=False))
    print("-" * 70)

def test_multiple_forms():
    """Test mapping to multiple form types"""
    print("\n" + "="*70)
    print("TESTING MULTIPLE FORM TYPES")
    print("="*70)
    
    sample_entities = {
        "name": "Saurabh R. Kshirsgar",
        "dob": "1990-04-02",
        "city": "Pune",
        "aadhaar_number": "123456789101",
        "pan_number": "ABCDE1234Z",
        "mobile": "9876543210"
    }
    
    form_ids = ["domicile_certificate", "income_certificate", "caste_certificate"]
    
    for form_id in form_ids:
        print(f"\n[{form_id}]")
        print("-" * 70)
        mapped_form = map_entities_to_form(sample_entities, form_id)
        stats = mapped_form["statistics"]
        print(f"Completion: {stats['completion_percentage']}% ({stats['filled_fields']}/{stats['total_fields']} fields)")
        print(f"Required completion: {stats['required_completion_percentage']}%")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FORM MAPPING DEMONSTRATION")
    print("="*70)
    
    demonstrate_form_mapping()
    
    print("\n" + "="*70)
    print("TESTING MULTIPLE FORMS")
    print("="*70)
    test_multiple_forms()
    
    print("\n" + "="*70)
    print("[SUCCESS] Demonstration complete!")
    print("="*70)
    print("\nTo test via API:")
    print("1. GET /forms - List all available forms")
    print("2. GET /forms/{form_id} - Get specific form template")
    print("3. POST /forms/map - Map entities to form")
    print("4. POST /process-and-map - Process document and map in one step")





