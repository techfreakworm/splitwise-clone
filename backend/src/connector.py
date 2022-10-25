from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connector:
    def __init__(self,endpoint,echo=True,future=True):
        self.db_endpoint = endpoint
        self.db_session = None
        self.db_engine = None
        self.db_echo = echo
        self.db_future = future

        self.__create_engine()
        self.__create_splitwise_db_session_engine()


    def __create_engine(self):
        self.db_engine = create_engine(
            # 'mysql+pymysql://user:password@host:3600/database',
            self.db_endpoint,
            echo=self.db_echo,
            future=self.db_engine
        )

    def __create_splitwise_db_session_engine(self):
        Session = sessionmaker(bind=self.db_engine)
        self.db_session = Session()


    