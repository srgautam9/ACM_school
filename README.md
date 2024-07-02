# ACM Summer School on Generative AI for text Hackathon
Authors:-
- Somraj Gautam
- Muktinath Vishwakarma

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
   - [PDF to CSV Conversion](#pdf-to-csv-conversion)
   - [Natural Language to SQL Conversion](#natural-language-to-sql-conversion)
6. [Detailed Component Description](#detailed-component-description)
   - [PDF to CSV Converter](#pdf-to-csv-converter)
   - [Natural Language to SQL Converter](#natural-language-to-sql-converter)
7. [Data Schema](#data-schema)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

This project provides a comprehensive solution for processing and analyzing electoral bond data in India. It consists of two main components:

1. A PDF to CSV converter that extracts electoral bond data from PDF files and converts it into a structured CSV format.
2. A Natural Language to SQL converter that allows users to query the extracted data using natural language questions.

These tools are designed to make it easier for researchers, journalists, and citizens to access and analyze information about electoral bonds, enhancing transparency in political funding.

## Features

### PDF to CSV Converter
- Extracts data from two types of electoral bond PDFs:
  - Encashment data (details of bonds encashed by political parties)
  - Purchase data (details of bonds purchased by individuals or entities)
- Handles complex PDF layouts and tables
- Cleans and structures the extracted data
- Outputs data in CSV format for easy analysis

### Natural Language to SQL Converter
- Converts natural language queries about electoral bond data into SQL queries
- Utilizes the Groq API for advanced natural language processing
- Works with the specific schema of the electoral bond dataset
- Allows for complex queries across both encashment and purchase data

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
   git clone https://github.com/yourusername/electoral-bond-analysis.git
   cd electoral-bond-analysis
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Groq API key as an environment variable:
   ```
   export GROQ_API_KEY='your_api_key_here'
   ```
   On Windows, use `set GROQ_API_KEY=your_api_key_here`

## Usage

### PDF to CSV Conversion

1. Place your PDF files in the `data/raw` directory.
2. Run the PDF to CSV conversion scripts:
   ```
   python scripts/pdf_to_csv_encashment.py
   python scripts/pdf_to_csv_purchase.py
   ```
3. The resulting CSV files will be saved in the `data/processed` directory.

### Natural Language to SQL Conversion

1. Ensure you have the processed CSV files in the `data/processed` directory.
2. Run the Jupyter notebook or Python script for NL to SQL conversion:
   ```
   jupyter notebook notebooks/nl_to_sql_analysis.ipynb
   # or
   python scripts/nl_to_sql_query.py
   ```

3. Enter your natural language query when prompted.

## Detailed Component Description

### PDF to CSV Converter

The PDF to CSV converter uses PyMuPDF (fitz) to extract text from PDF files. It employs regular expressions to identify and parse the tabular data within the PDFs. The process involves:

1. Opening the PDF file
2. Iterating through each page
3. Extracting text content
4. Applying regex patterns to identify relevant data
5. Structuring the extracted data into a pandas DataFrame
6. Cleaning and preprocessing the data (e.g., handling date formats, converting numeric values)
7. Saving the processed data as a CSV file

Key files:
- `scripts/pdf_to_csv_encashment.py`: Processes encashment data PDFs
- `scripts/pdf_to_csv_purchase.py`: Processes purchase data PDFs

### Natural Language to SQL Converter

The NL to SQL converter uses the Groq API to translate natural language questions into SQL queries. The process involves:

1. Loading the processed CSV data into pandas DataFrames
2. Defining the schema of the data for the Groq model
3. Sending the natural language query and schema information to the Groq API
4. Receiving and parsing the SQL query response
5. Executing the SQL query on the pandas DataFrames using pandasql
6. Returning and displaying the query results

Key files:
- `scripts/nl_to_sql_query.py`: Contains the `nl_to_sql` function and query execution logic
- `notebooks/nl_to_sql_analysis.ipynb`: Jupyter notebook for interactive query analysis

## Data Schema

### Encashment Data (encash_df)
- `date_of_encashment` (INT): Day of the month when the bond was encashed
- `month_of_encashment` (INT): Month when the bond was encashed
- `year_of_encashment` (INT): Year when the bond was encashed
- `name_of_political_party` (VARCHAR): Name of the political party that encashed the bond
- `bond_number` (INT): Unique identifier for the bond
- `denominations` (DECIMAL): Face value of the bond

### Purchase Data (purchase_df)
- `date_of_purchase` (INT): Day of the month when the bond was purchased
- `month_of_purchase` (INT): Month when the bond was purchased
- `year_of_purchase` (INT): Year when the bond was purchased
- `name_of_purchaser` (VARCHAR): Name of the individual or entity that purchased the bond
- `bond_number` (INT): Unique identifier for the bond
- `denominations` (DECIMAL): Face value of the bond

## Examples

### PDF to CSV Conversion

```python
import fitz
import pandas as pd
import re

# Open the PDF file
doc = fitz.open("data/raw/sample1.pdf")

# Extract and process data
all_rows = []
row_pattern = re.compile(r'(\d+)\s+(\d{1,2}/[A-Za-z]{3}/\d{4})\s+(.*?)\s+(\*{7}\d+)\s+([A-Z]+)\s+(\d+)\s+([\d,]+)\s+(\d+)\s+(\d+)')

for page in doc:
    text = page.get_text("text")
    rows = re.findall(row_pattern, text)
    all_rows.extend(rows)

# Create DataFrame and save to CSV
df = pd.DataFrame(all_rows, columns=['Sr No', 'Date of Encashment', 'Name of the Political Party', 'Account No', 'Prefix', 'Bond Number', 'Denominations', 'Pay Branch Code', 'Pay Teller'])
df.to_csv('data/processed/encashment_data.csv', index=False)
```

### Natural Language to SQL Conversion

```python
import groq
import pandas as pd
from pandasql import sqldf

def nl_to_sql(natural_language_query):
    client = groq.Client(api_key=os.environ["GROQ_API_KEY"])
    prompt = f"""
    Convert the following natural language query to SQL:
    "{natural_language_query}"
    
    Schema:
    encash_df: date_of_encashment INT, month_of_encashment INT, year_of_encashment INT, name_of_political_party VARCHAR(255), bond_number INT, denominations DECIMAL(15, 2)
    purchase_df: date_of_purchase INT, month_of_purchase INT, year_of_purchase INT, name_of_purchaser VARCHAR(255), bond_number INT, denominations DECIMAL(15, 2)
    """
    
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are an AI assistant that converts natural language queries to SQL queries."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.1
    )
    
    return response.choices[0].message.content.strip()

# Example usage
query = "What is the total value of bonds purchased by ACROPOLIS MAINTENANCE SERVICES PRIVATE LIMITED in April 2019?"
sql_query = nl_to_sql(query)
result = sqldf(sql_query, globals())
print(result)
```

## Troubleshooting

- **PDF Extraction Issues**: If the PDF to CSV conversion is not working correctly, check that your PDF files match the expected format. You may need to adjust the regular expressions in the extraction scripts.
- **Groq API Errors**: Ensure that your Groq API key is set correctly as an environment variable. Check the Groq documentation for any API usage limits or issues.
- **SQL Query Execution Errors**: Verify that the column names in the generated SQL query match the actual column names in your DataFrames. You may need to adjust the schema information provided to the Groq model.

## Contribution
- Somraj Gautam
- Muktinath Vishwakarma

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For any questions or issues, please open an issue on the GitHub repository or contact the project maintainers.
