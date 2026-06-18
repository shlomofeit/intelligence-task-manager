from mysql import connector


class DBConnection:

    conn = None

    @classmethod
    def connect(cls):

        try:
            cls.conn = connector.connect(
                host = "localhost",
                user = "root",
                password = "1234",
                port = 3306,
                database = "Intelligence_db"
            )
        except connector.errors.ProgrammingError:
            with cls.conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db; USE Intelligence_db")
                cls.connect()

        return cls.conn
    
    @classmethod
    def get_connection(cls):
        if cls.conn and cls.conn.is_connected():
            cls.create_tabels()
            return cls.conn
        
        cls.connect()
        cls.create_tabels()
        return cls.conn
    

    @classmethod
    def create_tabels(cls):

        cursor = cls.conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS agents(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        specialty VARCHAR(50) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        completed_missions INT DEFAULT 0 NOT NULL,
        failed_missions INT DEFAULT 0 NOT NULL,
        agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
        );
                       """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions(
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        location VARCHAR(100) NOT NULL,
        difficulty INT NOT NULL CHECK (difficulty BETWEEN 0 AND 10),
        importance INT NOT NULL CHECK (importance BETWEEN 0 AND 10),
        status ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'NEW',
        risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'),
        assigned_agent_id INT
        );
                       """)

        cursor.close()


    @classmethod
    def close(cls):
        if cls.conn and cls.conn.is_connected():
            cls.conn.close()