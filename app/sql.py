table_create_sql = [
    """ CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                firstname  VARCHAR(55) NOT NULL,
                lastname  VARCHAR(55) NOT NULL,
                othername  VARCHAR(55),
                email TEXT UNIQUE NOT NULL,
                phoneNumber VARCHAR(15) ,
                passportUrlString TEXT NOT NULL,
                password TEXT  NOT NULL,
                isAdmin  BOOLEAN NOT NULL DEFAULT FALSE,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                
            );
     """,
    """ CREATE TABLE IF NOT EXISTS parties (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                hqAddress TEXT NOT NULL,
                logoUrl TEXT UNIQUE NOT NULL,
                slogan TEXT ,
                bio TEXT ,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
           
    """,
    """CREATE TABLE IF NOT EXISTS offices(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            type VARCHAR(100)  NOT NULL,
            description  TEXT ,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    """CREATE TABLE IF NOT EXISTS candidates(
            id SERIAL,
            party_id INTEGER REFERENCES parties(id) ON DELETE CASCADE ,
            office_id INTEGER REFERENCES offices(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
            manifesto  TEXT ,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (office_id, user_id)
        );
    """,
    """CREATE TABLE IF NOT EXISTS votes(
             id SERIAL ,  
             office_id INTEGER REFERENCES offices(id),
             candidate_id INTEGER REFERENCES candidates(id) ,
             createdOn  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             createdBy INTEGER REFERENCES users(id),
            updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (createdBy, office_id)
        );
    """,
    """CREATE TABLE IF NOT EXISTS petitions(
             id SERIAL PRIMARY KEY,  
             createdOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             createdBy   INTEGER REFERENCES users(id),
             office_id  INTEGER REFERENCES offices(id),
             body TEXT NOT NULL

             );
    """

]

drop_tables = """
            SELECT
                    'drop table if exists "' || tablename || '" cascade;' as pg_drop
            FROM
                     pg_tables
            WHERE
                    schemaname='public';
            """
