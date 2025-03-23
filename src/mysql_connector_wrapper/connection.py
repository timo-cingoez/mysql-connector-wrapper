from typing import Optional, Any
import mysql.connector
from mysql.connector import errorcode
from .exceptions import ConnectionError
from .cursor import Cursor


class Connection:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        port: int,
        database: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a database connection with required and optional parameters.

        Args:
            host: The hostname or IP address of the MySQL server
            user: The username to authenticate with
            password: The password to authenticate with
            database: The database to use (optional, can connect without selecting a database)
            port: The port number of the MySQL server (default: 3306)
            **kwargs: Additional connection parameters supported by mysql.connector
        """
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            **kwargs,
        }

        if database:
            self.config["database"] = database

        self.connection = None

    def connect(self) -> None:
        """Establish a connection to the MySQL server.

        Returns:
            Self for method chaining

        Raises:
            ConnectionError: If connection fails
        """
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise ConnectionError("Invalid credentials") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise ConnectionError(
                    f"Database '{self.config.get('database')} does not exist"
                ) from err
            else:
                raise ConnectionError(f"Connection failed: {err}") from err

    def close(self) -> None:
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def cursor(self, dictionary: bool = True, **kwargs: Any) -> Cursor:
        """Get a cursor for executing queries.

        Args:
            dictionary: If True, returns rows as dictionaries (default: True)
            **kwargs: Additional cursor parameters supported by mysql.connector

        Returns:
            A cursor object

        Raises:
            ConnectionError: If not connected
        """
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Not connected to database")

        return Cursor(self.connection, dictionary=dictionary, **kwargs)

    def __enter__(self) -> "DatabaseConnection":
        """Context manager entry point."""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit point."""
        self.close()
