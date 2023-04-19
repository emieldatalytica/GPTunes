from faker import Faker

faker = Faker()


def get_random_city() -> str:
    """Get a random city.

    Returns:
        str: The random city.
    """
    return faker.city()
