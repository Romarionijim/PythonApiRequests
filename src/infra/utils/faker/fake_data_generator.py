from faker import Faker


class FakeDataGenerator:
    faker = Faker()

    @classmethod
    def get_random_male_first_name(cls) -> str:
        first_name = cls.faker.name_male()
        return first_name

    @classmethod
    def get_random_female_last_name(cls) -> str:
        female_first_name = cls.faker.name_female()
        return female_first_name

    @classmethod
    def get_Random_last_name(cls) -> str:
        last_name = cls.faker.last_name()
        return last_name

    @classmethod
    def get_random_number(cls) -> int:
        random_int = cls.faker.random_int(min=3000, max=5000)
        return random_int

    @classmethod
    def get_random_email(cls) -> str:
        random_email = cls.faker.company_email()
        return random_email
