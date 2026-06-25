from uuid import UUID


class CarNotFoundError(Exception):
    def __init__(self, id: UUID):
        self.id = id
        super().__init__(f"Carro com id {id} não encontrado.")
