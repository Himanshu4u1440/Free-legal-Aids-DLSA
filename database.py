import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dlsa.database")

Base = declarative_base()
engine = None
SessionLocal = None
ACTIVE_DB_TYPE = "Unknown"
DB_CONNECTION_INFO = ""

def init_database():
    global engine, SessionLocal, ACTIVE_DB_TYPE, DB_CONNECTION_INFO
    
    preferred_type = Config.DB_TYPE
    
    if preferred_type in ("mssql", "auto"):
        try:
            mssql_uri = Config.get_mssql_connection_string()
            logger.info(f"Attempting connection to Microsoft SQL Server at '{Config.DB_SERVER}', Database: '{Config.DB_DATABASE}'...")
            
            # Test connection with a short timeout
            test_engine = create_engine(mssql_uri, pool_pre_ping=True, pool_timeout=5)
            with test_engine.connect() as conn:
                result = conn.execute(text("SELECT @@VERSION")).scalar()
                logger.info(f"Connected to Microsoft SQL Server successfully! Version: {result[:50]}...")
            
            engine = test_engine
            ACTIVE_DB_TYPE = "Microsoft SQL Server"
            DB_CONNECTION_INFO = f"MS SQL ({Config.DB_SERVER} / {Config.DB_DATABASE})"
            
        except Exception as ex:
            if preferred_type == "mssql":
                logger.error(f"Failed to connect to required MS SQL Server: {ex}")
                raise ex
            else:
                logger.warning(f"Could not connect to local MS SQL Server ({ex}). Switching to SQLite mode for local demo/development.")
                sqlite_uri = f"sqlite:///{Config.SQLITE_DB_PATH}"
                engine = create_engine(sqlite_uri, connect_args={"check_same_thread": False})
                ACTIVE_DB_TYPE = "SQLite (Local Dev Mode - MS SQL Configured)"
                DB_CONNECTION_INFO = f"SQLite ({Config.SQLITE_DB_PATH}) [MS SQL Ready]"
    else:
        sqlite_uri = f"sqlite:///{Config.SQLITE_DB_PATH}"
        engine = create_engine(sqlite_uri, connect_args={"check_same_thread": False})
        ACTIVE_DB_TYPE = "SQLite"
        DB_CONNECTION_INFO = f"SQLite ({Config.SQLITE_DB_PATH})"

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    check_and_apply_migrations(engine)
    return engine

def check_and_apply_migrations(eng):
    if not eng:
        return
    try:
        with eng.begin() as conn:
            if "sqlite" in str(eng.url):
                cols = [row[1] for row in conn.execute(text("PRAGMA table_info(LegalAidApplications)")).fetchall()]
                if cols and "assigned_counsel_phone" not in cols:
                    conn.execute(text("ALTER TABLE LegalAidApplications ADD COLUMN assigned_counsel_phone VARCHAR(50);"))
                if cols and "last_sms_notification" not in cols:
                    conn.execute(text("ALTER TABLE LegalAidApplications ADD COLUMN last_sms_notification TEXT;"))
                if cols and "last_sms_sent_at" not in cols:
                    conn.execute(text("ALTER TABLE LegalAidApplications ADD COLUMN last_sms_sent_at DATETIME;"))

                event_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(LokAdalatEvents)")).fetchall()]
                if event_cols and "assigned_plvs" not in event_cols:
                    conn.execute(text("ALTER TABLE LokAdalatEvents ADD COLUMN assigned_plvs TEXT;"))

                # Seed initial assigned PLVs for existing default events if empty
                conn.execute(text("UPDATE LokAdalatEvents SET assigned_plvs = 'PLV Nimisha Joshi (Sr. No. 01), PLV Himanshu Parmar (Sr. No. 32)' WHERE id = 3;"))
                conn.execute(text("UPDATE LokAdalatEvents SET assigned_plvs = 'PLV Nimisha Joshi (Sr. No. 01), PLV Parth Rathod (Sr. No. 03), PLV Nidhi Mashru (Sr. No. 04)' WHERE id = 1;"))
                conn.execute(text("UPDATE LokAdalatEvents SET assigned_plvs = 'PLV Hetvi Dave (Sr. No. 05), PLV Anjali Vaghela (Sr. No. 06)' WHERE id = 2;"))

                # Keep PLVAssignments in sync with PLV status
                conn.execute(text("UPDATE PLVAssignments SET is_active = 0 WHERE plv_id IN (SELECT id FROM PLVs WHERE is_active = 0 OR status != 'Active');"))
    except Exception as e:
        logger.warning(f"Migration error: {e}")

# Initialize engine upon import
init_database()

def get_db():
    """Context manager or generator for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
