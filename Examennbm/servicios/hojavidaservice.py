from ..models.citas import HojaVida
from ..conexion.conbdhojavida import (select_all_hojas_vida,
                                 select_hoja_vida_by_persona_id,
                                 crear_hoja_vida,
                                 eliminar_hoja_vida,
                                 actualizar_hoja_vida)

def servicio_hojas_vida_all():
    hojas_vida = select_all_hojas_vida()
    print(hojas_vida)
    return hojas_vida

def servicio_consultar_hoja_vida(persona_id: int):
    if persona_id:
        hoja_vida = select_hoja_vida_by_persona_id(persona_id)
        print(hoja_vida)
        return hoja_vida
    else:
        return select_all_hojas_vida()

def servicio_crear_hoja_vida(persona_id: int, experiencia: str, educacion: str, habilidades: str):
    print("person id")
    print(persona_id)
    hoja_vida_existente = servicio_consultar_hoja_vida(persona_id)
    if not hoja_vida_existente:
        nueva_hoja_vida = HojaVida(persona_id=persona_id, experiencia=experiencia,
                                   educacion=educacion, habilidades=habilidades)
        return crear_hoja_vida(nueva_hoja_vida)
    else:
        return "La hoja de vida ya existe para esta persona"

def servicio_eliminar_hoja_vida(id: int):
    return eliminar_hoja_vida(id)

def servicio_actualizar_hoja_vida(id: int, datos_actualizacion: dict):
    return actualizar_hoja_vida(id, datos_actualizacion)