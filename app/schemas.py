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


class CategoryInSchema(BaseModel):
    Category_ID: int
    Category_Name: str
    Category_Image: str | None
    sort_order: int | None


class ProductMarkInSchema(BaseModel):
    Mark_ID: int
    Mark_Name: str


class ImageInSchema(BaseModel):
    Image_ID: int
    Image_URL: str
    MainImage: bool
    Product_ID: int
    position: int | str | None
    sort_order: int | None
    title: str | None


class ParameterInSchema(BaseModel):
    Parameter_ID: int
    chosen: bool | None
    disabled: bool | None
    extra_field_color: str | None
    extra_field_image: str | None
    name: str | None
    old_price: Decimal | None
    parameter_string: str | None
    price: Decimal | None
    sort_order: int | None


class ProductInSchema(BaseModel):
    Product_ID: int
    Product_Name: str
    OnMain: bool
    images: list[ImageInSchema]
    parameters: list[ParameterInSchema]
    categories: list[CategoryInSchema]
