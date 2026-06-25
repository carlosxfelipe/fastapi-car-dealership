res_not_found = {"description": "Recurso não encontrado"}
res_bad_request = {"description": "Requisição inválida ou parâmetros incorretos"}

get_car_by_id_responses = {
    404: res_not_found,
    422: res_bad_request,
}

update_car_responses = {
    404: res_not_found,
    422: res_bad_request,
}

delete_car_responses = {
    404: res_not_found,
    422: res_bad_request,
}
