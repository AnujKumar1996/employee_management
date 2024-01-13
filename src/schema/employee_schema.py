from pydantic import BaseModel, Field, constr
from enum import Enum


class Department(str, Enum):
    testing = "Testing"
    development = "Development"
    finance = "Finance"
    human_resource = "Human Resource"
    support = "Support"


class EmployeeManagementCreate(BaseModel):
    name: str = Field(description="Employee's name")
    email: str = Field(
        example="Email address",
        description="Employee's email address",
        min_length=6,
        pattern="^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})+$",
    )

    contact: int = Field(
        ...,
        description="Employee's contact number (10 digits)",
        ge=10**9,  # Minimum value (10 digits)
        le=10**10 - 1,  # Maximum value (10 digits)
    )

    department: Department = Field(
        description="Employee's department (Testing, Development, Finance, Human Resource, Support)"
    )


class EmployeeManagement(BaseModel):
    id: str = Field(description="Employee's ID")
    name: str = Field(description="Employee's name")
    email: str = Field(
        example="Email address",
        description="Employee's email address",
        min_length=6,
        pattern="^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})+$",
    )
    contact: int = Field(
        ...,
        description="Employee's contact number (10 digits)",
        ge=10**9,  # Minimum value (10 digits)
        le=10**10 - 1,  # Maximum value (10 digits)
    )
    department: Department = Field(
        description="Employee's department (Testing, Development, Finance, Human Resource, Support)"
    )
