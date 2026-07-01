"""
Form Mapper - Maps extracted entities to form fields
"""

from typing import Dict, Any, Optional, List
from form_templates import FormTemplate, get_form_template

def get_nested_value(data: Dict, key_path: str, default=None):
    """
    Get nested dictionary value using dot notation
    Example: get_nested_value(data, "address.city") -> data["address"]["city"]
    """
    keys = key_path.split(".")
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default
    return value if value is not None else default

def map_entities_to_form(entities: Dict[str, Any], form_id: str, language: str = "english") -> Dict[str, Any]:
    """
    Map extracted entities to a specific form template
    
    Args:
        entities: Extracted entities from entity_extractor
        form_id: ID of the form template (e.g., "domicile_certificate")
        language: Language code for translations (default: "english")
    
    Returns:
        Dictionary with form fields mapped and filled with entity values
    """
    # Get form template
    form_template = get_form_template(form_id)
    if not form_template:
        raise ValueError(f"Form template '{form_id}' not found")
    
    # Get translated form dictionary
    form_dict = form_template.to_dict(language)
    
    # Initialize mapped form data with translated labels
    mapped_form = {
        "form_id": form_id,
        "form_name": form_dict["form_name"],
        "fields": {}
    }
    
    # Map each field in the form template
    for field in form_template.fields:
        field_value = None
        
        # If field has entity mapping, try to get value from entities
        if field.entity_mapping:
            field_value = get_nested_value(entities, field.entity_mapping)
        
        # Get translated field data from form_dict
        translated_field = next((f for f in form_dict["fields"] if f["field_id"] == field.field_id), None)
        field_label = translated_field["label"] if translated_field else field.label
        field_validation = translated_field["validation"] if translated_field else field.validation
        
        # Store field data with translated label
        mapped_form["fields"][field.field_id] = {
            "label": field_label,
            "value": field_value,
            "type": field.field_type,
            "required": field.required,
            "filled": field_value is not None,
            "entity_mapping": field.entity_mapping,
            "validation": field_validation,
            "placeholder": field.placeholder
        }
    
    # Calculate completion statistics
    total_fields = len(form_template.fields)
    filled_fields = sum(1 for f in mapped_form["fields"].values() if f["filled"])
    required_fields = sum(1 for f in form_template.fields if f.required)
    filled_required = sum(
        1 for f in form_template.fields 
        if f.required and get_nested_value(entities, f.entity_mapping or "") is not None
    )
    
    mapped_form["statistics"] = {
        "total_fields": total_fields,
        "filled_fields": filled_fields,
        "required_fields": required_fields,
        "filled_required_fields": filled_required,
        "completion_percentage": round((filled_fields / total_fields) * 100, 2) if total_fields > 0 else 0,
        "required_completion_percentage": round((filled_required / required_fields) * 100, 2) if required_fields > 0 else 0
    }
    
    return mapped_form

def get_mapping_suggestions(entities: Dict[str, Any], form_id: str, language: str = "english") -> List[Dict[str, Any]]:
    """
    Get suggestions for fields that couldn't be auto-filled
    
    Args:
        entities: Extracted entities
        form_id: Form template ID
        language: Language code for translations (default: "english")
    
    Returns:
        List of suggestions for missing fields
    """
    form_template = get_form_template(form_id)
    if not form_template:
        return []
    
    # Get translated form dictionary
    form_dict = form_template.to_dict(language)
    
    suggestions = []
    
    for field in form_template.fields:
        if field.required and field.entity_mapping:
            value = get_nested_value(entities, field.entity_mapping)
            if value is None:
                # Get translated label
                translated_field = next((f for f in form_dict["fields"] if f["field_id"] == field.field_id), None)
                field_label = translated_field["label"] if translated_field else field.label
                
                suggestions.append({
                    "field_id": field.field_id,
                    "label": field_label,
                    "type": field.field_type,
                    "suggestion": f"Field '{field_label}' is required but not found in document. Please fill manually.",
                    "entity_mapping": field.entity_mapping
                })
    
    return suggestions

def update_form_field(mapped_form: Dict[str, Any], field_id: str, value: Any) -> Dict[str, Any]:
    """
    Update a specific field in the mapped form (for user edits)
    
    Args:
        mapped_form: The mapped form dictionary
        field_id: ID of the field to update
        value: New value for the field
    
    Returns:
        Updated mapped form
    """
    if field_id in mapped_form["fields"]:
        mapped_form["fields"][field_id]["value"] = value
        mapped_form["fields"][field_id]["filled"] = value is not None and value != ""
        
        # Recalculate statistics
        total_fields = mapped_form["statistics"]["total_fields"]
        filled_fields = sum(1 for f in mapped_form["fields"].values() if f["filled"])
        required_fields = mapped_form["statistics"]["required_fields"]
        filled_required = sum(
            1 for f in mapped_form["fields"].values() 
            if f["required"] and f["filled"]
        )
        
        mapped_form["statistics"]["filled_fields"] = filled_fields
        mapped_form["statistics"]["filled_required_fields"] = filled_required
        mapped_form["statistics"]["completion_percentage"] = round((filled_fields / total_fields) * 100, 2) if total_fields > 0 else 0
        mapped_form["statistics"]["required_completion_percentage"] = round((filled_required / required_fields) * 100, 2) if required_fields > 0 else 0
    
    return mapped_form

def get_form_preview(mapped_form: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a simplified preview of the mapped form (for display)
    
    Returns:
        Simplified form preview with only filled fields
    """
    preview = {
        "form_id": mapped_form["form_id"],
        "form_name": mapped_form["form_name"],
        "filled_fields": {},
        "missing_required_fields": [],
        "statistics": mapped_form["statistics"]
    }
    
    for field_id, field_data in mapped_form["fields"].items():
        if field_data["filled"]:
            preview["filled_fields"][field_id] = {
                "label": field_data["label"],
                "value": field_data["value"],
                "type": field_data["type"]
            }
        elif field_data["required"]:
            preview["missing_required_fields"].append({
                "field_id": field_id,
                "label": field_data["label"],
                "type": field_data["type"]
            })
    
    return preview





