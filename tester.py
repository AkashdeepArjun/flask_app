from app import db  # or: from database import db

# 1. Print the exact database Flask is connected to
print("CONNECTED DB:", db.engine.url)

# 2. Wipe the ghost revision and clear the table
db.session.execute(db.text("DROP TABLE IF EXISTS alembic_version;"))
db.session.execute(db.text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL, PRIMARY KEY (version_num));"))
db.session.commit()

print("ALEMBIC TABLE WIPED SUCCESSFULLY!")
exit()