class CarsService:
    def __init__(self):
        self._cars = [
            {
                "id": 1,
                "brand": "Toyota",
                "model": "Corolla",
            },
            {
                "id": 2,
                "brand": "Honda",
                "model": "Civic",
            },
            {
                "id": 3,
                "brand": "Jeep",
                "model": "Cherokee",
            },
        ]

    def find_all(self):
        return self._cars

    def find_one_by_id(self, id: int):
        for car in self._cars:
            if car["id"] == id:
                return car
        return None

    def create(self, brand: str, model: str):
        new_id = self._cars[-1]["id"] + 1 if self._cars else 1
        new_car = {
            "id": new_id,
            "brand": brand,
            "model": model,
        }
        self._cars.append(new_car)
        return new_car
