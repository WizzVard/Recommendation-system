from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

REPOSITORY_NAME = 'Recommendation-system'
USER_NAME = 'WizzVard'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit', 'numpy', 'sklearn']

setup(
    name=SRC_REPO,
    version='0.0.1',
    author=USER_NAME,
    description='A small package for Movie Recommender System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/{USER_NAME}/{REPOSITORY_NAME}',
    author_email='wizzvard22@gmail.com',
    packages=[SRC_REPO],
    python_requires='>=3.11',
    isntall_requires=LIST_OF_REQUIREMENTS
)