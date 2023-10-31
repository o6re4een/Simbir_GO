
    
from schemas.color_schema import ColorSchemaCreate
from schemas.transportModel_schema import TransportModelSchemaBase
from schemas.transportType_schema import TransportTypeSchema, TransportTypeSchemaCreate
from schemas.transport_schema import TransportSchemaCreate, TrasnportSchemaResponse
from services.users_service import UsersService
from utils.unitofwork import IUnitOfWork


async def create_if_not_exist(uow: IUnitOfWork, transport_dict: dict, owner_id: int = None) -> dict:
    color_name = transport_dict['color']
    existing_color = await uow.colors.find_one(value=color_name)
    if not existing_color:
        color_data = ColorSchemaCreate(
            value=color_name  # Provide the correct data for the color here
        )
        color_id = await uow.colors.add_one(color_data.model_dump())
    else:
        color_id = existing_color
    
    # Check if transport type exists, and if not, create it
    if(transport_dict.get("transportType")):
        transport_type_name = transport_dict['transportType']
        existing_transport_type = await uow.transport_types.find_one(value=transport_type_name)
        if not existing_transport_type:
            transport_type_data = TransportTypeSchemaCreate(
                value=transport_type_name  # Provide the correct data for the transport type here
            )
            transport_type_id = await uow.transport_types.add_one(transport_type_data.model_dump())
        else:
            transport_type_id = existing_transport_type
        transport_dict['transportTypeId'] = transport_type_id.id

    # Check if transport model exists, and if not, create it
    model_name = transport_dict['model']
    existing_model = await uow.transport_models.find_one(value=model_name)
    if not existing_model:
        model_data = TransportModelSchemaBase(
            value=model_name  # Provide the correct data for the model here
        )
        model_id = await uow.transport_models.add_one(model_data.model_dump())
    else:
        model_id = existing_model

    # await uow.commit()
    # Update the transport_dict with the newly created IDs (if they were created)
    
    transport_dict['colorId'] = color_id.id
   
    transport_dict['transportModelId'] = model_id.id
    if(owner_id):
        transport_dict['ownerId'] = owner_id 
    # transport_dict['canBeRented'] = transport_data.canBeRented

    transport_dict['model'] = None
    transport_dict['color'] = None
    transport_dict["transportType"] = None

    new_dict = {
        key: value for key, value in transport_dict.items()
        if value is not None
    }
    return new_dict

async def clear_transport_dict(uow, transport):
    # print(transport.model_dump())
    # transport = TrasnportSchemaResponse(
    #     **transport.model_dump()
    # )
    transportType = await TransportTypeService().get_transport_type_by_id(uow, transport.transportTypeId)
    color = await ColorService().get_color_by_id(uow, transport.colorId)
    transportModel = await TransportModelService().get_transport_model_by_id(uow, transport.transportModelId)
    owner = await UsersService().get_by_id(uow, transport.ownerId)
  

    transport = TrasnportSchemaResponse(
        **transport.model_dump()
    )

    transport.model = transportModel.value
    transport.color = color.value
    transport.transportType = transportType.value
    transport.owner = owner.username
    # transport["transportTypeId"] = None
    # transport["transportModelId"] = None
    # transport["colorId"] = None
   
    
    # new_dict = {
    #     key: value for key, value in transport.items()
    #     if value is not None
    # }
    return transport

class TransportService:
    
    async def create_transport(self, uow: IUnitOfWork, transport_data: TransportSchemaCreate, owner_id):
        transport_dict = transport_data.model_dump()
        async with uow:
            # Check if color exists, and if not, create it
            new_dict = await create_if_not_exist(uow, transport_dict, owner_id)

            # print(transport_dict)

            transport_id = await uow.transport.add_one(new_dict)
            await uow.commit()
        return transport_id

    async def get_transports(self, uow: IUnitOfWork):
        async with uow:
            transports = await uow.transport.find_all()
            return transports

    async def get_transport_by_id(self, uow: IUnitOfWork, transport_id):
        async with uow:
            transport = await uow.transport.find_one(id=transport_id)

            transport = await clear_transport_dict(uow, transport)


            return transport

    async def find_transport_by_id_range(self, uow: IUnitOfWork, start_id: int, end_id: int, type):
        async with uow:
             
            transportType = await uow.transport_types.find_one(value=type) 
            transport = await uow.transport.find_by_id_range(start_id, end_id, transportTypeId=transportType.id)
            return transport
          
            

    async def update_transport(self, uow: IUnitOfWork, transport_id: int, transport_data: TransportSchemaCreate):
        async with uow:
            update_data_dict = transport_data.model_dump(exclude_unset=True)

            new_dict = await create_if_not_exist(uow, update_data_dict)

            new_dict = {
                key: value for key, value in update_data_dict.items()
                if value is not None
            }
            updated_transport = await uow.transport.edit_one(transport_id, new_dict)
            await uow.commit()
            return updated_transport

    async def delete_transport_by_id(self, uow: IUnitOfWork, transport_id: int):
        async with uow:
            result = await uow.transport.delete_by_id(transport_id)
            await uow.commit()
            return result

class TransportModelService:
    async def create_transport_model(self, uow: IUnitOfWork, transport_model_data: TransportModelSchemaBase):
        transport_model_dict = transport_model_data.model_dump()
        async with uow:
            transport_model_id = await uow.transport_models.add_one(transport_model_dict)
            await uow.commit()
            return transport_model_id

    async def get_transport_models(self, uow: IUnitOfWork):
        async with uow:
            transport_models = await uow.transport_models.find_all()
            return transport_models

    async def get_transport_model_by_id(self, uow: IUnitOfWork, transport_model_id):
        async with uow:
            transport_model = await uow.transport_models.find_one(id=transport_model_id)
            return transport_model

    async def update_transport_model(self, uow: IUnitOfWork, transport_model_id: int, transport_model_data: TransportTypeSchemaCreate):
        async with uow:
            update_data_dict = transport_model_data.model_dump(exclude_unset=True)
            updated_transport_model = await uow.transport_models.edit_one(transport_model_id, update_data_dict)
            await uow.commit()
            return updated_transport_model

    async def delete_transport_model_by_id(self, uow: IUnitOfWork, transport_model_id: int):
        async with uow:
            result = await uow.transport_models.delete_by_id(transport_model_id)
            await uow.commit()
            return result

class TransportTypeService:
    async def create_transport_type(self, uow: IUnitOfWork, transport_type_data: TransportTypeSchemaCreate):
        transport_type_dict = transport_type_data.model_dump()
        async with uow:
            transport_type_id = await uow.transport_types.add_one(transport_type_dict)
            await uow.commit()
            return transport_type_id

    async def get_transport_types(self, uow: IUnitOfWork) -> list[TransportTypeSchema]:
        async with uow:
            transport_types = await uow.transport_types.find_all()
            return transport_types

    async def get_transport_type_by_id(self, uow: IUnitOfWork, transport_type_id):
        async with uow:
            transport_type = await uow.transport_types.find_one(id=transport_type_id)
            return transport_type

    async def update_transport_type(self, uow: IUnitOfWork, transport_type_id: int, transport_type_data: TransportTypeSchemaCreate):
        async with uow:
            update_data_dict = transport_type_data.model_dump(exclude_unset=True)
            updated_transport_type = await uow.transport_types.edit_one(transport_type_id, update_data_dict)
            await uow.commit()
            return updated_transport_type

    async def delete_transport_type_by_id(self, uow: IUnitOfWork, transport_type_id: int):
        async with uow:
            result = await uow.transport_types.delete_by_id(transport_type_id)
            await uow.commit()
            return result

class ColorService:
    async def create_color(self, uow: IUnitOfWork, color_data: ColorSchemaCreate):
        color_dict = color_data.model_dump()
        async with uow:
            color_id = await uow.colors.add_one(color_dict)
            await uow.commit()
            return color_id

    async def get_colors(self, uow: IUnitOfWork):
        async with uow:
            colors = await uow.colors.find_all()
            return colors

    async def get_color_by_id(self, uow: IUnitOfWork, color_id):
        async with uow:
            color = await uow.colors.find_one(id=color_id)
            return color

    async def update_color(self, uow: IUnitOfWork, color_id: int, color_data: ColorSchemaCreate):
        async with uow:
            update_data_dict = color_data.model_dump(exclude_unset=True)
            updated_color = await uow.colors.edit_one(color_id, update_data_dict)
            await uow.commit()
            return updated_color

    async def delete_color_by_id(self, uow: IUnitOfWork, color_id: int):
        async with uow:
            result = await uow.colors.delete_by_id(color_id)
            await uow.commit()
            return result