from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from PIL import Image
import pytesseract
import io
import tempfile
import os
import traceback

# Try to import pdf2image for PDF support
try:
    from pdf2image import convert_from_bytes
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# Import entity extractor
from entity_extractor import extract_entities
# Import document-specific extractors
try:
    from document_extractors import extract_document_entities, detect_document_type
    DOCUMENT_EXTRACTORS_AVAILABLE = True
except ImportError:
    DOCUMENT_EXTRACTORS_AVAILABLE = False

# Import form mapping
from form_templates import get_all_form_templates, get_form_template
from form_mapper import map_entities_to_form, get_mapping_suggestions, update_form_field, get_form_preview

# Import PDF generator
try:
    from pdf_generator import generate_filled_form_pdf
    PDF_GENERATOR_AVAILABLE = True
except ImportError:
    PDF_GENERATOR_AVAILABLE = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORTANT: set this to your actual tesseract.exe path if different
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler path configuration (for PDF processing)
# Set this to your Poppler bin directory if not in PATH
# Common Windows locations:
# - C:\poppler\Library\bin
# - C:\Program Files\poppler\bin
# - C:\Users\<username>\poppler\bin
POPPLER_PATH = os.environ.get("POPPLER_PATH", None)  # Can be set via environment variable
# Uncomment and set if Poppler is not in PATH:
POPPLER_PATH = r"C:\Users\Admin\seva-assistant\Release-24.02.0-0\poppler-24.02.0\Library\bin"

# Try to auto-detect Poppler in common locations if not in PATH
if not POPPLER_PATH and PDF_SUPPORT:
    common_poppler_paths = [
        r"C:\poppler\Library\bin",
        r"C:\Program Files\poppler\bin",
        r"C:\Program Files (x86)\poppler\bin",
    ]
    for path in common_poppler_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, "pdftoppm.exe")):
            POPPLER_PATH = path
            break

# Supported languages mapping
SUPPORTED_LANGUAGES = {
    "english": "eng",
    "hindi": "hin",
    "marathi": "mar",
    "tamil": "tam",
    "telugu": "tel",
    "gujarati": "guj",
}

def get_tesseract_lang(language: str = "english") -> str:
    """
    Get Tesseract language code from language name.
    Supports multiple languages by combining codes (e.g., "eng+hin")
    """
    lang_code = SUPPORTED_LANGUAGES.get(language.lower(), "eng")
    
    # For Indian documents, often have English labels with regional language content
    # So we combine English with the selected language
    if language.lower() != "english":
        return f"eng+{lang_code}"
    return lang_code

@app.get("/")
def root():
    """
    Root endpoint - API information
    """
    return {
        "name": "Seva Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "languages": "/languages",
            "process_document": "/process/document",
            "process_and_map": "/process-and-map",
            "extract_entities": "/extract-entities",
            "get_forms": "/forms",
            "get_form": "/forms/{form_id}",
            "map_form": "/forms/map",
            "generate_pdf": "/forms/generate-pdf",
        },
        "docs": "/docs",
        "openapi_schema": "/openapi.json"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/languages")
def get_supported_languages():
    """
    Get list of supported languages for OCR
    """
    return {
        "languages": list(SUPPORTED_LANGUAGES.keys()),
        "language_codes": SUPPORTED_LANGUAGES,
        "default": "english"
    }

# Test endpoint for entity extraction (useful for debugging)
class TextInput(BaseModel):
    text: str

@app.post("/extract-entities")
async def extract_entities_endpoint(input_data: TextInput) -> Dict[str, Any]:
    """
    Test endpoint to extract entities from plain text.
    Useful for testing entity extraction without OCR.
    """
    entities = extract_entities(input_data.text)
    return {
        "input_text": input_data.text,
        "extracted_entities": entities,
    }

@app.post("/process/document")
async def process_document(
    file: UploadFile = File(...),
    language: str = "english"
) -> Dict[str, Any]:
    try:
        # Read file into memory
        content = await file.read()
        filename = file.filename or "unknown"
        
        # Determine file type
        content_type = file.content_type or ""
        is_pdf = content_type == "application/pdf" or filename.lower().endswith(".pdf")
        is_image = content_type.startswith("image/") or filename.lower().endswith((".jpg", ".jpeg", ".png"))
        
        if not is_pdf and not is_image:
            raise HTTPException(
                status_code=400, 
                detail="Only PDF, JPEG, and PNG files are supported"
            )
        
        text = ""
        pages_processed = 1
        
        if is_pdf:
            if not PDF_SUPPORT:
                raise HTTPException(
                    status_code=500,
                    detail="PDF support requires pdf2image library. Install it with: pip install pdf2image"
                )
            
            try:
                # Convert PDF pages to images
                # Use poppler_path if specified, otherwise rely on PATH
                if POPPLER_PATH:
                    images = convert_from_bytes(content, dpi=300, poppler_path=POPPLER_PATH)
                else:
                    images = convert_from_bytes(content, dpi=300)
                pages_processed = len(images)
                
                # Run OCR on each page
                lang_code = get_tesseract_lang(language)
                all_text = []
                for i, image in enumerate(images):
                    try:
                        page_text = pytesseract.image_to_string(image, lang=lang_code)
                    except Exception as lang_error:
                        # Fallback to English if language pack not installed
                        print(f"Warning: Language {language} not available, falling back to English. Error: {lang_error}")
                        page_text = pytesseract.image_to_string(image, lang="eng")
                    if page_text.strip():
                        all_text.append(f"--- Page {i+1} ---\n{page_text}")
                
                text = "\n\n".join(all_text)
                
            except Exception as e:
                error_msg = str(e)
                if "poppler" in error_msg.lower() or "PDFInfoNotInstalledError" in str(type(e)):
                    poppler_instructions = """
Poppler is not installed or not found in PATH. To fix this:

OPTION 1 - Install Poppler and add to PATH:
1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the zip file to a location like C:\\poppler
3. Add C:\\poppler\\Library\\bin to your system PATH
4. Restart your terminal/IDE

OPTION 2 - Set POPPLER_PATH in code:
1. Download Poppler from the link above
2. Extract to a location like C:\\poppler
3. In backend/main.py, uncomment and set:
   POPPLER_PATH = r"C:\\poppler\\Library\\bin"

OPTION 3 - Set environment variable:
   set POPPLER_PATH=C:\\poppler\\Library\\bin
"""
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error processing PDF: {error_msg}\n\n{poppler_instructions}"
                    )
                else:
                    error_trace = traceback.format_exc()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error processing PDF: {error_msg}\nTraceback: {error_trace}"
                    )
        
        else:
            # Handle image files (JPEG, PNG)
            try:
                image = Image.open(io.BytesIO(content))
                lang_code = get_tesseract_lang(language)
                try:
                    text = pytesseract.image_to_string(image, lang=lang_code)
                except Exception as lang_error:
                    # Fallback to English if language pack not installed
                    print(f"Warning: Language {language} not available, falling back to English. Error: {lang_error}")
                    text = pytesseract.image_to_string(image, lang="eng")
            except Exception as e:
                error_trace = traceback.format_exc()
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing image: {str(e)}\nTraceback: {error_trace}"
                )

        # Extract entities from OCR text
        # Use document-specific extractor if available, otherwise use generic extractor
        if DOCUMENT_EXTRACTORS_AVAILABLE:
            entities = extract_document_entities(text)
            doc_type = detect_document_type(text)
        else:
            entities = extract_entities(text)
            doc_type = "unknown"
        
        return {
            "filename": filename,
            "file_type": "PDF" if is_pdf else "Image",
            "document_type": doc_type if DOCUMENT_EXTRACTORS_AVAILABLE else "unknown",
            "ocr_text": text,
            "pages_processed": pages_processed,
            "extracted_entities": entities,
            "language_used": language,
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any other unexpected errors
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}\nTraceback: {error_trace}"
        )

# ============================================================================
# FORM MAPPING ENDPOINTS
# ============================================================================

@app.get("/forms", response_model=Dict[str, Any])
async def get_forms(language: str = "english") -> Dict[str, Any]:
    """
    Get all available form templates
    
    Query parameters:
    - language: Language code for form labels (default: "english")
    
    Returns a list of all available government form templates with their fields and configurations.
    """
    templates = get_all_form_templates(language)
    return {
        "forms": templates,
        "total": len(templates),
        "language": language
    }

@app.get("/forms/{form_id}")
async def get_form(form_id: str, language: str = "english"):
    """
    Get a specific form template by ID
    
    Query parameters:
    - language: Language code for form labels (default: "english")
    """
    form_template = get_form_template(form_id)
    if not form_template:
        raise HTTPException(status_code=404, detail=f"Form '{form_id}' not found")
    return form_template.to_dict(language)

class MapFormRequest(BaseModel):
    entities: Dict[str, Any]
    form_id: str
    language: str = "english"

@app.post("/forms/map")
async def map_form_to_entities(request: MapFormRequest) -> Dict[str, Any]:
    """
    Map extracted entities to a form template
    
    Request body:
    {
        "entities": {...},  // Extracted entities from entity_extractor
        "form_id": "domicile_certificate",  // Form template ID
        "language": "english"  // Language code for form labels (optional, default: "english")
    }
    """
    try:
        mapped_form = map_entities_to_form(request.entities, request.form_id, request.language)
        suggestions = get_mapping_suggestions(request.entities, request.form_id, request.language)
        
        return {
            "mapped_form": mapped_form,
            "suggestions": suggestions,
            "preview": get_form_preview(mapped_form),
            "language": request.language
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error mapping form: {str(e)}\nTraceback: {error_trace}"
        )

class ProcessAndMapRequest(BaseModel):
    form_id: str

@app.post("/process-and-map")
async def process_document_and_map(
    file: UploadFile = File(...),
    form_id: str = "domicile_certificate",
    language: str = "english"
) -> Dict[str, Any]:
    """
    Process document (OCR + Entity Extraction) and map to form in one step
    
    Query parameters:
    - form_id: Form template ID (default: "domicile_certificate")
    """
    try:
        # Read file into memory
        content = await file.read()
        filename = file.filename or "unknown"
        
        # Determine file type
        content_type = file.content_type or ""
        is_pdf = content_type == "application/pdf" or filename.lower().endswith(".pdf")
        is_image = content_type.startswith("image/") or filename.lower().endswith((".jpg", ".jpeg", ".png"))
        
        if not is_pdf and not is_image:
            raise HTTPException(
                status_code=400, 
                detail="Only PDF, JPEG, and PNG files are supported"
            )
        
        text = ""
        pages_processed = 1
        
        if is_pdf:
            if not PDF_SUPPORT:
                raise HTTPException(
                    status_code=500,
                    detail="PDF support requires pdf2image library. Install it with: pip install pdf2image"
                )
            
            try:
                # Use poppler_path if specified, otherwise rely on PATH
                if POPPLER_PATH:
                    images = convert_from_bytes(content, dpi=300, poppler_path=POPPLER_PATH)
                else:
                    images = convert_from_bytes(content, dpi=300)
                pages_processed = len(images)
                lang_code = get_tesseract_lang(language)
                all_text = []
                for i, image in enumerate(images):
                    try:
                        page_text = pytesseract.image_to_string(image, lang=lang_code)
                    except Exception as lang_error:
                        # Fallback to English if language pack not installed
                        print(f"Warning: Language {language} not available, falling back to English. Error: {lang_error}")
                        page_text = pytesseract.image_to_string(image, lang="eng")
                    if page_text.strip():
                        all_text.append(f"--- Page {i+1} ---\n{page_text}")
                text = "\n\n".join(all_text)
            except Exception as e:
                error_msg = str(e)
                if "poppler" in error_msg.lower() or "PDFInfoNotInstalledError" in str(type(e)):
                    poppler_instructions = """
Poppler is not installed or not found in PATH. To fix this:

OPTION 1 - Install Poppler and add to PATH:
1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the zip file to a location like C:\\poppler
3. Add C:\\poppler\\Library\\bin to your system PATH
4. Restart your terminal/IDE

OPTION 2 - Set POPPLER_PATH in code:
1. Download Poppler from the link above
2. Extract to a location like C:\\poppler
3. In backend/main.py, uncomment and set:
   POPPLER_PATH = r"C:\\poppler\\Library\\bin"

OPTION 3 - Set environment variable:
   set POPPLER_PATH=C:\\poppler\\Library\\bin
"""
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error processing PDF: {error_msg}\n\n{poppler_instructions}"
                    )
                else:
                    error_trace = traceback.format_exc()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error processing PDF: {error_msg}\nTraceback: {error_trace}"
                    )
        else:
            try:
                image = Image.open(io.BytesIO(content))
                lang_code = get_tesseract_lang(language)
                try:
                    text = pytesseract.image_to_string(image, lang=lang_code)
                except Exception as lang_error:
                    # Fallback to English if language pack not installed
                    print(f"Warning: Language {language} not available, falling back to English. Error: {lang_error}")
                    text = pytesseract.image_to_string(image, lang="eng")
            except Exception as e:
                error_trace = traceback.format_exc()
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing image: {str(e)}\nTraceback: {error_trace}"
                )

        # Extract entities
        # Use document-specific extractor if available, otherwise use generic extractor
        if DOCUMENT_EXTRACTORS_AVAILABLE:
            entities = extract_document_entities(text)
            doc_type = detect_document_type(text)
        else:
            entities = extract_entities(text)
            doc_type = "unknown"
        
        # Map to form (using language parameter for form labels)
        mapped_form = map_entities_to_form(entities, form_id, language)
        suggestions = get_mapping_suggestions(entities, form_id, language)
        
        return {
            "filename": filename,
            "file_type": "PDF" if is_pdf else "Image",
            "document_type": doc_type if DOCUMENT_EXTRACTORS_AVAILABLE else "unknown",
            "ocr_text": text,
            "pages_processed": pages_processed,
            "extracted_entities": entities,
            "mapped_form": mapped_form,
            "suggestions": suggestions,
            "preview": get_form_preview(mapped_form),
            "language_used": language,
        }
    except HTTPException:
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}\nTraceback: {error_trace}"
        )

# ============================================================================
# PDF GENERATION ENDPOINT
# ============================================================================

class PdfRequest(BaseModel):
    mapped_form: Dict[str, Any]

@app.post("/forms/generate-pdf")
async def generate_pdf_endpoint(request: PdfRequest):
    """
    Generate a filled PDF from mapped form data.

    Body:
    {
      "mapped_form": { ... }  // use mapped_form from /forms/map or /process-and-map
    }
    """
    if not PDF_GENERATOR_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation requires reportlab library. Install it with: pip install reportlab"
        )
    
    try:
        pdf_bytes = generate_filled_form_pdf(request.mapped_form)

        form_name = request.mapped_form.get("form_name", "filled_form").replace(" ", "_")
        filename = f"{form_name}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            },
        )
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF: {str(e)}\nTraceback: {error_trace}"
        )
