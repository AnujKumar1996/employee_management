from fastapi import FastAPI, status, Query
import secrets
import string
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pathlib import Path
from src.schema.employee_schema import EmployeeManagement, EmployeeManagementCreate
from fastapi import APIRouter
from src.schema.error_schema import Error404, Error500


router = APIRouter()

from typing import List, Optional


def generate_random_id():
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits
    # Generate a random length between 2 and 5
    length = secrets.randbelow(4) + 4
    # Create the random ID by choosing characters randomly
    random_id = "".join(secrets.choice(characters) for _ in range(length))
    return random_id


def create_response_json(unique_id, data_dict, file_location):
    """
    Method to write responses to json file
    """
    try:
        with open(file_location, "r") as file:
            existing_data = json.load(file)
    except Exception:
        existing_data = {}
    existing_data[unique_id] = data_dict
    try:
        with open(file_location, "w") as file:
            json.dump(existing_data, file, indent=4)
        print(f"Data for unique ID {unique_id} has been written to {file_location}")
    except Exception as e:
        print(f"An error occurred while writing to {file_location}: {e}")


@router.post("/employees/", response_model=EmployeeManagement)
def create_user(user: EmployeeManagementCreate):
    try:
        current_directory = Path(__file__).parents[1]

        response_file = "employee_management_response.json"

        file_name = current_directory / "response" / response_file

        user_dict = user.dict()
        user_dict["id"] = generate_random_id()

        response_data = jsonable_encoder(EmployeeManagement(**user_dict))

        create_response_json(user_dict["id"], response_data, file_name)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response_data,
            media_type="application/json;charset=utf-8",
        )
    except Exception as err:
        error_500 = {
            "message": str(err),
            "reason": "The server encountered an unexpected condition that prevented it from fulfilling the request",
            "referenceError": "https://tools.ietf.org/html/rfc7231",
            "code": "internalError",
        }
        json_compatible_item_data = jsonable_encoder(Error500(**error_500))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json_compatible_item_data,
            media_type="application/json;charset=utf-8",
        )


@router.get("/employee/{id}", response_model=EmployeeManagement)
def get_employee_by_id(
    id: str = Path(description="Unique identifier for the Employee."),
):
    try:
        current_directory = Path(__file__).parents[1]
        file = "employee_management_response.json"
        file_name = current_directory / "response" / file
        
        if not file_name.exists():
            raise HTTPException(status_code=404, detail="file not found")

        try:
            with open(file_name, "r") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=404, detail="Record not found")

        if id in json_data:
            json_result = json_data[id]
            response_data = jsonable_encoder(EmployeeManagement(**json_result))
            return JSONResponse(
                status_code=200,
                content=response_data,
                media_type="application/json;charset=utf-8",
            )
        else:
            error_404 = {
                "message": "Id not found",
                "reason": "Id not found",
                "referenceError": "https://tools.ietf.org/html/rfc7231",
                "code": "notFound",
            }
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content=json_compatible_item_data
            )

    except Exception as err:
        error_500 = {
            "message": str(err),
            "reason": "The server encountered an unexpected condition that prevented it from fulfilling the request",
            "referenceError": "https://tools.ietf.org/html/rfc7231",
            "code": "internalError",
        }
        json_compatible_item_data = jsonable_encoder(Error500(**error_500))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json_compatible_item_data,
            media_type="application/json;charset=utf-8",
        )


@router.patch("/employee/{id}", response_model=EmployeeManagement)
def update_user(
    user: EmployeeManagementCreate,
    id: str = Path(description="Unique identifier for the Employee."),
):
    # try:
        current_directory = Path(__file__).parents[1]
        file = "employee_management_response.json"
        file_name = current_directory / "response" / file
        
        if not file_name.exists():
            raise HTTPException(status_code=404, detail="file not found")

        try:
            with open(file_name, "r") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=404, detail="Record not found")


        # with open(file_name, "r") as json_file:
        #     json_data = json.load(json_file)

        if id in json_data:
            json_result = json_data[id]

            json_result.update(user.dict())

            with open(file_name, "w") as json_file:
                json.dump(json_data, json_file, indent=2, default=str)

            response_data = jsonable_encoder(EmployeeManagement(**json_result))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response_data,
                media_type="application/json;charset=utf-8",
            )
        else:
            error_404 = {
                "message": "Id not found",
                "reason": "Id not found",
                "referenceError": "https://tools.ietf.org/html/rfc7231",
                "code": "notFound",
            }
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content=json_compatible_item_data
            )
    # except Exception as err:
    #     error_500 = {
    #         "message": str(err),
    #         "reason": "The server encountered an unexpected condition that prevented it from fulfilling the request",
    #         "referenceError": "https://tools.ietf.org/html/rfc7231",
    #         "code": "internalError",
    #     }
    #     json_compatible_item_data = jsonable_encoder(Error500(**error_500))
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content=json_compatible_item_data,
    #         media_type="application/json;charset=utf-8",
    #     )


@router.delete("/employees/{employee_id}")
def delete_user(employee_id: str):
  
        current_directory = Path(__file__).parents[1]
        file = "employee_management_response.json"
        file_name = current_directory / "response" / file
        
        if not file_name.exists():
            raise HTTPException(status_code=404, detail="file not found")

        try:
            with open(file_name, "r") as file:
                existing_data = json.load(file)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=404, detail="Record not found")

        if employee_id not in existing_data:
            error_404 = {
                "message": "Id not found",
                "reason": "Id not found",
                "referenceError": "https://tools.ietf.org/html/rfc7231",
                "code": "notFound",
            }
            json_compatible_item_data = jsonable_encoder(Error404(**error_404))
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content=json_compatible_item_data
            )

        del existing_data[employee_id]

        with open(file_name, "w") as file:
            json.dump(existing_data, file, indent=4)

        return JSONResponse(
            content={"message": f"Employee with ID {employee_id} has been deleted"}
        )



@router.get("/find_employees/")
def lists_or_finds_employee(
    name: Optional[str] = Query(
        default=None,
        description="The name of the employee",
    ),
    department: Optional[str] = Query(
        default=None,
        description="Department of the employee",
        enum=["development", "Testing", "human_resources", "support", "finance"],
    ),
    offset: Optional[int] = Query(
        default=None,
        description="Requested index for the start of the items to be provided in the response requested by the client. Note that the index starts with '0'.",
        format="int32",
    ),
    limit: Optional[int] = Query(
        default=None,
        description="Requested number of items to be provided in the response requested by the client",
        format="int32",
    ),
):
    """
    This operation lists or finds ProductOrder entities
    """
    # try:
    if offset is not None and offset < 0:
        raise HTTPException(status_code=400, detail="Offset cannot be negative")
    if limit is not None and limit < 0:
        raise HTTPException(status_code=400, detail="Limit cannot be negative")
    if offset is None:
        offset = 0
    if limit is None:
        limit = 10
    # response_file = "employee_management_response.json"
    current_directory = Path(__file__).parents[1]
    file = "employee_management_response.json"
    file_name = current_directory / "response" / file
    if not file_name.exists():
        raise HTTPException(status_code=404, detail="file not found")

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=404, detail="Record not found")
    
    extracted_data = []
    for _, employ_info in data.items():
        json_name = employ_info.get("name")

        json_department = employ_info.get("department")

        if (name == None or name == json_name) and (
            department is None or department == json_department
        ):
            extracted_info = {
                "id": employ_info.get("id"),
                "name": employ_info.get("name"),
                "department": employ_info.get("department"),
                "email": employ_info.get("email"),
                "contact": employ_info.get("contact"),
            }
            extracted_data.append(extracted_info)
    limited_responses = extracted_data[offset : offset + limit]

    if not limited_responses or not extracted_data:
        raise HTTPException(
            status_code=404, detail="No matching result found for the given criteria."
        )
    limited_responses_schema = jsonable_encoder(
        [EmployeeManagement(**employee_data) for employee_data in limited_responses]
    )

    return limited_responses_schema
