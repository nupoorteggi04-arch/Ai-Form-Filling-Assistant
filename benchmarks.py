"""
Performance Benchmarks for Seva Assistant
Measures processing times and accuracy for OCR, entity extraction, and form mapping
"""

import time
import statistics
from typing import Dict, List, Any
from entity_extractor import extract_entities
from form_mapper import map_entities_to_form
from form_templates import get_all_form_templates

# Sample test data
SAMPLE_OCR_TEXTS = [
    """
    Name:- Saurabh R. Kshirsgar.
    DOB:- 02/04/1990
    
    City:- Pune
    
    Pan: abcde1234Z
    
    Adhar:- 1234 5678 9101
    """,
    """
    FULL NAME: Rajesh Kumar Sharma
    DATE OF BIRTH: 15/08/1985
    GENDER: Male
    FATHER'S NAME: Suresh Kumar Sharma
    MOTHER'S NAME: Sunita Sharma
    ADDRESS: 123 Main Street, Sector 5
    CITY: Delhi
    STATE: Delhi
    PINCODE: 110001
    MOBILE: 9876543210
    EMAIL: rajesh@example.com
    PAN NUMBER: ABCDE1234F
    AADHAAR: 1234 5678 9012
    """,
    """
    Applicant Name: Priya Patel
    Birth Date: 20/12/1995
    City: Ahmedabad
    State: Gujarat
    Pincode: 380001
    Mobile Number: 9123456789
    """,
]

SAMPLE_ENTITIES = [
    {
        "name": "Saurabh R. Kshirsgar",
        "dob": "1990-04-02",
        "date_of_birth": "1990-04-02",
        "address": {"city": "Pune"},
        "pan_number": "ABCDE1234Z",
        "aadhaar_number": "123456789101",
    },
    {
        "name": "Rajesh Kumar Sharma",
        "dob": "1985-08-15",
        "date_of_birth": "1985-08-15",
        "gender": "Male",
        "father_name": "Suresh Kumar Sharma",
        "mother_name": "Sunita Sharma",
        "address": {
            "line1": "123 Main Street, Sector 5",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110001",
        },
        "mobile": "9876543210",
        "email": "rajesh@example.com",
        "pan_number": "ABCDE1234F",
        "aadhaar_number": "123456789012",
    },
    {
        "name": "Priya Patel",
        "dob": "1995-12-20",
        "date_of_birth": "1995-12-20",
        "address": {
            "city": "Ahmedabad",
            "state": "Gujarat",
            "pincode": "380001",
        },
        "mobile": "9123456789",
    },
]


def benchmark_entity_extraction(iterations: int = 10) -> Dict[str, Any]:
    """Benchmark entity extraction performance"""
    print("=" * 60)
    print("BENCHMARK: Entity Extraction")
    print("=" * 60)
    
    times = []
    total_extracted = 0
    total_possible = 0
    
    for i, text in enumerate(SAMPLE_OCR_TEXTS, 1):
        print(f"\nTest Case {i}:")
        print(f"Text length: {len(text)} characters")
        
        case_times = []
        for iteration in range(iterations):
            start_time = time.perf_counter()
            entities = extract_entities(text)
            end_time = time.perf_counter()
            
            elapsed = (end_time - start_time) * 1000  # Convert to milliseconds
            case_times.append(elapsed)
            times.append(elapsed)
            
            # Count extracted fields
            extracted_count = sum(1 for v in entities.values() if v is not None)
            if isinstance(entities.get("address"), dict):
                extracted_count += sum(1 for v in entities["address"].values() if v is not None)
            total_extracted += extracted_count
            total_possible += 15  # Approximate max fields
        
        avg_time = statistics.mean(case_times)
        print(f"  Average time: {avg_time:.2f} ms")
        print(f"  Min time: {min(case_times):.2f} ms")
        print(f"  Max time: {max(case_times):.2f} ms")
    
    results = {
        "operation": "Entity Extraction",
        "iterations": iterations * len(SAMPLE_OCR_TEXTS),
        "average_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "total_time_ms": sum(times),
        "throughput_per_sec": (iterations * len(SAMPLE_OCR_TEXTS)) / (sum(times) / 1000),
        "extraction_rate": (total_extracted / total_possible * 100) if total_possible > 0 else 0,
    }
    
    print(f"\nOverall Results:")
    print(f"  Average: {results['average_time_ms']:.2f} ms")
    print(f"  Median: {results['median_time_ms']:.2f} ms")
    print(f"  Throughput: {results['throughput_per_sec']:.2f} operations/sec")
    print(f"  Extraction Rate: {results['extraction_rate']:.1f}%")
    
    return results


def benchmark_form_mapping(iterations: int = 10) -> Dict[str, Any]:
    """Benchmark form mapping performance"""
    print("\n" + "=" * 60)
    print("BENCHMARK: Form Mapping")
    print("=" * 60)
    
    forms = get_all_form_templates()
    times = []
    completion_rates = []
    
    for form in forms:
        form_id = form["form_id"]
        form_name = form["form_name"]
        field_count = len(form["fields"])
        
        print(f"\nForm: {form_name} ({form_id})")
        print(f"  Fields: {field_count}")
        
        form_times = []
        for entities in SAMPLE_ENTITIES:
            for iteration in range(iterations):
                start_time = time.perf_counter()
                mapped = map_entities_to_form(entities, form_id)
                end_time = time.perf_counter()
                
                elapsed = (end_time - start_time) * 1000
                form_times.append(elapsed)
                times.append(elapsed)
                
                # Calculate completion rate
                stats = mapped.get("statistics", {})
                if stats.get("total_fields", 0) > 0:
                    completion = stats.get("completion_percentage", 0)
                    completion_rates.append(completion)
        
        avg_time = statistics.mean(form_times)
        print(f"  Average time: {avg_time:.2f} ms")
    
    results = {
        "operation": "Form Mapping",
        "iterations": iterations * len(SAMPLE_ENTITIES) * len(forms),
        "average_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "total_time_ms": sum(times),
        "throughput_per_sec": (iterations * len(SAMPLE_ENTITIES) * len(forms)) / (sum(times) / 1000),
        "average_completion_rate": statistics.mean(completion_rates) if completion_rates else 0,
    }
    
    print(f"\nOverall Results:")
    print(f"  Average: {results['average_time_ms']:.2f} ms")
    print(f"  Median: {results['median_time_ms']:.2f} ms")
    print(f"  Throughput: {results['throughput_per_sec']:.2f} operations/sec")
    print(f"  Average Completion Rate: {results['average_completion_rate']:.1f}%")
    
    return results


def benchmark_end_to_end(iterations: int = 5) -> Dict[str, Any]:
    """Benchmark end-to-end processing (extraction + mapping)"""
    print("\n" + "=" * 60)
    print("BENCHMARK: End-to-End Processing")
    print("=" * 60)
    
    forms = get_all_form_templates()
    times = []
    
    for form in forms:
        form_id = form["form_id"]
        form_name = form["form_name"]
        
        print(f"\nForm: {form_name}")
        
        form_times = []
        for text in SAMPLE_OCR_TEXTS:
            for iteration in range(iterations):
                start_time = time.perf_counter()
                
                # Extract entities
                entities = extract_entities(text)
                
                # Map to form
                mapped = map_entities_to_form(entities, form_id)
                
                end_time = time.perf_counter()
                
                elapsed = (end_time - start_time) * 1000
                form_times.append(elapsed)
                times.append(elapsed)
        
        avg_time = statistics.mean(form_times)
        print(f"  Average time: {avg_time:.2f} ms")
    
    results = {
        "operation": "End-to-End Processing",
        "iterations": iterations * len(SAMPLE_OCR_TEXTS) * len(forms),
        "average_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "total_time_ms": sum(times),
        "throughput_per_sec": (iterations * len(SAMPLE_OCR_TEXTS) * len(forms)) / (sum(times) / 1000),
    }
    
    print(f"\nOverall Results:")
    print(f"  Average: {results['average_time_ms']:.2f} ms")
    print(f"  Median: {results['median_time_ms']:.2f} ms")
    print(f"  Throughput: {results['throughput_per_sec']:.2f} operations/sec")
    
    return results


def run_all_benchmarks(iterations: int = 10) -> Dict[str, Any]:
    """Run all benchmarks and return results"""
    print("\n" + "=" * 60)
    print("SEVA ASSISTANT - PERFORMANCE BENCHMARKS")
    print("=" * 60)
    print(f"Iterations per test: {iterations}")
    print(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = {}
    
    # Run benchmarks
    all_results["entity_extraction"] = benchmark_entity_extraction(iterations)
    all_results["form_mapping"] = benchmark_form_mapping(iterations)
    all_results["end_to_end"] = benchmark_end_to_end(iterations // 2)  # Fewer iterations for E2E
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Entity Extraction: {all_results['entity_extraction']['average_time_ms']:.2f} ms avg")
    print(f"Form Mapping: {all_results['form_mapping']['average_time_ms']:.2f} ms avg")
    print(f"End-to-End: {all_results['end_to_end']['average_time_ms']:.2f} ms avg")
    
    return all_results


if __name__ == "__main__":
    # Run benchmarks with 10 iterations each
    results = run_all_benchmarks(iterations=10)
    
    # Save results to file
    import json
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n[SUCCESS] Benchmarks completed! Results saved to benchmark_results.json")

