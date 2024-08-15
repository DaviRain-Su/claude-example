# setup.py
from setuptools import setup, find_packages

setup(
    name="claude_example",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'claude_cache=claude_cache.cache:main_function',
        ],
    },
)
