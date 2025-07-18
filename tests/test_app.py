import os
import pytest

from src.extract_ics import extract_ics_incidents
from src.preprocess import preprocess_for_langchain
from src.vector_store import create_vectorstore
from src.responder_planner import adaptive_plan_response

# Fixture: Load minimal sample data for testing
@pytest.fixture
def dummy_vcdb_entry():
    return [{
        "summary": "Unauthorized access using modbus protocol",
        "action": {"vector": "External"},
        "victim": {"employee_count": "51 to 100"},
        "timeline": {"incident": "2022-05-15"},
    }]

def test_extract_fallback():
    result = extract_ics_incidents("data/vcdb", fallback_if_empty=True)
    assert isinstance(result, list)
    assert len(result) > 0
    assert "summary" in result[0]

def test_preprocessing(dummy_vcdb_entry):
    docs = preprocess_for_langchain(dummy_vcdb_entry)
    assert isinstance(docs, list)
    assert hasattr(docs[0], 'page_content')

def test_vectorstore_building(dummy_vcdb_entry):
    docs = preprocess_for_langchain(dummy_vcdb_entry)
    vectorstore = create_vectorstore(docs)
    assert hasattr(vectorstore, 'as_retriever')

def test_responder_planner_basic():
    result = adaptive_plan_response("ransomware in ics")
    assert isinstance(result, str)
    assert "response" in result.lower() or "mitigation" in result.lower()
