import enum

class RolNombre(str, enum.Enum):
    super_admin = "super_admin"
    encargado = "encargado"
    docente = "docente"

class EstadoGeneral(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"

class Gestion(str, enum.Enum):
    publica = "publica"
    privada = "privada"
    convenio = "convenio"

class TipoDocumento(str, enum.Enum):
    DNI = "DNI"
    CE = "CE"
    PASAPORTE = "PASAPORTE"
    OTRO = "OTRO"

class NivelEducativo(str, enum.Enum):
    inicial = "inicial"
    primaria = "primaria"
    secundaria = "secundaria"

class NivelLogro(str, enum.Enum):
    C = "C"
    B = "B"
    A = "A"
    AD = "AD"

class EstadoMatricula(str, enum.Enum):
    activo = "activo"
    retirado = "retirado"
    trasladado = "trasladado"

class EstadoArchivoCarga(str, enum.Enum):
    pendiente = "pendiente"
    procesado = "procesado"
    con_errores = "con_errores"
    rechazado = "rechazado"

class EstadoFicha(str, enum.Enum):
    borrador = "borrador"
    pendiente_revision = "pendiente_revision"
    validada = "validada"
    exportada = "exportada"

class TipoAlerta(str, enum.Enum):
    caida_rendimiento = "caida_rendimiento"
    estancamiento = "estancamiento"
    riesgo_asistencia = "riesgo_asistencia"

class SeveridadAlerta(str, enum.Enum):
    bajo = "bajo"
    medio = "medio"
    alto = "alto"

class EstadoDocumentoCurricular(str, enum.Enum):
    activo = "activo"
    reemplazado = "reemplazado"
    error_indexacion = "error_indexacion"

class Tendencia(str, enum.Enum):
    subida = "subida"
    estable = "estable"
    caida = "caida"