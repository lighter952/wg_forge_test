from pydantic import BaseModel, field_validator


class Cat(BaseModel):
    name: str
    color: str
    tail_length: int
    whiskers_length: int

    @field_validator('color')
    def is_in_enum(cls, v):
        if v not in ['black', 'white', 'black & white', 'red', 'red & white', 'red & black & white']:
            raise ValueError("Not in colors list")
        return v.title()

    @field_validator('tail_length')
    def tail_length_check(cls, v):
        if v not in range(0,30):
            raise ValueError("Tail length not in range from 0 to 30 cm")
        return v

    @field_validator('whiskers_length')
    def whiskers_length_check(cls, v):
        if v not in range(0, 70):
            raise ValueError("Whiskers length not in range from 0 to 70 cm")
        return v


