from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:919@localhost/postgres", echo=True,)
engine.connect()







