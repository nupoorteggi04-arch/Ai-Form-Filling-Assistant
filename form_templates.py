"""
Form Templates for Indian Government Services
Defines structure and field mappings for various government forms
"""

from typing import Dict, List, Any, Optional

# Translation dictionaries for form labels
FORM_TRANSLATIONS: Dict[str, Dict[str, Dict[str, str]]] = {
    "english": {
        "domicile_certificate": {
            "form_name": "Domicile Certificate",
            "description": "Certificate of Domicile/Residence for Indian citizens",
            "applicant_name": "Applicant Full Name",
            "father_name": "Father's Name",
            "mother_name": "Mother's Name",
            "date_of_birth": "Date of Birth",
            "gender": "Gender",
            "address_line1": "Address Line 1",
            "address_line2": "Address Line 2",
            "city": "City/Town",
            "district": "District",
            "state": "State",
            "pincode": "PIN Code",
            "aadhaar_number": "Aadhaar Number",
            "mobile_number": "Mobile Number",
            "email": "Email Address",
        },
        "income_certificate": {
            "form_name": "Income Certificate",
            "description": "Certificate of Income for availing government schemes",
            "applicant_name": "Applicant Full Name",
            "father_name": "Father's/Husband's Name",
            "date_of_birth": "Date of Birth",
            "gender": "Gender",
            "address_line1": "Permanent Address Line 1",
            "city": "City/Town",
            "district": "District",
            "state": "State",
            "pincode": "PIN Code",
            "aadhaar_number": "Aadhaar Number",
            "pan_number": "PAN Number (if applicable)",
            "annual_income": "Annual Income (INR)",
            "mobile_number": "Mobile Number",
        },
        "caste_certificate": {
            "form_name": "Caste Certificate",
            "description": "Certificate for Scheduled Caste/Scheduled Tribe/Other Backward Classes",
            "applicant_name": "Applicant Full Name",
            "father_name": "Father's Name",
            "mother_name": "Mother's Name",
            "date_of_birth": "Date of Birth",
            "gender": "Gender",
            "caste_category": "Caste Category",
            "caste_name": "Caste Name",
            "address_line1": "Address Line 1",
            "city": "City/Town",
            "district": "District",
            "state": "State",
            "pincode": "PIN Code",
            "aadhaar_number": "Aadhaar Number",
            "mobile_number": "Mobile Number",
        },
        "birth_certificate": {
            "form_name": "Birth Certificate Application",
            "description": "Application for Birth Certificate",
            "child_name": "Child's Full Name",
            "date_of_birth": "Date of Birth",
            "gender": "Gender",
            "father_name": "Father's Full Name",
            "mother_name": "Mother's Full Name",
            "place_of_birth": "Place of Birth",
            "address_line1": "Address Line 1",
            "city": "City/Town",
            "district": "District",
            "state": "State",
            "pincode": "PIN Code",
            "aadhaar_number": "Aadhaar Number (if available)",
            "mobile_number": "Mobile Number",
        },
    },
    "hindi": {
        "domicile_certificate": {
            "form_name": "अधिवास प्रमाणपत्र",
            "description": "भारतीय नागरिकों के लिए अधिवास/निवास प्रमाणपत्र",
            "applicant_name": "आवेदक का पूरा नाम",
            "father_name": "पिता का नाम",
            "mother_name": "माता का नाम",
            "date_of_birth": "जन्म तिथि",
            "gender": "लिंग",
            "address_line1": "पता पंक्ति 1",
            "address_line2": "पता पंक्ति 2",
            "city": "शहर/कस्बा",
            "district": "जिला",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार संख्या",
            "mobile_number": "मोबाइल नंबर",
            "email": "ईमेल पता",
        },
        "income_certificate": {
            "form_name": "आय प्रमाणपत्र",
            "description": "सरकारी योजनाओं के लिए आय प्रमाणपत्र",
            "applicant_name": "आवेदक का पूरा नाम",
            "father_name": "पिता/पति का नाम",
            "date_of_birth": "जन्म तिथि",
            "gender": "लिंग",
            "address_line1": "स्थायी पता पंक्ति 1",
            "city": "शहर/कस्बा",
            "district": "जिला",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार संख्या",
            "pan_number": "पैन नंबर (यदि उपलब्ध)",
            "annual_income": "वार्षिक आय (रुपए)",
            "mobile_number": "मोबाइल नंबर",
        },
        "caste_certificate": {
            "form_name": "जाति प्रमाणपत्र",
            "description": "अनुसूचित जाति/अनुसूचित जनजाति/अन्य पिछड़ा वर्ग प्रमाणपत्र",
            "applicant_name": "आवेदक का पूरा नाम",
            "father_name": "पिता का नाम",
            "mother_name": "माता का नाम",
            "date_of_birth": "जन्म तिथि",
            "gender": "लिंग",
            "caste_category": "जाति श्रेणी",
            "caste_name": "जाति का नाम",
            "address_line1": "पता पंक्ति 1",
            "city": "शहर/कस्बा",
            "district": "जिला",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार संख्या",
            "mobile_number": "मोबाइल नंबर",
        },
        "birth_certificate": {
            "form_name": "जन्म प्रमाणपत्र आवेदन",
            "description": "जन्म प्रमाणपत्र के लिए आवेदन",
            "child_name": "बच्चे का पूरा नाम",
            "date_of_birth": "जन्म तिथि",
            "gender": "लिंग",
            "father_name": "पिता का पूरा नाम",
            "mother_name": "माता का पूरा नाम",
            "place_of_birth": "जन्म स्थान",
            "address_line1": "पता पंक्ति 1",
            "city": "शहर/कस्बा",
            "district": "जिला",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार संख्या (यदि उपलब्ध)",
            "mobile_number": "मोबाइल नंबर",
        },
    },
    "marathi": {
        "domicile_certificate": {
            "form_name": "निवास प्रमाणपत्र",
            "description": "भारतीय नागरिकांसाठी निवास/वास्तव्य प्रमाणपत्र",
            "applicant_name": "अर्जदाराचे पूर्ण नाव",
            "father_name": "वडिलांचे नाव",
            "mother_name": "आईचे नाव",
            "date_of_birth": "जन्मतारीख",
            "gender": "लिंग",
            "address_line1": "पत्ता ओळ 1",
            "address_line2": "पत्ता ओळ 2",
            "city": "शहर/कस्बा",
            "district": "जिल्हा",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार क्रमांक",
            "mobile_number": "मोबाइल नंबर",
            "email": "ईमेल पत्ता",
        },
        "income_certificate": {
            "form_name": "उत्पन्न प्रमाणपत्र",
            "description": "सरकारी योजनांसाठी उत्पन्न प्रमाणपत्र",
            "applicant_name": "अर्जदाराचे पूर्ण नाव",
            "father_name": "वडिल/पतीचे नाव",
            "date_of_birth": "जन्मतारीख",
            "gender": "लिंग",
            "address_line1": "स्थायी पत्ता ओळ 1",
            "city": "शहर/कस्बा",
            "district": "जिल्हा",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार क्रमांक",
            "pan_number": "पॅन नंबर (उपलब्ध असल्यास)",
            "annual_income": "वार्षिक उत्पन्न (रुपये)",
            "mobile_number": "मोबाइल नंबर",
        },
        "caste_certificate": {
            "form_name": "जात प्रमाणपत्र",
            "description": "अनुसूचित जाती/अनुसूचित जमाती/इतर मागास वर्ग प्रमाणपत्र",
            "applicant_name": "अर्जदाराचे पूर्ण नाव",
            "father_name": "वडिलांचे नाव",
            "mother_name": "आईचे नाव",
            "date_of_birth": "जन्मतारीख",
            "gender": "लिंग",
            "caste_category": "जात श्रेणी",
            "caste_name": "जातीचे नाव",
            "address_line1": "पत्ता ओळ 1",
            "city": "शहर/कस्बा",
            "district": "जिल्हा",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार क्रमांक",
            "mobile_number": "मोबाइल नंबर",
        },
        "birth_certificate": {
            "form_name": "जन्म प्रमाणपत्र अर्ज",
            "description": "जन्म प्रमाणपत्रासाठी अर्ज",
            "child_name": "मुलाचे पूर्ण नाव",
            "date_of_birth": "जन्मतारीख",
            "gender": "लिंग",
            "father_name": "वडिलांचे पूर्ण नाव",
            "mother_name": "आईचे पूर्ण नाव",
            "place_of_birth": "जन्मस्थळ",
            "address_line1": "पत्ता ओळ 1",
            "city": "शहर/कस्बा",
            "district": "जिल्हा",
            "state": "राज्य",
            "pincode": "पिन कोड",
            "aadhaar_number": "आधार क्रमांक (उपलब्ध असल्यास)",
            "mobile_number": "मोबाइल नंबर",
        },
    },
    "tamil": {
        "domicile_certificate": {
            "form_name": "வாழ்விட சான்றிதழ்",
            "description": "இந்திய குடிமக்களுக்கான வாழ்விட/வசிப்பு சான்றிதழ்",
            "applicant_name": "விண்ணப்பதாரர் முழு பெயர்",
            "father_name": "தந்தையின் பெயர்",
            "mother_name": "தாயின் பெயர்",
            "date_of_birth": "பிறந்த தேதி",
            "gender": "பாலினம்",
            "address_line1": "முகவரி வரி 1",
            "address_line2": "முகவரி வரி 2",
            "city": "நகரம்/பேரூர்",
            "district": "மாவட்டம்",
            "state": "மாநிலம்",
            "pincode": "அஞ்சல் குறியீடு",
            "aadhaar_number": "ஆதார் எண்",
            "mobile_number": "மொபைல் எண்",
            "email": "மின்னஞ்சல் முகவரி",
        },
        "income_certificate": {
            "form_name": "வருமான சான்றிதழ்",
            "description": "அரசு திட்டங்களுக்கான வருமான சான்றிதழ்",
            "applicant_name": "விண்ணப்பதாரர் முழு பெயர்",
            "father_name": "தந்தை/கணவர் பெயர்",
            "date_of_birth": "பிறந்த தேதி",
            "gender": "பாலினம்",
            "address_line1": "நிரந்தர முகவரி வரி 1",
            "city": "நகரம்/பேரூர்",
            "district": "மாவட்டம்",
            "state": "மாநிலம்",
            "pincode": "அஞ்சல் குறியீடு",
            "aadhaar_number": "ஆதார் எண்",
            "pan_number": "PAN எண் (இருந்தால்)",
            "annual_income": "ஆண்டு வருமானம் (ரூபாய்)",
            "mobile_number": "மொபைல் எண்",
        },
        "caste_certificate": {
            "form_name": "சாதி சான்றிதழ்",
            "description": "திட்டமிடப்பட்ட சாதி/திட்டமிடப்பட்ட பழங்குடி/பிற பிற்படுத்தப்பட்ட வகுப்பு சான்றிதழ்",
            "applicant_name": "விண்ணப்பதாரர் முழு பெயர்",
            "father_name": "தந்தையின் பெயர்",
            "mother_name": "தாயின் பெயர்",
            "date_of_birth": "பிறந்த தேதி",
            "gender": "பாலினம்",
            "caste_category": "சாதி வகை",
            "caste_name": "சாதி பெயர்",
            "address_line1": "முகவரி வரி 1",
            "city": "நகரம்/பேரூர்",
            "district": "மாவட்டம்",
            "state": "மாநிலம்",
            "pincode": "அஞ்சல் குறியீடு",
            "aadhaar_number": "ஆதார் எண்",
            "mobile_number": "மொபைல் எண்",
        },
        "birth_certificate": {
            "form_name": "பிறப்புச் சான்றிதழ் விண்ணப்பம்",
            "description": "பிறப்புச் சான்றிதழுக்கான விண்ணப்பம்",
            "child_name": "குழந்தையின் முழு பெயர்",
            "date_of_birth": "பிறந்த தேதி",
            "gender": "பாலினம்",
            "father_name": "தந்தையின் முழு பெயர்",
            "mother_name": "தாயின் முழு பெயர்",
            "place_of_birth": "பிறந்த இடம்",
            "address_line1": "முகவரி வரி 1",
            "city": "நகரம்/பேரூர்",
            "district": "மாவட்டம்",
            "state": "மாநிலம்",
            "pincode": "அஞ்சல் குறியீடு",
            "aadhaar_number": "ஆதார் எண் (இருந்தால்)",
            "mobile_number": "மொபைல் எண்",
        },
    },
    "telugu": {
        "domicile_certificate": {
            "form_name": "నివాస ధృవపత్రం",
            "description": "భారతీయ పౌరులకు నివాస/వాసస్థల ధృవపత్రం",
            "applicant_name": "అభ్యర్థి పూర్తి పేరు",
            "father_name": "తండ్రి పేరు",
            "mother_name": "తల్లి పేరు",
            "date_of_birth": "జనన తేదీ",
            "gender": "లింగం",
            "address_line1": "చిరునామా వరుస 1",
            "address_line2": "చిరునామా వరుస 2",
            "city": "నగరం/పట్టణం",
            "district": "జిల్లా",
            "state": "రాష్ట్రం",
            "pincode": "పిన్ కోడ్",
            "aadhaar_number": "ఆధార్ సంఖ్య",
            "mobile_number": "మొబైల్ నంబర్",
            "email": "ఇమెయిల్ చిరునామా",
        },
        "income_certificate": {
            "form_name": "ఆదాయ ధృవపత్రం",
            "description": "ప్రభుత్వ పథకాల కోసం ఆదాయ ధృవపత్రం",
            "applicant_name": "అభ్యర్థి పూర్తి పేరు",
            "father_name": "తండ్రి/భర్త పేరు",
            "date_of_birth": "జనన తేదీ",
            "gender": "లింగం",
            "address_line1": "శాశ్వత చిరునామా వరుస 1",
            "city": "నగరం/పట్టణం",
            "district": "జిల్లా",
            "state": "రాష్ట్రం",
            "pincode": "పిన్ కోడ్",
            "aadhaar_number": "ఆధార్ సంఖ్య",
            "pan_number": "PAN నంబర్ (ఉన్నట్లయితే)",
            "annual_income": "సంవత్సరాంత ఆదాయం (రూపాయలు)",
            "mobile_number": "మొబైల్ నంబర్",
        },
        "caste_certificate": {
            "form_name": "జాతి ధృవపత్రం",
            "description": "షెడ్యూల్డ్ కులం/షెడ్యూల్డ్ తెగ/ఇతర వెనుకబడిన తరగతి ధృవపత్రం",
            "applicant_name": "అభ్యర్థి పూర్తి పేరు",
            "father_name": "తండ్రి పేరు",
            "mother_name": "తల్లి పేరు",
            "date_of_birth": "జనన తేదీ",
            "gender": "లింగం",
            "caste_category": "జాతి వర్గం",
            "caste_name": "జాతి పేరు",
            "address_line1": "చిరునామా వరుస 1",
            "city": "నగరం/పట్టణం",
            "district": "జిల్లా",
            "state": "రాష్ట్రం",
            "pincode": "పిన్ కోడ్",
            "aadhaar_number": "ఆధార్ సంఖ్య",
            "mobile_number": "మొబైల్ నంబర్",
        },
        "birth_certificate": {
            "form_name": "జనన ధృవపత్రం అప్లికేషన్",
            "description": "జనన ధృవపత్రం కోసం అప్లికేషన్",
            "child_name": "పిల్లల పూర్తి పేరు",
            "date_of_birth": "జనన తేదీ",
            "gender": "లింగం",
            "father_name": "తండ్రి పూర్తి పేరు",
            "mother_name": "తల్లి పూర్తి పేరు",
            "place_of_birth": "జనన స్థలం",
            "address_line1": "చిరునామా వరుస 1",
            "city": "నగరం/పట్టణం",
            "district": "జిల్లా",
            "state": "రాష్ట్రం",
            "pincode": "పిన్ కోడ్",
            "aadhaar_number": "ఆధార్ సంఖ్య (ఉన్నట్లయితే)",
            "mobile_number": "మొబైల్ నంబర్",
        },
    },
}

# Gender options translations
GENDER_OPTIONS_TRANSLATIONS: Dict[str, List[str]] = {
    "english": ["Male", "Female", "Other"],
    "hindi": ["पुरुष", "महिला", "अन्य"],
    "marathi": ["पुरुष", "स्त्री", "इतर"],
    "tamil": ["ஆண்", "பெண்", "மற்றவை"],
    "telugu": ["పురుషుడు", "స్త్రీ", "ఇతరులు"],
    "gujarati": ["પુરુષ", "સ્ત્રી", "અન્ય"],
    "bengali": ["পুরুষ", "মহিলা", "অন্যান্য"],
    "kannada": ["ಪುರುಷ", "ಮಹಿಳೆ", "ಇತರರು"],
    "malayalam": ["പുരുഷൻ", "സ്ത്രീ", "മറ്റുള്ളവർ"],
    "punjabi": ["ਪੁਰਸ਼", "ਔਰਤ", "ਹੋਰ"],
}

# Caste category translations
CASTE_CATEGORY_TRANSLATIONS: Dict[str, List[str]] = {
    "english": ["SC", "ST", "OBC", "General"],
    "hindi": ["अनुसूचित जाति", "अनुसूचित जनजाति", "अन्य पिछड़ा वर्ग", "सामान्य"],
    "marathi": ["अनुसूचित जाती", "अनुसूचित जमाती", "इतर मागास वर्ग", "सामान्य"],
    "tamil": ["திட்டமிடப்பட்ட சாதி", "திட்டமிடப்பட்ட பழங்குடி", "பிற பிற்படுத்தப்பட்ட வகுப்பு", "பொது"],
    "telugu": ["షెడ్యూల్డ్ కులం", "షెడ్యూల్డ్ తెగ", "ఇతర వెనుకబడిన తరగతి", "సాధారణ"],
}

def get_translation(form_id: str, field_key: str, language: str = "english") -> str:
    """
    Get translated label for a form field
    
    Args:
        form_id: Form template ID (e.g., "domicile_certificate")
        field_key: Field key (e.g., "applicant_name", "form_name")
        language: Language code (default: "english")
    
    Returns:
        Translated label, or English label if translation not found
    """
    lang = language.lower()
    
    # Try to get translation in requested language
    if lang in FORM_TRANSLATIONS:
        translations = FORM_TRANSLATIONS[lang]
        form_translations = translations.get(form_id, {})
        translated_label = form_translations.get(field_key)
        if translated_label:
            return translated_label
    
    # Fallback to English translation
    if lang != "english" and "english" in FORM_TRANSLATIONS:
        english_translations = FORM_TRANSLATIONS["english"]
        english_form_translations = english_translations.get(form_id, {})
        english_label = english_form_translations.get(field_key)
        if english_label:
            return english_label
    
    # Final fallback: return field_key (shouldn't happen if all translations are defined)
    return field_key

class FormField:
    """Represents a single field in a government form"""
    def __init__(
        self,
        field_id: str,
        label: str,
        field_type: str = "text",
        required: bool = False,
        entity_mapping: Optional[str] = None,
        validation: Optional[Dict] = None,
        placeholder: Optional[str] = None
    ):
        self.field_id = field_id
        self.label = label
        self.field_type = field_type  # text, date, number, select, etc.
        self.required = required
        self.entity_mapping = entity_mapping  # Maps to entity key (e.g., "name", "dob")
        self.validation = validation or {}
        self.placeholder = placeholder

class FormTemplate:
    """Represents a complete government form template"""
    def __init__(
        self,
        form_id: str,
        form_name: str,
        description: str,
        fields: List[FormField],
        category: str = "certificate"
    ):
        self.form_id = form_id
        self.form_name = form_name
        self.description = description
        self.fields = fields
        self.category = category
    
    def to_dict(self, language: str = "english") -> Dict[str, Any]:
        """Convert form template to dictionary with optional language translation"""
        # Get translated form name and description
        translated_form_name = get_translation(self.form_id, "form_name", language)
        translated_description = get_translation(self.form_id, "description", language)
        
        # Get translated labels for fields
        translated_fields = []
        for field in self.fields:
            translated_label = get_translation(self.form_id, field.field_id, language)
            
            # Handle validation options translation (for gender, caste_category)
            validation = field.validation.copy() if field.validation else {}
            if "options" in validation:
                if field.field_id == "gender":
                    validation["options"] = GENDER_OPTIONS_TRANSLATIONS.get(
                        language.lower(), 
                        GENDER_OPTIONS_TRANSLATIONS["english"]
                    )
                elif field.field_id == "caste_category":
                    validation["options"] = CASTE_CATEGORY_TRANSLATIONS.get(
                        language.lower(),
                        CASTE_CATEGORY_TRANSLATIONS["english"]
                    )
            
            translated_fields.append({
                "field_id": field.field_id,
                "label": translated_label,
                "type": field.field_type,
                "required": field.required,
                "entity_mapping": field.entity_mapping,
                "validation": validation,
                "placeholder": field.placeholder  # Placeholders remain in English for now
            })
        
        return {
            "form_id": self.form_id,
            "form_name": translated_form_name,
            "description": translated_description,
            "category": self.category,
            "fields": translated_fields
        }

# Form Templates Database
FORM_TEMPLATES: Dict[str, FormTemplate] = {}

def register_form_template(template: FormTemplate):
    """Register a form template"""
    FORM_TEMPLATES[template.form_id] = template

def get_form_template(form_id: str) -> Optional[FormTemplate]:
    """Get a form template by ID"""
    return FORM_TEMPLATES.get(form_id)

def get_all_form_templates(language: str = "english") -> List[Dict[str, Any]]:
    """Get all form templates as dictionaries with optional language translation"""
    return [template.to_dict(language) for template in FORM_TEMPLATES.values()]

# ============================================================================
# DOMICILE CERTIFICATE FORM
# ============================================================================
domicile_form = FormTemplate(
    form_id="domicile_certificate",
    form_name="Domicile Certificate",
    description="Certificate of Domicile/Residence for Indian citizens",
    category="certificate",
    fields=[
        FormField(
            field_id="applicant_name",
            label="Applicant Full Name",
            field_type="text",
            required=True,
            entity_mapping="name",
            placeholder="Enter full name as per Aadhaar"
        ),
        FormField(
            field_id="father_name",
            label="Father's Name",
            field_type="text",
            required=True,
            entity_mapping="father_name",
            placeholder="Enter father's full name"
        ),
        FormField(
            field_id="mother_name",
            label="Mother's Name",
            field_type="text",
            required=False,
            entity_mapping="mother_name",
            placeholder="Enter mother's full name"
        ),
        FormField(
            field_id="date_of_birth",
            label="Date of Birth",
            field_type="date",
            required=True,
            entity_mapping="dob",
            placeholder="DD/MM/YYYY"
        ),
        FormField(
            field_id="gender",
            label="Gender",
            field_type="select",
            required=True,
            entity_mapping="gender",
            validation={"options": ["Male", "Female", "Other"]}
        ),
        FormField(
            field_id="address_line1",
            label="Address Line 1",
            field_type="text",
            required=True,
            entity_mapping="address.line1",
            placeholder="House/Flat No., Street"
        ),
        FormField(
            field_id="address_line2",
            label="Address Line 2",
            field_type="text",
            required=False,
            entity_mapping="address.line2",
            placeholder="Area, Locality"
        ),
        FormField(
            field_id="city",
            label="City/Town",
            field_type="text",
            required=True,
            entity_mapping="address.city",
            placeholder="Enter city name"
        ),
        FormField(
            field_id="district",
            label="District",
            field_type="text",
            required=True,
            entity_mapping="address.district",
            placeholder="Enter district name"
        ),
        FormField(
            field_id="state",
            label="State",
            field_type="text",
            required=True,
            entity_mapping="address.state",
            placeholder="Enter state name"
        ),
        FormField(
            field_id="pincode",
            label="PIN Code",
            field_type="text",
            required=True,
            entity_mapping="address.pincode",
            validation={"pattern": r"^\d{6}$"},
            placeholder="6-digit PIN code"
        ),
        FormField(
            field_id="aadhaar_number",
            label="Aadhaar Number",
            field_type="text",
            required=True,
            entity_mapping="aadhaar_number",
            validation={"pattern": r"^\d{12}$"},
            placeholder="12-digit Aadhaar number"
        ),
        FormField(
            field_id="mobile_number",
            label="Mobile Number",
            field_type="text",
            required=True,
            entity_mapping="mobile",
            validation={"pattern": r"^\d{10}$"},
            placeholder="10-digit mobile number"
        ),
        FormField(
            field_id="email",
            label="Email Address",
            field_type="email",
            required=False,
            entity_mapping="email",
            placeholder="example@email.com"
        ),
    ]
)

register_form_template(domicile_form)

# ============================================================================
# INCOME CERTIFICATE FORM
# ============================================================================
income_form = FormTemplate(
    form_id="income_certificate",
    form_name="Income Certificate",
    description="Certificate of Income for availing government schemes",
    category="certificate",
    fields=[
        FormField(
            field_id="applicant_name",
            label="Applicant Full Name",
            field_type="text",
            required=True,
            entity_mapping="name",
            placeholder="Enter full name"
        ),
        FormField(
            field_id="father_name",
            label="Father's/Husband's Name",
            field_type="text",
            required=True,
            entity_mapping="father_name",
            placeholder="Enter father's or husband's name"
        ),
        FormField(
            field_id="date_of_birth",
            label="Date of Birth",
            field_type="date",
            required=True,
            entity_mapping="dob",
            placeholder="DD/MM/YYYY"
        ),
        FormField(
            field_id="gender",
            label="Gender",
            field_type="select",
            required=True,
            entity_mapping="gender",
            validation={"options": ["Male", "Female", "Other"]}
        ),
        FormField(
            field_id="address_line1",
            label="Permanent Address Line 1",
            field_type="text",
            required=True,
            entity_mapping="address.line1",
            placeholder="House/Flat No., Street"
        ),
        FormField(
            field_id="city",
            label="City/Town",
            field_type="text",
            required=True,
            entity_mapping="address.city",
            placeholder="Enter city name"
        ),
        FormField(
            field_id="district",
            label="District",
            field_type="text",
            required=True,
            entity_mapping="address.district",
            placeholder="Enter district name"
        ),
        FormField(
            field_id="state",
            label="State",
            field_type="text",
            required=True,
            entity_mapping="address.state",
            placeholder="Enter state name"
        ),
        FormField(
            field_id="pincode",
            label="PIN Code",
            field_type="text",
            required=True,
            entity_mapping="address.pincode",
            validation={"pattern": r"^\d{6}$"},
            placeholder="6-digit PIN code"
        ),
        FormField(
            field_id="aadhaar_number",
            label="Aadhaar Number",
            field_type="text",
            required=True,
            entity_mapping="aadhaar_number",
            validation={"pattern": r"^\d{12}$"},
            placeholder="12-digit Aadhaar number"
        ),
        FormField(
            field_id="pan_number",
            label="PAN Number (if applicable)",
            field_type="text",
            required=False,
            entity_mapping="pan_number",
            validation={"pattern": r"^[A-Z]{5}\d{4}[A-Z]$"},
            placeholder="ABCDE1234Z"
        ),
        FormField(
            field_id="annual_income",
            label="Annual Income (INR)",
            field_type="number",
            required=True,
            entity_mapping=None,  # Not extracted from documents
            placeholder="Enter annual income"
        ),
        FormField(
            field_id="mobile_number",
            label="Mobile Number",
            field_type="text",
            required=True,
            entity_mapping="mobile",
            validation={"pattern": r"^\d{10}$"},
            placeholder="10-digit mobile number"
        ),
    ]
)

register_form_template(income_form)

# ============================================================================
# CASTE CERTIFICATE FORM
# ============================================================================
caste_form = FormTemplate(
    form_id="caste_certificate",
    form_name="Caste Certificate",
    description="Certificate for Scheduled Caste/Scheduled Tribe/Other Backward Classes",
    category="certificate",
    fields=[
        FormField(
            field_id="applicant_name",
            label="Applicant Full Name",
            field_type="text",
            required=True,
            entity_mapping="name",
            placeholder="Enter full name"
        ),
        FormField(
            field_id="father_name",
            label="Father's Name",
            field_type="text",
            required=True,
            entity_mapping="father_name",
            placeholder="Enter father's full name"
        ),
        FormField(
            field_id="mother_name",
            label="Mother's Name",
            field_type="text",
            required=True,
            entity_mapping="mother_name",
            placeholder="Enter mother's full name"
        ),
        FormField(
            field_id="date_of_birth",
            label="Date of Birth",
            field_type="date",
            required=True,
            entity_mapping="dob",
            placeholder="DD/MM/YYYY"
        ),
        FormField(
            field_id="gender",
            label="Gender",
            field_type="select",
            required=True,
            entity_mapping="gender",
            validation={"options": ["Male", "Female", "Other"]}
        ),
        FormField(
            field_id="caste_category",
            label="Caste Category",
            field_type="select",
            required=True,
            entity_mapping=None,
            validation={"options": ["SC", "ST", "OBC", "General"]},
            placeholder="Select category"
        ),
        FormField(
            field_id="caste_name",
            label="Caste Name",
            field_type="text",
            required=True,
            entity_mapping=None,
            placeholder="Enter caste name"
        ),
        FormField(
            field_id="address_line1",
            label="Address Line 1",
            field_type="text",
            required=True,
            entity_mapping="address.line1",
            placeholder="House/Flat No., Street"
        ),
        FormField(
            field_id="city",
            label="City/Town",
            field_type="text",
            required=True,
            entity_mapping="address.city",
            placeholder="Enter city name"
        ),
        FormField(
            field_id="district",
            label="District",
            field_type="text",
            required=True,
            entity_mapping="address.district",
            placeholder="Enter district name"
        ),
        FormField(
            field_id="state",
            label="State",
            field_type="text",
            required=True,
            entity_mapping="address.state",
            placeholder="Enter state name"
        ),
        FormField(
            field_id="pincode",
            label="PIN Code",
            field_type="text",
            required=True,
            entity_mapping="address.pincode",
            validation={"pattern": r"^\d{6}$"},
            placeholder="6-digit PIN code"
        ),
        FormField(
            field_id="aadhaar_number",
            label="Aadhaar Number",
            field_type="text",
            required=True,
            entity_mapping="aadhaar_number",
            validation={"pattern": r"^\d{12}$"},
            placeholder="12-digit Aadhaar number"
        ),
        FormField(
            field_id="mobile_number",
            label="Mobile Number",
            field_type="text",
            required=True,
            entity_mapping="mobile",
            validation={"pattern": r"^\d{10}$"},
            placeholder="10-digit mobile number"
        ),
    ]
)

register_form_template(caste_form)

# ============================================================================
# BIRTH CERTIFICATE APPLICATION FORM
# ============================================================================
birth_certificate_form = FormTemplate(
    form_id="birth_certificate",
    form_name="Birth Certificate Application",
    description="Application for Birth Certificate",
    category="certificate",
    fields=[
        FormField(
            field_id="child_name",
            label="Child's Full Name",
            field_type="text",
            required=True,
            entity_mapping="name",
            placeholder="Enter child's full name"
        ),
        FormField(
            field_id="date_of_birth",
            label="Date of Birth",
            field_type="date",
            required=True,
            entity_mapping="dob",
            placeholder="DD/MM/YYYY"
        ),
        FormField(
            field_id="gender",
            label="Gender",
            field_type="select",
            required=True,
            entity_mapping="gender",
            validation={"options": ["Male", "Female", "Other"]}
        ),
        FormField(
            field_id="father_name",
            label="Father's Full Name",
            field_type="text",
            required=True,
            entity_mapping="father_name",
            placeholder="Enter father's full name"
        ),
        FormField(
            field_id="mother_name",
            label="Mother's Full Name",
            field_type="text",
            required=True,
            entity_mapping="mother_name",
            placeholder="Enter mother's full name"
        ),
        FormField(
            field_id="place_of_birth",
            label="Place of Birth",
            field_type="text",
            required=True,
            entity_mapping="address.city",
            placeholder="Hospital/City name"
        ),
        FormField(
            field_id="address_line1",
            label="Address Line 1",
            field_type="text",
            required=True,
            entity_mapping="address.line1",
            placeholder="House/Flat No., Street"
        ),
        FormField(
            field_id="city",
            label="City/Town",
            field_type="text",
            required=True,
            entity_mapping="address.city",
            placeholder="Enter city name"
        ),
        FormField(
            field_id="district",
            label="District",
            field_type="text",
            required=True,
            entity_mapping="address.district",
            placeholder="Enter district name"
        ),
        FormField(
            field_id="state",
            label="State",
            field_type="text",
            required=True,
            entity_mapping="address.state",
            placeholder="Enter state name"
        ),
        FormField(
            field_id="pincode",
            label="PIN Code",
            field_type="text",
            required=True,
            entity_mapping="address.pincode",
            validation={"pattern": r"^\d{6}$"},
            placeholder="6-digit PIN code"
        ),
        FormField(
            field_id="aadhaar_number",
            label="Aadhaar Number (if available)",
            field_type="text",
            required=False,
            entity_mapping="aadhaar_number",
            validation={"pattern": r"^\d{12}$"},
            placeholder="12-digit Aadhaar number"
        ),
        FormField(
            field_id="mobile_number",
            label="Mobile Number",
            field_type="text",
            required=True,
            entity_mapping="mobile",
            validation={"pattern": r"^\d{10}$"},
            placeholder="10-digit mobile number"
        ),
    ]
)

register_form_template(birth_certificate_form)





