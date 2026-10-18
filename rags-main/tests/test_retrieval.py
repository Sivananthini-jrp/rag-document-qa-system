
import os
from pathlib import Path

import pytest
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.embeddings import OpenAIEmbedding

from core.utils import load_data


TEST_CASES = [
    {
        "question": "Where is WynTech headquartered?",
        "expected_file": "company.pdf",
    },
    {
        "question": "When was WynTech founded?",
        "expected_file": "company.pdf",
    },
    {
        "question": "Which database does CloudReach use?",
        "expected_file": "product.pdf",
    },
    {
        "question": "Which campaign channels does CloudReach support?",
        "expected_file": "product.pdf",
    },
]


@pytest.fixture(scope="module")
def retriever():
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not configured")

    documents = load_data(
        file_names=[
            "tests/sample_docs/company.pdf",
            "tests/sample_docs/product.pdf",
        ]
    )

    context = ServiceContext.from_defaults(
        embed_model=OpenAIEmbedding(),
        chunk_size=256,
    )

    index = VectorStoreIndex.from_documents(
        documents,
        service_context=context,
    )

    return index.as_retriever(similarity_top_k=2)


@pytest.mark.parametrize("case", TEST_CASES)
def test_retrieval(retriever, case):
    results = retriever.retrieve(case["question"])

    retrieved_files = {
        Path(
            result.node.metadata.get("file_name", "")
        ).name
        for result in results
    }

    assert case["expected_file"] in retrieved_files, (
        f"Expected {case['expected_file']}, "
        f"but retrieved {retrieved_files}"
    )
