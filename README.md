# ACM Summer School on Generative AI for text Hackathon
Authors:-
- Somraj Gautam
- Muktinath Vishwakarma

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Run](#run)
5. [Contribution](#contribution)
6. [License](#license)

## Introduction

This project provides a comprehensive solution for processing and analyzing electoral bond data in India. It consists of two main components:

1. A PDF to CSV converter that extracts electoral bond data from PDF files and converts it into a structured CSV format.
2. A Natural Language to SQL converter that allows users to query the extracted data using natural language questions.

These tools are designed to make it easier for researchers, journalists, and citizens to access and analyze information about electoral bonds, enhancing transparency in political funding.

## Requirements

- Python 3.7+
- Required Python packages:
  - PyMuPDF (fitz) 1.18.14+
  - pandas 1.2.0+
  - groq 0.4.0+
  - pandasql 0.7.3+
  - matplotlib 3.3.0+
  - seaborn 0.11.0+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/srgautam9/ACM_school.git
   cd ACM_school
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Run
```
export GROQ_API_KEY=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
```
```
streamlit run app.py
```

## Contribution
- Somraj Gautam
- Muktinath Vishwakarma

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For any questions or issues, please open an issue on the GitHub repository or contact the project maintainers.
