1. Project Structure & Layers
Organize the repo into distinct folders that reflect responsibility. A typical layout:

bash
Copy
my_project/
├── src/
│   ├── domain/               # Core business logic & entities
│   │   ├── models.py
│   │   ├── services.py
│   │   └── __init__.py
│   ├── application/          # Use‐cases, orchestrators, DTOs
│   │   ├── interfaces.py     # Abstract interfaces (e.g., VectorStore)
│   │   ├── use_cases.py
│   │   └── __init__.py
│   ├── infrastructure/       # Concrete implementations, external I/O
│   │   ├── vectorstores/     # Different backends (e.g., FAISS, Pinecone)
│   │   │   ├── __init__.py
│   │   │   ├── faiss_store.py
│   │   │   └── pinecone_store.py
│   │   ├── persistence.py    # DB adapters, file I/O, etc.
│   │   └── __init__.py
│   ├── presentation/         # CLI or REST controllers (e.g., FastAPI routers)
│   │   ├── cli.py
│   │   └── __init__.py
│   ├── config/               # Configuration, environment variables, constants
│   │   ├── constants.py
│   │   └── settings.py
│   ├── tests/                # Unit/integration tests mirroring src/ structure
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   └── __init__.py
├── requirements.txt
├── setup.py                  # If packaging, or pyproject.toml
└── README.md
domain/ holds pure business objects and rules, with no external dependencies.

application/ defines abstract interfaces (e.g., VectorStoreInterface) and use‐case functions that orchestrate domain objects.

infrastructure/ provides concrete classes that implement those interfaces (e.g., FaissVectorStore(VectorStoreInterface), PineconeVectorStore(VectorStoreInterface)).

presentation/ adapts I/O (CLI, API) into calls to the application layer.

config/constants.py defines all “magic values” (timeouts, default filenames, default parameters, environment keys), named in UPPER_SNAKE_CASE.

tests/ mirrors the same package hierarchy to keep unit tests co‐located (e.g., tests/infrastructure/test_faiss_store.py).

2. Interface & Abstraction Layer Patterns
Use Abstract Base Classes (ABCs) for Swappable Components

In application/interfaces.py, declare something like:

python
Copy
from abc import ABC, abstractmethod
from typing import List
from domain.models import Vector, Document

class VectorStoreInterface(ABC):
    @abstractmethod
    def index(self, docs: List[Document]) -> None:
        """Add documents to the vector index."""
        ...

    @abstractmethod
    def query(self, embedding: Vector, top_k: int) -> List[Document]:
        """Return top_k documents most similar to embedding."""
        ...
Any layer that needs to index/query vectors depends on VectorStoreInterface, not on a concrete class.

Dependency Injection via Constructors or Factories

In your use‐case classes (e.g., application/use_cases.py), accept the interface in the constructor:

python
Copy
class DocumentSearchService:
    def __init__(self, vs: VectorStoreInterface):
        self._vector_store = vs

    def search(self, query_embedding: Vector, top_k: int) -> List[Document]:
        return self._vector_store.query(query_embedding, top_k)
In a “Composition Root” (e.g., inside presentation/cli.py or a FastAPI startup event), instantiate FaissVectorStore or PineconeVectorStore and pass it in.

Keep Layers Strictly Separate

Domain must not import from infrastructure.

Application can import domain and application/interfaces, but not infrastructure.

Infrastructure implements interfaces from application but never uses domain’s business logic directly (only through models).

Presentation ties together application and infrastructure but does not embed core business logic.

3. Configuration & “Magic” Values
Define All Constants in One Place

Create config/constants.py. Example contents:

python
Copy
# Vector store defaults
DEFAULT_VECTOR_DIMENSION: int = 512
DEFAULT_TOP_K: int = 5

# Pinecone
PINECONE_API_KEY_ENV: str = "PINECONE_API_KEY"
PINECONE_ENV_ENV: str = "PINECONE_ENVIRONMENT"

# File paths
CORPUS_DIR: str = "/data/corpus"
INDEX_DIR: str = "/data/index"
Import these constants wherever needed. Never hard‐code a number or string inside functions.

Use Environment or Settings Module for Runtime Configuration

In config/settings.py, read from environment or a .env file:

python
Copy
import os

from config.constants import PINECONE_API_KEY_ENV, PINECONE_ENV_ENV

PINECONE_API_KEY: str = os.getenv(PINECONE_API_KEY_ENV, "")
PINECONE_ENVIRONMENT: str = os.getenv(PINECONE_ENV_ENV, "")
Do not sprinkle os.getenv(...) throughout; centralize it here.

4. Naming Conventions & Code Style
PEP 8 line length of 79 characters (docstrings can be 72).

Snake_case for functions, variables, modules, and filenames (my_module.py).

PascalCase for class names (class VectorStoreBase).

UPPER_SNAKE_CASE for constants (DEFAULT_TIMEOUT_SECONDS).

private attributes/methods prefixed with a single underscore (_cache, _compute_similarity).

Explicit Imports, no wildcard (from application.interfaces import VectorStoreInterface).

5. Dependency Management & Virtual Environments
Maintain a requirements.txt or pyproject.toml with pinned versions for reproducibility.

Use a venv or poetry to isolate dependencies.

Separate dependencies into:

production (core libs: numpy, scikit‐learn, etc.)

dev (pytest, black, flake8, mypy, pre-commit)

6. Type Hinting & Static Analysis
Type‐hint every function signature (parameters + return).

python
Copy
from typing import List

def compute_similarity(vec_a: Vector, vec_b: Vector) -> float:
    ...
Use mypy (or pyright) as part of CI to catch mismatches.

Favor TypedDict or dataclass for structured data in domain models:

python
Copy
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Document:
    id: str
    text: str
    embedding: List[float]
Where possible, mark methods as returning None explicitly (-> None).

7. Logging & Error Handling
Use the Standard logging Module

In each module, define a logger at the top:

python
Copy
import logging

logger = logging.getLogger(__name__)
Don’t print directly; use logger.debug(), logger.info(), logger.warning(), logger.error().

Configure a root logger in presentation or a main.py, setting a default level (e.g., INFO) and handlers (console, file).

Custom Exception Classes

Define a base exception in domain/exceptions.py:

python
Copy
class DomainError(Exception):
    """Base exception for domain layer errors."""
    ...
Raise domain‐specific errors (e.g., EntityNotFoundError) rather than generic ValueError.

Catch only at boundary layers (e.g., in presentation) to translate into HTTP codes or CLI exit codes.

8. Documentation & Docstrings
Module‐level docstrings at top of each .py explaining purpose.

Class docstrings briefly stating what it represents and any invariants.

Method docstrings in either Google or NumPy style, e.g.:

python
Copy
def index(self, docs: List[Document]) -> None:
    """
    Index a list of documents for future similarity queries.

    Args:
        docs: A list of Document instances to be added to the index.

    Raises:
        StorageError: If the underlying store is unavailable.
    """
    ...
If your project is intended for external consumption, maintain a README.md that explains:

Project overview/architecture

Installation

Usage examples (CLI or API)

How to swap vector‐store backends (e.g., set an environment variable or pass a different class).

9. Testing Strategy
Place tests in src/tests/ mirroring each layer:

tests/domain/ for pure domain logic.

tests/application/ for use‐case flows with mocked interfaces.

tests/infrastructure/ for integration tests against a real/in‐memory store (e.g., FAISS in RAM).

Use pytest conventions: files prefixed with test_ and test functions also prefixed with test_.

Fixtures for shared setup (e.g., a temporary FAISS index directory).

Aim for 100% coverage in domain and application layers; infrastructure can be lower if relying on external libs.

Run tests in CI on every push and PR.

10. Additional Best Practices
No Magic Values

As stated, move every literal (strings, ints, floats) used more than once into config/constants.py.

Examples: default batch sizes, timeouts, directory paths.

Naming should be descriptive: MAX_SEARCH_RESULTS rather than K = 5.

Immutable Data Where Appropriate

Use @dataclass(frozen=True) for value‐objects in domain/models.py.

Avoid mutating shared data—return new objects instead.

Avoid Side Effects in Constructors

Classes should set instance variables in __init__ but not perform heavy I/O or indexing.

Provide explicit methods like connect(), index_all(), etc., instead of doing it on import or instantiation.

Keep Function Length Short (< 50 lines)

If a function grows beyond ~50 lines, split it into private helpers.

Favor Composition Over Inheritance

Instead of a monolithic BaseVectorStore with dozens of methods, define small interfaces (e.g., IndexerInterface, QueryInterface) and compose them into a concrete store.

Version Control & Pre‐commit Hooks

Enable pre-commit with hooks like black, flake8, isort.

Enforce trailing newline, no tabs, consistent formatting, import sorting.

Continuous Integration

In your CI pipeline (GitHub Actions, GitLab CI, etc.), run:

black --check

flake8

mypy

pytest --maxfail=1 --disable-warnings -q

Packaging & Distribution (if needed)

If the project will be installed as a library, include a minimal setup.py or pyproject.toml declaring your package under src/.

Use namespace packages to avoid import collisions.

Summary Checklist
Project Layout establishes clear layers: domain ↔ application ↔ infrastructure ↔ presentation.

Interfaces (ABCs) in application/interfaces.py isolate clients from concrete implementations.

Constants: no magic values—everything in config/constants.py (UPPER_SNAKE_CASE).

PEP 8 conventions everywhere: naming, imports, line length, etc.

Type hints & dataclasses for clarity and static checks.

Logging with module‐scoped loggers; custom exceptions for domain errors.

Docstrings in Google or NumPy style on all public APIs.

Tests mirroring folder structure; high coverage in pure layers.

CI hooks for formatting (black), linting (flake8), type‐checking (mypy), and test runs.