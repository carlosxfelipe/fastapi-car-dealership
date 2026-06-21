res_not_found = {"description": "Recurso não encontrado"}
res_bad_request = {"description": "Requisição inválida ou parâmetros incorretos"}

list_cars_responses: dict = {}

get_car_by_id_responses = {
    404: res_not_found,
    422: res_bad_request,
}

create_car_responses: dict = {}
