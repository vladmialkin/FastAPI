from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:919@localhost/fast_api_bd", echo=True,)
engine.connect()

