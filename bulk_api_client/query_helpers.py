from bulk_api_client.exceptions import InvalidQObject


class Q:
    """
    Q object that mimics the functionality of the Django Q object used to create
    a queryset. Operations happen automatically due to Python functionality. Use
    'output_filter' method to produce a dictionary containing the full chain.
    """

    AND = "and"
    OR = "or"
    NOT = "not"
    default = AND

    def __init__(self, _conn=None, _negated=False, **kwargs):
        self._conn = _conn or self.default
        self.negated = _negated
        self._children = list(kwargs.items())

    def _combine(self, object_on_right, conn):
        """
        Private combine method using self (Q) and Q object to the right,
        combining children if both contain the same operator or creating a new
        nest if the operators differ. Returns a new Q object that is the full
        chain.

        Args:
            self (Q): dict of fields columns (with alias and/or
            distinct)
            object_on_right (Q): Q object to the right of self within the chain

        Returns:
            Q object representing full chain

        """
        if not isinstance(object_on_right, Q):
            raise InvalidQObject(
                "{} must be a Q object".format(object_on_right)
            )

        if not object_on_right._children:
            return self

        elif not self._children:
            return object_on_right

        q = type(self)()
        q._conn = conn
        q.add(self, conn)
        q.add(object_on_right, conn)
        return q

    def add(self, object_on_right, conn):
        if self._conn == conn:
            if (
                object_on_right._children
                and not self.negated
                and (
                    conn == object_on_right._conn
                    or len(object_on_right._children) == 1
                )
            ):
                self._children.extend(object_on_right._children)
                return self
            else:
                self._children.append(object_on_right)
                return object_on_right
        else:
            q = type(self)()
            q._children = self._children
            q._conn = self._conn
            q.negated = self.negated

            self._conn = conn
            self._children = [q, object_on_right]

            return object_on_right

    def __and__(self, object_on_right):
        return self._combine(object_on_right, self.AND)

    def __or__(self, object_on_right):
        return self._combine(object_on_right, self.OR)

    def __eq__(self, object_on_right):
        return (
            self.__class__ == object_on_right.__class__
            and self._conn == object_on_right._conn
            and self._children == object_on_right._children
        )

    def __invert__(self):
        q = type(self)()
        q.add(self, self.NOT)
        q._negate()

        return q

    def _negate(self):
        """Negate the sense of the root connector."""
        self.negated = not self.negated

    def output_filter(self):
        """
        Creates a dictionary corresponding to the Q chain using the left-most Q
        object within the chain

        Args:
            self (Q obj)

        Returns:
            dict

        """
        return {
            self._conn: [
                c.output_filter() if isinstance(c, Q) else {c[0]: c[1]}
                for c in self._children
            ]
        }
