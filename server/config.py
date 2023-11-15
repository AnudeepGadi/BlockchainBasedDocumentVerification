from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host_domain: str
    passphrase: str
    address: str
    private_key: str
    contract_address: str
    ethereum_url: str
    ecc_curve: str
    student_public_key: str
    verifier_public_key: str
    student_private_key: str
    verifier_private_key: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env"


settings = Settings()
