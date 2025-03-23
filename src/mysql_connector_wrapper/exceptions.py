class ConnectionError(Exception):
    """Exception raised for errors in the database connection"""

    pass


class QueryError(Exception):
    """Exception raised for errors in database queries."""

    pass
