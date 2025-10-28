from setuptools import setup, find_packages

setup(
    name="google-ai-agents-hackathon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "python-multipart",
        "requests",
    ],
)

