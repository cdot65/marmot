from faker import Faker
import toml


def create_toml():
    """
    Creates a TOML file with unique usernames and IP addresses.

    Uses the Faker library to generate unique usernames. Each username is combined with a unique
    IP address and then written to a TOML file.
    """
    fake = Faker()

    # Create unique usernames and IP addresses
    usernames = [f"redtail\\{fake.first_name().lower()}{i}" for i in range(1, 1001)]
    ips = [f"192.168.{i//256}.{i%256}" for i in range(1, 1001)]

    # Creating logins list with usernames and IP addresses
    logins = []
    for username, ip in zip(usernames, ips):
        logins.append({"username": username, "ipaddr": ip})

    # Create users dictionary with logins
    users = {"users": {"logins": logins}}

    # Write to TOML file
    with open("settings.toml", "w") as file:
        toml.dump(users, file)


if __name__ == "__main__":
    """Main function that calls the create_toml function."""
    create_toml()
