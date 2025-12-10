"""Builder pattern implementation."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Optional

T = TypeVar("T")


class Builder(ABC, Generic[T]):
    """Abstract builder interface for constructing complex objects.

    Usage:
        class QueryBuilder(Builder[str]):
            def __init__(self) -> None:
                self._parts: list[str] = []

            def select(self, columns: str) -> 'QueryBuilder':
                self._parts.append(f"SELECT {columns}")
                return self

            def build(self) -> str:
                return " ".join(self._parts)
    """

    @abstractmethod
    def build(self) -> T:
        """Build and return the final object.

        Returns:
            Constructed object of type T
        """
        pass

    def reset(self) -> "Builder[T]":
        """Reset the builder to initial state.

        Returns:
            Self for method chaining
        """
        return self


class QueryBuilder:
    """Builder for constructing SQL queries.

    Example:
        query = (QueryBuilder()
            .select("*")
            .from_table("users")
            .where("age > ?")
            .build())
    """

    def __init__(self) -> None:
        """Initialize query builder."""
        self._select: Optional[str] = None
        self._from_table: Optional[str] = None
        self._where_conditions: list[str] = []
        self._joins: list[str] = []
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None

    def select(self, columns: str) -> "QueryBuilder":
        """Set SELECT clause.

        Args:
            columns: Column names to select

        Returns:
            Self for method chaining
        """
        self._select = columns
        return self

    def from_table(self, table: str) -> "QueryBuilder":
        """Set FROM clause.

        Args:
            table: Table name

        Returns:
            Self for method chaining
        """
        self._from_table = table
        return self

    def where(self, condition: str) -> "QueryBuilder":
        """Add WHERE condition.

        Args:
            condition: WHERE condition

        Returns:
            Self for method chaining
        """
        self._where_conditions.append(condition)
        return self

    def join(self, table: str, on: str) -> "QueryBuilder":
        """Add JOIN clause.

        Args:
            table: Table to join
            on: JOIN condition

        Returns:
            Self for method chaining
        """
        self._joins.append(f"JOIN {table} ON {on}")
        return self

    def order_by(self, column: str, ascending: bool = True) -> "QueryBuilder":
        """Add ORDER BY clause.

        Args:
            column: Column to order by
            ascending: Whether to sort ascending

        Returns:
            Self for method chaining
        """
        direction = "ASC" if ascending else "DESC"
        self._order_by = f"{column} {direction}"
        return self

    def limit(self, count: int) -> "QueryBuilder":
        """Set LIMIT clause.

        Args:
            count: Maximum number of rows

        Returns:
            Self for method chaining
        """
        self._limit = count
        return self

    def build(self) -> str:
        """Build the SQL query string.

        Returns:
            SQL query string

        Raises:
            ValueError: If query is incomplete
        """
        if not self._select or not self._from_table:
            raise ValueError("SELECT and FROM clauses are required")

        parts = [f"SELECT {self._select}", f"FROM {self._from_table}"]

        if self._joins:
            parts.extend(self._joins)

        if self._where_conditions:
            where_clause = " AND ".join(self._where_conditions)
            parts.append(f"WHERE {where_clause}")

        if self._order_by:
            parts.append(f"ORDER BY {self._order_by}")

        if self._limit:
            parts.append(f"LIMIT {self._limit}")

        return " ".join(parts)

    def reset(self) -> "QueryBuilder":
        """Reset builder to initial state.

        Returns:
            Self for method chaining
        """
        self._select = None
        self._from_table = None
        self._where_conditions = []
        self._joins = []
        self._order_by = None
        self._limit = None
        return self

