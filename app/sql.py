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
            id SERIAL PRIMARY KEY,
            party_id INTEGER REFERENCES parties(id) ON DELETE NO ACTION ,
            office_id INTEGER REFERENCES offices(id) ON DELETE NO ACTION,
            user_id INTEGER REFERENCES users(id) ON DELETE NO ACTION,
            manifesto  TEXT ,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(office_id, user_id)
        );
    """,
    """CREATE TABLE IF NOT EXISTS votes(
        id SERIAL PRIMARY KEY,
        office_id INTEGER REFERENCES offices(id) ON DELETE NO ACTION,
        candidate_id INTEGER REFERENCES candidates(id) ON DELETE NO ACTION ,
        createdOn  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        createdBy INTEGER REFERENCES users(id) ON DELETE NO ACTION,
        updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (createdBy, office_id)
        );
    """,
    """CREATE TABLE IF NOT EXISTS petitions(
             id SERIAL PRIMARY KEY,
             createdOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             createdBy   INTEGER REFERENCES users(id) ON DELETE NO ACTION,
             office_id  INTEGER REFERENCES offices(id) ON DELETE NO ACTION,
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
drop_tables2 = """DROP TABLE
                users, offices,parties, candidates, votes, petitions """
