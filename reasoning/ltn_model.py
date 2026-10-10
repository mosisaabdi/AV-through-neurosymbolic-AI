class LTNReasoner:
    """Integration seam, not a complete LTN implementation."""
    def __init__(self, backend=None):
        self.backend = backend

    def evaluate(self, predicates, rules):
        if self.backend is None:
            raise NotImplementedError(
                "Connect the exact LTN package/version, groundings, operators, quantifiers, "
                "and aggregation used in the paper."
            )
        return self.backend.evaluate(predicates, rules)
