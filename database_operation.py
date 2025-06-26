import sqlalchemy
import pandas as pd
import urllib
import pandas as pd
from openai import AzureOpenAI
import json

endpoint = "https://aihub2565181539.openai.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"

subscription_key = "CnrQXBv16oAlU7kXdE8lXbeKVRlytn8bg55ae4fFm2wUjpz432FLJQQJ99BEAC77bzfXJ3w3AAAAACOG2x9F"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )




def query_op(user_input):
    print('db_fn has been called')
    endpoint = "https://aihub2565181539.openai.azure.com/"
    model_name = "gpt-4o"
    deployment = "gpt-4o"

    subscription_key = "CnrQXBv16oAlU7kXdE8lXbeKVRlytn8bg55ae4fFm2wUjpz432FLJQQJ99BEAC77bzfXJ3w3AAAAACOG2x9F"
    api_version = "2024-12-01-preview"

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    try:
        response = client.chat.completions.create(
            model=deployment,  # Use deployment name, not model name
            messages=[
                {"role": "system", "content": """ "You are SQL query generator, generate a sql query that select all the columns from a relating table by referring the following database architecture explanation enclosed in ++"
                    "Enclose the generated SQL query in ++"
                 "Select the columns as much as possible to which is related to the user imput, as the resulting dataframe will be processed again and all the data would be required"
                 "The SQL query will be executed in SQL server database, so functions and syntaxes known to SQL server"
                 "The SQL query should be enclosed in ++"
                 "Avoid using SQL keywords as column aliases in the query"
                 "for filtering use the same keywords used in the user input, don't assume and change the keywords in where condition"
                "the following is the database architecture, **Tables and Columns:**
                 "don't assume column names, Use only the available columns in where condition"
                    CUSTOMER: This table likely stores core customer information.

                    CUSTOMERID (likely Primary Key)
                    FIRST_NAME
                    LAST_NAME
                    DOB
                    SSN_LAST4
                    MARITAL_STATUS
                    ANNUAL_INCOME
                    PREFERRED_CONTACT
                    PHONE_NUMBER
                    EMAIL
                    ADDRESS
                    CITY
                    STATE
                    ZIP_CODE
                    HIGH_NET_WORTH_FLAG
                    LAST_LOGIN_DATE
                    FINANCIAL_GOALS
                    CLIENT_INVESTMENTS: This table stores information about specific client investments.

                    HOLDINGID (likely Primary Key)
                    CLIENTID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    INVESTMENTTYPEID (Foreign Key referencing INVESTMENT_TYPES.INVESTMENTID)
                    PRODUCTNAME
                    PRODUCTSYMBOL
                    SECTOR
                    QUANTITY
                    PURCHASEPRICE
                    MARKETPRICE
                    VALUE
                    PURCHASEDATE
                    DIVIDENDYIELD
                    RISKLEVEL
                    ASSETCLASS
                    ACCOUNTTYPE
                    BROKERNAME
                    LASTUPDATED
                    INVESTMENT_TYPES: This table defines the different types of investments.

                    INVESTMENTID (Primary Key)
                    INVESTMENTTYPE
                    DESCRIPTION
                    PRODUCTS_EXAMPLES
                    WHOBUYS
                    SYNTHETIC_BANK_TRANSACTIONS: This table stores information about bank transactions.

                    TRANSACTION_ID (Primary Key)
                    CUSTOMER_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    TRANSACTION_DATE
                    TRANSACTION_DESCRIPTION
                    TRANSACTION_AMOUNT
                    TRANSACTION_TYPE
                    BANK_NAME
                    EMAIL_CONVERSATION_DATA_CORRECTED: Stores data related to email communications.

                    EMAILID (Primary Key)
                    CUST ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    FAID (Foreign Key likely referencing FA_ADVISORS.ADVISOR_ID)
                    EMAIL
                    MEETING_NOTES_DATA: Stores notes from meetings.

                    MEETING_ID (Primary Key)
                    CLIENT_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    ADVISOR_ID (Foreign Key referencing FA_ADVISORS.ADVISOR_ID)
                    MEETING_PLATFORM
                    TRANSCRIPT_SUMMARY
                    ACTION_ITEMS
                    SENTIMENT
                    
                    PHONE_CALL_DATA: Stores data related to phone calls.

                    CALL_ID (Primary Key)
                    CLIENT_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    FA_ID (Foreign Key referencing FA_ADVISORS.ADVISOR_ID)
                    CALL_TRANSCRIPT
                    CALL_DURATION
                    KEY_POINTS
                    SENTIMENT
                    FINANCIAL_FOLLOWUPS: Stores information about financial followups with clients.

                    BRANCH_ID
                    BRANCH_OFFICER
                    FINANCIAL_ADVISOR_ID (Foreign Key referencing FA_ADVISORS.ADVISOR_ID)
                    FINANCIAL_ADVISOR_NAME
                    CLIENT_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    ENGAGEMENT_SCORE
                    FOLLOW_UP_PENDING
                    FOLLOW_UPS_COMPLETED
                    FOLLOW_UP_DATE
                    HOME_PURCHASE_DATA: Stores information about a customer's home purchase.

                    CUSTOMER_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    FIRST_NAME
                    LAST_NAME
                    ASSET_ID
                    ASSET TYPE
                    ASSET_STATUS
                    PURCHASE_DATE
                    PROPERTY_VALUE
                    MARRIAGE_STATUS_DATA: Stores marriage status change history.

                    CUSTOMER_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    FIRST_NAME
                    LAST_NAME
                    MARITAL STATUS
                    PREVIOUS_MARITAL_STATUS
                    STATUS_CHANGE_DATE
                 
                    JOB_CHANGE_DATA: Stores job change history for a customer.

                    CUSTOMER ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    FIRST_NAME
                    LAST_NAME
                    EMPLOYEE ID
                    EMPLOYER_NAME
                    JOB_TITLE
                    START_DATE
                    PREVIOUS_EMPLOYER
                    Relationships (Based on Foreign Keys)

                    FA_ADVISORS: Contains Financial Advisors data.

                    FINANCIAL_ADVISOR_ID (Foreign Key referencing CUSTOMER.CUSTOMER_ID)
                    FINANCIAL_ADVISOR_NAME
                    ROLE
                    

                    CLIENT_INVESTMENTS relates to CUSTOMER via CLIENTID. A customer can have multiple investments.
                    CLIENT_INVESTMENTS relates to INVESTMENT_TYPES via INVESTMNENTID. An investment can belong to a specific type.
                    SYNTHETIC_BANK_TRANSACTIONS relates to CUSTOMER via CUSTOMER_ID. A customer can have multiple bank transactions.
                    EMAIL_CONVERSATION_DATA_CORRECTED relates to CUSTOMER via CUST ID.
                    EMAIL_CONVERSATION_DATA_CORRECTED relates to FA_ADVISORS via FAID
                    MEETING_NOTES_DATA relates to CUSTOMER via CLIENT_ID.
                    MEETING_NOTES_DATA relates to FA_ADVISORS via ADVISOR_ID.
                    PHONE_CALL_DATA relates to CUSTOMER via CLIENT_ID.
                    PHONE_CALL_DATA relates to FA_ADVISORS via FA_ID.
                    FINANCIAL_FOLLOWUPS relates to CUSTOMER via CLIENT_ID.
                    FINANCIAL_FOLLOWUPS relates to FA_ADVISORS via FINANCIAL_ADVISOR_ID.
                    HOME_PURCHASE_DATA relates to CUSTOMER via CUSTOMER_ID.
                    MARRIAGE_STATUS_DATA relates to CUSTOMER via CUSTOMER_ID.
                    JOB_CHANGE_DATA relates to CUSTOMER via CUSTOMER_ID.

                    Consider all cloumns datatypes in varchar

                    IMPORTANT INSTRUCTION = Output only the sql query enclosed in ++
                    
                    """},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        print("Chatbot:", response.choices[0].message.content.strip())
        query = response.choices[0].message.content.strip()
        return query
        # df=db_op(query)
        # print(df)
        # print(type(df))

        # return df_fn(df,user_input)
    except Exception as e:
        print("Chatbot: Sorry, something went wrong.", str(e))
        return e

def db_op(query):
    # db_server = "sqlserverswee.database.windows.net"  # e.g., 'localhost', 'server.database.windows.net'
    # db_database = "pocdb"
    # db_username = "sqlserver" # Optional: Use None for Windows Authentication
    # db_password = "Admin!pass" # Optional: Use None for Windows Authentication
    db_server = "10.10.21.3"  # e.g., 'localhost', 'server.database.windows.net'
    db_database = "BFS-FinalcialAdvisory"
    db_username = False # Optional: Use None for Windows Authentication
    db_password =  False# Optional: Use None for Windows Authentication
    # The ODBC driver name might vary based on your installation.
    # Check your installed ODBC drivers. Common examples:
    # 'ODBC Driver 17 for SQL Server'
    # 'SQL Server Native Client 11.0'
    # 'SQL Server'
    db_driver = "ODBC Driver 17 for SQL Server" # CHANGE AS NEEDED

    # --- SQL Query ---
    # Replace with the actual query you want to run.
    query=query.replace("++","")
    sql_query = query # Example query

    # --- Connection String ---
    # Using pyodbc
    # For SQL Server Authentication:
    if db_username and db_password:
        # Quote password in case it contains special characters
        quoted_password = urllib.parse.quote_plus(db_password)
        conn_str = (
            f"mssql+pyodbc://{db_username}:{quoted_password}@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )
    # For Windows Authentication (Trusted Connection):
    else:
        conn_str = (
            f"mssql+pyodbc://@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}&trusted_connection=yes"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )

    # --- Create SQLAlchemy Engine ---
    try:
        print(f"Attempting to connect to: {db_server}/{db_database}")
        # The engine object manages connections to the database.
        engine = sqlalchemy.create_engine(conn_str)

        # Optional: Test connection (recommended)
        with engine.connect() as connection:
            print("Connection successful!")

        # --- Execute Query and Load into Pandas DataFrame ---
        print(f"\nExecuting query: {sql_query}")
        # pd.read_sql takes the SQL query and the SQLAlchemy engine (or connection)
        df = pd.read_sql(sql_query, engine)

        # --- Print the DataFrame ---
        print("\nQuery Results:")
        print(df)
        return df

    except sqlalchemy.exc.OperationalError as oe:
        print('Connection error occured')
    except sqlalchemy.exc.ProgrammingError as oe:
        print('Query error occured')
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"General SQLAlchemy error: {e}")
        return e
    except ImportError as e:
        print(f"Error: A required library is missing. {e}")
        print("Please install required libraries: pip install sqlalchemy pandas pyodbc")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return e

    finally:
        # Dispose of the engine connection pool if it was created
        if 'engine' in locals() and engine:
            engine.dispose()
            print("\nDatabase engine disposed.")

def default_db_op():
    # db_server = "sqlserverswee.database.windows.net"  # e.g., 'localhost', 'server.database.windows.net'
    # db_database = "pocdb"
    # db_username = "sqlserver" # Optional: Use None for Windows Authentication
    # db_password = "Admin!pass" # Optional: Use None for Windows Authentication
    db_server = "10.10.21.3"  # e.g., 'localhost', 'server.database.windows.net'
    db_database = "BFS-FinalcialAdvisory"
    db_username = False # Optional: Use None for Windows Authentication
    db_password =  False# Optional: Use None for Windows Authentication
    # The ODBC driver name might vary based on your installation.
    # Check your installed ODBC drivers. Common examples:
    # 'ODBC Driver 17 for SQL Server'
    # 'SQL Server Native Client 11.0'
    # 'SQL Server'
    db_driver = "ODBC Driver 17 for SQL Server" # CHANGE AS NEEDED

    # --- SQL Query ---
    # Replace with the actual query you want to run.
    query="""  SELECT * FROM CUSTOMER C 
        FULL JOIN FINANCIAL_FOLLOWUPS FF ON FF.CLIENT_ID = C.CUSTOMERID
        FULL JOIN FA_ADVISORS FA ON FA.FINANCIAL_ADVISOR_ID = FF.FINANCIAL_ADVISOR_ID
        FULL JOIN HOME_PURCHASE_DATA HPD ON HPD.CUSTOMER_ID = C.CUSTOMERID
        FULL JOIN CLIENT_INVESTMENTS CI ON CI.CLIENTID = C.CUSTOMERID
        FULL JOIN INVESTMENT_TYPES IT ON IT.INVESTMENTID = CI.INVESTMENTTYPEID
        FULL JOIN JOB_CHANGE_DATA JCD ON JCD.CUSTOMER_ID = C.CUSTOMERID
        FULL JOIN MARRIAGE_STATUS_DATA MSD ON MSD.CUSTOMER_ID = C.CUSTOMERID
        FULL JOIN SYNTHETIC_BANK_TRANSACTIONS SBT ON SBT.CUSTOMER_ID = C.CUSTOMERID """
    sql_query = query
    # --- Connection String ---
    # Using pyodbc
    # For SQL Server Authentication:
    if db_username and db_password:
        # Quote password in case it contains special characters
        quoted_password = urllib.parse.quote_plus(db_password)
        conn_str = (
            f"mssql+pyodbc://{db_username}:{quoted_password}@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )
    # For Windows Authentication (Trusted Connection):
    else:
        conn_str = (
            f"mssql+pyodbc://@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}&trusted_connection=yes"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )

    # --- Create SQLAlchemy Engine ---
    try:
        print(f"Attempting to connect to: {db_server}/{db_database}")
        # The engine object manages connections to the database.
        engine = sqlalchemy.create_engine(conn_str)

        # Optional: Test connection (recommended)
        with engine.connect() as connection:
            print("Connection successful!")

        # --- Execute Query and Load into Pandas DataFrame ---
        print(f"\nExecuting query: {sql_query}")
        # pd.read_sql takes the SQL query and the SQLAlchemy engine (or connection)
        df = pd.read_sql(sql_query, engine)

        # --- Print the DataFrame ---
        print("\nQuery Results:")
        print(df)
        return df

    except sqlalchemy.exc.OperationalError as oe:
        print('Connection error occured')
    except sqlalchemy.exc.ProgrammingError as oe:
        print('Query error occured')
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"General SQLAlchemy error: {e}")
        return e
    except ImportError as e:
        print(f"Error: A required library is missing. {e}")
        print("Please install required libraries: pip install sqlalchemy pandas pyodbc")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return e

    finally:
        # Dispose of the engine connection pool if it was created
        if 'engine' in locals() and engine:
            engine.dispose()
            print("\nDatabase engine disposed.")

def summarization_op(client_id):
    # db_server = "sqlserverswee.database.windows.net"  # e.g., 'localhost', 'server.database.windows.net'
    # db_database = "pocdb"
    # db_username = "sqlserver" # Optional: Use None for Windows Authentication
    # db_password = "Admin!pass" # Optional: Use None for Windows Authentication
    db_server = "10.10.21.3"  # e.g., 'localhost', 'server.database.windows.net'
    db_database = "BFS-FinalcialAdvisory"
    db_username = False # Optional: Use None for Windows Authentication
    db_password =  False# Optional: Use None for Windows Authentication
    # The ODBC driver name might vary based on your installation.
    # Check your installed ODBC drivers. Common examples:
    # 'ODBC Driver 17 for SQL Server'
    # 'SQL Server Native Client 11.0'
    # 'SQL Server'
    db_driver = "ODBC Driver 17 for SQL Server" # CHANGE AS NEEDED

    # --- SQL Query ---
    # Replace with the actual query you want to run.
    # if client_id:
    #     query=f"""    SELECT  C.CUSTOMERID, TRANSCRIPT_SUMMARY FROM CUSTOMER C 
    # FULL JOIN EMAIL_CONVERSATION_DATA_CORRECTED ECD ON ECD.CUST_ID = C.CUSTOMERID
    # FULL JOIN MEETING_NOTES_DATA MND ON MND.CLIENT_ID = C.CUSTOMERID
    # FULL JOIN PHONE_CALL_DATA PCD ON PCD.CLIENT_ID = C.CUSTOMERID
    # WHERE C.CUSTOMERID = '{client_id}'"""
    # else:
    #     query = """    SELECT  C.CUSTOMERID, TRANSCRIPT_SUMMARY FROM CUSTOMER C 
    # FULL JOIN EMAIL_CONVERSATION_DATA_CORRECTED ECD ON ECD.CUST_ID = C.CUSTOMERID
    # FULL JOIN MEETING_NOTES_DATA MND ON MND.CLIENT_ID = C.CUSTOMERID
    # FULL JOIN PHONE_CALL_DATA PCD ON PCD.CLIENT_ID = C.CUSTOMERID"""
    # sql_query = query
    if client_id:
        email_query = f"""SELECT * FROM EMAIL_CONVERSATION_DATA_CORRECTED WHERE CUST_ID = '{client_id}'"""
        phone_call_query = f"""SELECT * FROM PHONE_CALL_DATA WHERE CLIENT_ID = '{client_id}'"""
        meeting_notes_query = f"""SELECT * FROM MEETING_NOTES_DATA WHERE CLIENT_ID = '{client_id}'"""
    else:
        email_query = """SELECT * FROM EMAIL_CONVERSATION_DATA_CORRECTED WHERE CUST_ID = 'C0001'"""
        phone_call_query = """SELECT * FROM PHONE_CALL_DATA WHERE CLIENT_ID = 'C0001'"""
        meeting_notes_query = """SELECT * FROM MEETING_NOTES_DATA WHERE CLIENT_ID = 'C0001'"""

    
    # --- Connection String ---
    # Using pyodbc
    # For SQL Server Authentication:
    if db_username and db_password:
        # Quote password in case it contains special characters
        quoted_password = urllib.parse.quote_plus(db_password)
        conn_str = (
            f"mssql+pyodbc://{db_username}:{quoted_password}@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )
    # For Windows Authentication (Trusted Connection):
    else:
        conn_str = (
            f"mssql+pyodbc://@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}&trusted_connection=yes"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )

    # --- Create SQLAlchemy Engine ---
    try:
        print(f"Attempting to connect to: {db_server}/{db_database}")
        # The engine object manages connections to the database.
        engine = sqlalchemy.create_engine(conn_str)

        # Optional: Test connection (recommended)
        with engine.connect() as connection:
            print("Connection successful!")

        # --- Execute Query and Load into Pandas DataFrame ---
        #print(f"\nExecuting query: {sql_query}")
        # pd.read_sql takes the SQL query and the SQLAlchemy engine (or connection)
        email_df = pd.read_sql(email_query, engine)
        meeting_notes_df = pd.read_sql(meeting_notes_query, engine)
        meeting_notes_df['DATE'] = meeting_notes_df['DATE'].apply(lambda d: d.isoformat())

        
        phone_call_df = pd.read_sql(phone_call_query, engine)

        # --- Print the DataFrame ---
        payload = {
                "input_data": {
                    "client_id": "C0001",
                    "meeting_notes": meeting_notes_df.to_dict(orient='records'),
                    "emails": email_df.to_dict(orient='records'),
                    "calls": phone_call_df.to_dict(orient='records')
                }
            }
        print("\nQuery Results:")
        print(payload)
        json_str = json.dumps(payload)
        return payload

    except sqlalchemy.exc.OperationalError as oe:
        print('Connection error occured')
    except sqlalchemy.exc.ProgrammingError as qe:
        print(f"Query error occured : {qe}")
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"General SQLAlchemy error: {e}")
        return e
    except ImportError as e:
        print(f"Error: A required library is missing. {e}")
        print("Please install required libraries: pip install sqlalchemy pandas pyodbc")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return e

    finally:
        # Dispose of the engine connection pool if it was created
        if 'engine' in locals() and engine:
            engine.dispose()
            print("\nDatabase engine disposed.")

def error_log(error,err_desc):
    # db_server = "sqlserverswee.database.windows.net"  # e.g., 'localhost', 'server.database.windows.net'
    # db_database = "pocdb"
    # db_username = "sqlserver" # Optional: Use None for Windows Authentication
    # db_password = "Admin!pass" # Optional: Use None for Windows Authentication
    db_server = "10.10.21.3"  # e.g., 'localhost', 'server.database.windows.net'
    db_database = "BFS-FinalcialAdvisory"
    db_username = False # Optional: Use None for Windows Authentication
    db_password =  False# Optional: Use None for Windows Authentication
    # The ODBC driver name might vary based on your installation.
    # Check your installed ODBC drivers. Common examples:
    # 'ODBC Driver 17 for SQL Server'
    # 'SQL Server Native Client 11.0'
    # 'SQL Server'
    db_driver = "ODBC Driver 17 for SQL Server" # CHANGE AS NEEDED

    # --- Connection String ---
    # Using pyodbc
    # For SQL Server Authentication:
    if db_username and db_password:
        # Quote password in case it contains special characters
        quoted_password = urllib.parse.quote_plus(db_password)
        conn_str = (
            f"mssql+pyodbc://{db_username}:{quoted_password}@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )
    # For Windows Authentication (Trusted Connection):
    else:
        conn_str = (
            f"mssql+pyodbc://@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}&trusted_connection=yes"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )

    # --- Create SQLAlchemy Engine ---
    try:
        print(f"Attempting to connect to: {db_server}/{db_database}")
        # The engine object manages connections to the database.
        engine = sqlalchemy.create_engine(conn_str)
        insert_query = sqlalchemy.text("""
            INSERT INTO ERROR_LOG (ERROR, ERROR_DETAILS,ERROR_TIMESTAMP)
            VALUES (:error, :error_details, )
        """)

        # Data to insert
        params = {
            "error": error,
            "error_details": err_desc
        }

        # Execute the query
        with engine.connect() as conn:
            conn.execute(insert_query, params)
            conn.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"Database connection or query error: {e}")
        return e
    except ImportError as e:
        print(f"Error: A required library is missing. {e}")
        print("Please install required libraries: pip install sqlalchemy pandas pyodbc")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return e

def inference_ip(client_id):
    # db_server = "sqlserverswee.database.windows.net"  # e.g., 'localhost', 'server.database.windows.net'
    # db_database = "pocdb"
    # db_username = "sqlserver" # Optional: Use None for Windows Authentication
    # db_password = "Admin!pass" # Optional: Use None for Windows Authentication
    db_server = "10.10.21.3"  # e.g., 'localhost', 'server.database.windows.net'
    db_database = "BFS-FinalcialAdvisory"
    db_username = False # Optional: Use None for Windows Authentication
    db_password =  False# Optional: Use None for Windows Authentication
    # The ODBC driver name might vary based on your installation.
    # Check your installed ODBC drivers. Common examples:
    # 'ODBC Driver 17 for SQL Server'
    # 'SQL Server Native Client 11.0'
    # 'SQL Server'
    db_driver = "ODBC Driver 17 for SQL Server" # CHANGE AS NEEDED

    # --- SQL Query ---
    # Replace with the actual query you want to run.
    if client_id:
        query=f"""SELECT DATEDIFF(year,DOB,GETDATE()) AS age, 
                'Default' as gender,
                ANNUAL_INCOME AS income,
                'Default' AS employment_status,
                LOWER(MSD.MARITAL_STATUS) AS marital_status,
                500 AS credit_score,
                0 AS existing_loans,
                'urban' AS location,
                0 AS new_childbirth,
                0 AS job_change,
                0 AS home_purchase
                FROM CUSTOMER C
                INNER JOIN MARRIAGE_STATUS_DATA MSD ON C.CUSTOMERID = MSD.CUSTOMER_ID
                WHERE C.CUSTOMERID = 'C0001';"""
    # --- Connection String ---
    # Using pyodbc
    # For SQL Server Authentication:
    if db_username and db_password:
        # Quote password in case it contains special characters
        quoted_password = urllib.parse.quote_plus(db_password)
        conn_str = (
            f"mssql+pyodbc://{db_username}:{quoted_password}@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )
    # For Windows Authentication (Trusted Connection):
    else:
        conn_str = (
            f"mssql+pyodbc://@{db_server}/{db_database}?"
            f"driver={urllib.parse.quote_plus(db_driver)}&trusted_connection=yes"
            # Add other parameters like encrypt/trust server certificate if needed
            # f"&Encrypt=yes&TrustServerCertificate=yes"
        )

    # --- Create SQLAlchemy Engine ---
    try:
        print(f"Attempting to connect to: {db_server}/{db_database}")
        # The engine object manages connections to the database.
        engine = sqlalchemy.create_engine(conn_str)

        # Optional: Test connection (recommended)
        with engine.connect() as connection:
            print("Connection successful!")

        # --- Execute Query and Load into Pandas DataFrame ---
        print(f"\nExecuting query: {query}")
        # pd.read_sql takes the SQL query and the SQLAlchemy engine (or connection)
        df = pd.read_sql(query, engine)

        # --- Print the DataFrame ---
        print("\nQuery Results:")
        print(df)
        return df

    except sqlalchemy.exc.OperationalError as oe:
        print('Connection error occured')
    except sqlalchemy.exc.ProgrammingError as oe:
        print('Query error occured')
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"General SQLAlchemy error: {e}")
        return e
    except ImportError as e:
        print(f"Error: A required library is missing. {e}")
        print("Please install required libraries: pip install sqlalchemy pandas pyodbc")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return e

    finally:
        # Dispose of the engine connection pool if it was created
        if 'engine' in locals() and engine:
            engine.dispose()
            print("\nDatabase engine disposed.")
