import type { ActividadId, Participante } from '../types'

export type CasoParticipantes = {
  id: string
  titulo: string
  descripcion: string
  actividad: ActividadId
  participantes: Participante[]
  esperado: string
  test: string
}

const participante = (nombre: string, dni: string, edad: string, talle_vestimenta = ''): Participante =>
  ({ nombre, dni, edad, talle_vestimenta })

export const casosParticipantes: CasoParticipantes[] = [
  {
    id: 'edad', titulo: 'Edad mínima', descripcion: 'Tirolesa con un participante de 7 años.',
    actividad: 'Tirolesa', participantes: [participante('Ana Perez', '12345678', '7', 'M')],
    esperado: 'Tirolesa requiere una edad mínima de 8 años.',
    test: 'test_confirma_con_las_reglas_de_edad_y_talle_de_la_actividad',
  },
  {
    id: 'talle', titulo: 'Talle obligatorio', descripcion: 'Palestra sin talle de vestimenta.',
    actividad: 'Palestra', participantes: [participante('Ana Perez', '12345678', '16')],
    esperado: 'Seleccioná el talle del participante 1.',
    test: 'test_validar_talles_vestimenta',
  },
  {
    id: 'dni', titulo: 'DNI repetido', descripcion: 'Dos participantes con el mismo DNI.',
    actividad: 'Safari', participantes: [participante('Ana Perez', '12345678', '25'), participante('Luis Gomez', '12345678', '28')],
    esperado: 'Los DNI de los participantes no pueden repetirse.',
    test: 'test_rechaza_dnis_repetidos_dentro_de_la_misma_solicitud',
  },
  {
    id: 'valido', titulo: 'Datos válidos', descripcion: 'Un participante de Safari que cumple las reglas.',
    actividad: 'Safari', participantes: [participante('Ana Perez', '12345678', '25')],
    esperado: 'Datos válidos.',
    test: 'test_validar_cantidad_valida',
  },
]
