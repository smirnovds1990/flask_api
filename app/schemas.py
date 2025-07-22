from decimal import Decimal

from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    image_url: str
    main_image: bool
    position: int | None
    sort_order: int | None
    title: str | None

    class Config:
        orm_mode = True


class ParameterSchema(BaseModel):
    id: int
    chosen: bool | None
    disabled: bool | None
    extra_field_color: str | None
    extra_field_image: str | None
    name: str | None
    old_price: Decimal | None
    parameter_string: str | None
    price: Decimal | None
    sort_order: int | None

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str
    image: str | None
    sort_order: int | None

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    id: int
    name: str
    images: list[ImageSchema]
    parameters: list[ParameterSchema]
    categories: list[CategorySchema]

    class Config:
        orm_mode = True
