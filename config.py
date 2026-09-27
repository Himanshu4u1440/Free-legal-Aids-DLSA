import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dlsa_portal_secure_secret_key_2026")
    
    # DB Engine selection: 'mssql', 'sqlite', or 'auto'
    DB_TYPE = os.getenv("DB_TYPE", "auto").lower()
    
    # Microsoft SQL Server Configuration
    DB_SERVER = os.getenv("DB_SERVER", "localhost")
    DB_DATABASE = os.getenv("DB_DATABASE", "DLSA_DB")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_DRIVER = os.getenv("DB_DRIVER", "SQL Server")
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes").lower() in ("yes", "true", "1")
    
    # SQLite Path
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "dlsa.db")

    @classmethod
    def get_mssql_connection_string(cls, login_timeout=3):
        """Constructs an ODBC connection string for MS SQL Server."""
        params = [
            f"DRIVER={{{cls.DB_DRIVER}}}",
            f"SERVER={cls.DB_SERVER}",
            f"DATABASE={cls.DB_DATABASE}"
        ]
        
        if cls.DB_TRUSTED_CONNECTION:
            params.append("Trusted_Connection=yes")
        else:
            if cls.DB_USER:
                params.append(f"UID={cls.DB_USER}")
            if cls.DB_PASSWORD:
                params.append(f"PWD={cls.DB_PASSWORD}")
                
        # Modern driver options
        if "17" in cls.DB_DRIVER or "18" in cls.DB_DRIVER:
            params.append("TrustServerCertificate=yes")
            
        params.append(f"LoginTimeout={login_timeout}")
        
        odbc_str = ";".join(params) + ";"
        encoded = urllib.parse.quote_plus(odbc_str)
        return f"mssql+pyodbc:///?odbc_connect={encoded}"

    @classmethod
    def get_database_uri(cls):
        """Returns the appropriate database URI."""
        if cls.DB_TYPE == "mssql":
            return cls.get_mssql_connection_string()
        elif cls.DB_TYPE == "sqlite":
            return f"sqlite:///{cls.SQLITE_DB_PATH}"
        else:
            return cls.get_mssql_connection_string()
