import random


class PersonaService:
    """
    Mocked persona provider.

    This could be replaced by
    a user profile service or ML model.
    """

    def get_persona(self, user_id: str) -> str:

        """
        Return persona for user.

        :param user_id: User identifier
        :return: Persona type
        """
        return random.choice(["NEW", "RETURNING", "POWER"])