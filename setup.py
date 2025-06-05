from setuptools import setup, find_packages

setup(
    name="memexor",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "uvicorn>=0.15.0,<0.16.0",
        "python-multipart>=0.0.5",
        "openai>=0.27.0",
        "weaviate-client>=3.0.0",
        "python-dotenv>=0.19.0",
        "pydantic>=1.8.0",
        "numpy>=1.21.0",
        "langchain>=0.0.200",
    ],
) 