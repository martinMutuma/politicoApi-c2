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
            party_id INTEGER REFERENCES parties(id) ON DELETE CASCADE ,
            office_id INTEGER REFERENCES offices(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            manifesto  TEXT ,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(office_id, user_id)
        );
    """,
    """CREATE TABLE IF NOT EXISTS votes(
        id SERIAL PRIMARY KEY,
        office_id INTEGER REFERENCES offices(id) ON DELETE CASCADE,
        candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE ,
        createdOn  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        createdBy INTEGER REFERENCES users(id) ON DELETE CASCADE,
        updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (createdBy, office_id)
        );
    """,
    """CREATE TABLE IF NOT EXISTS petitions(
             id SERIAL PRIMARY KEY,
             createdOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             createdBy   INTEGER REFERENCES users(id) ON DELETE CASCADE,
             office_id  INTEGER REFERENCES offices(id) ON DELETE CASCADE,
             body TEXT NOT NULL,
             evidence TEXT NOT NULL
             );
    """,
    """DROP VIEW  IF EXISTS candidate_details CASCADE
    """,
    """DROP VIEW  IF EXISTS vote_details CASCADE
    """,
    """CREATE OR REPLACE VIEW candidate_details AS
        SELECT s.id As  candidatev_id,s.party_id,
        s.office_id  as candidate_office_id, o.name AS office_name,
        o.type AS office_type,
       CONCAT( u.firstname,' ',u.lastname,' ',u.othername) AS candidate_name,
        u.passporturlstring AS candidate_passport, u.id AS candidate_user_id
        FROM candidates s
        JOIN offices o ON  s.office_id = o.id
        JOIN users u ON  u.id = s.user_id
    """,
    """CREATE OR REPLACE VIEW vote_details as
        select v.*,d.*,u.passporturlstring as voter_passport,
        CONCAT( u.firstname,' ',u.lastname,' ',u.othername) AS voter_name
        from votes v
        join candidate_details d on d.candidatev_id = v.candidate_id
        join users u on u.id = v.createdby
    """



]

drop_tables = """
            SELECT
             'DROP TABLE IF EXISTS ' || tablename || ' cascade;' as pg_drop
            FROM
                     pg_tables
            WHERE
                    schemaname='public';
            """
drop_tables2 = """DROP TABLE
                users, offices,parties, candidates, votes, petitions cascade"""
