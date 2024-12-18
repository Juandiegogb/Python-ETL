# Projecto de migración tablero

## Tablero:  MONITOR DE CAMAS

la siguiente sentencia SQL es la encargada de alimentar el tablero, a continuación se realiza un listado de las tablas involucradas para su futura implementación en una ETL de Python

```
/*MONITOR DE CAMAS*/
/*DETALLE*/
SELECT DISTINCT
 COALESCE(InstalacionPrestador8.Descripcion,InstalacionPrestador7.Descripcion,InstalacionPrestador6.Descripcion,InstalacionPrestador5.Descripcion,InstalacionPrestador4.Descripcion,InstalacionPrestador3.Descripcion,InstalacionPrestador2.Descripcion,InstalacionPrestador1.Descripcion) AS Sucursal
 ,Servicio.Descripcion AS Servicio
 ,TipoInstalacionPrestador.Codigo
 ,InstalacionPrestador.Descripcion AS Cama
 ,InstalacionPrestador1.Descripcion AS Habitacion
 ,EstadoInstalacionPrestador.Descripcion AS Estado
 ,Persona.NumeroDocumento AS IdentificacionPaciente
 ,Sexo.Genero
 ,GrupoHabilitacion.Descripcion AS Grupo
 ,CASE InstalacionPrestador.CamaVirtual WHEN '1' THEN 'Si'
  WHEN '0' THEN 'No' END AS CamaVirtual
 ,TipoInstalacionPrestador.Descripcion AS Tipo
 ,Prestador.Descripcion AS Prestador
 ,Admision.ConsecutivoAdmision AS IDIngreso
 ,CONCAT(Persona.PrimerNombre, Persona.SegundoNombre, Persona.PrimerApellido, Persona.SegundoApellido) AS Paciente
 ,Pagador.Descripcion AS Prevision
 ,Tarifario.Descripcion AS Arancel
FROM InstalacionPrestador
INNER JOIN TipoInstalacionPrestador ON InstalacionPrestador.Tipo = TipoInstalacionPrestador.ID AND TipoInstalacionPrestador.Codigo = '321'
INNER JOIN EstadoInstalacionPrestador ON InstalacionPrestador.Estado = EstadoInstalacionPrestador.ID AND EstadoInstalacionPrestador.Codigo <>  'Bloq'
LEFT JOIN InstalacionPrestador InstalacionPrestador1 ON InstalacionPrestador.IDSuperior = InstalacionPrestador1.ID --Habitación
LEFT JOIN InstalacionPrestador InstalacionPrestador2 ON InstalacionPrestador1.IDSuperior = InstalacionPrestador2.ID
LEFT JOIN InstalacionPrestador InstalacionPrestador3 ON InstalacionPrestador2.IDSuperior = InstalacionPrestador3.ID
LEFT JOIN InstalacionPrestador InstalacionPrestador4 ON InstalacionPrestador3.IDSuperior = InstalacionPrestador4.ID
LEFT JOIN InstalacionPrestador InstalacionPrestador5 ON InstalacionPrestador4.IDSuperior = InstalacionPrestador5.ID
LEFT JOIN InstalacionPrestador InstalacionPrestador6 ON InstalacionPrestador5.IDSuperior = InstalacionPrestador6.ID
LEFT JOIN InstalacionPrestador InstalacionPrestador7 ON InstalacionPrestador6.IDSuperior = InstalacionPrestador7.ID
LEFT JOIN InstalacionPrestador InstalacionPrestador8 ON InstalacionPrestador7.IDSuperior = InstalacionPrestador8.ID
LEFT JOIN (
   SELECT
   ROW_NUMBER() OVER(PARTITION BY InstalacionPrestador ORDER BY FechaReal DESC) AS UltimaAdmision
   ,InstalacionPrestador
   ,Admision
   ,FechaReal
   FROM AdmisionInstalacionPrestador
   ) UltimaAdmision ON InstalacionPrestador.ID = UltimaAdmision.InstalacionPrestador AND UltimaAdmision = 1
LEFT JOIN Admision ON UltimaAdmision.Admision = Admision.ID
LEFT JOIN Persona ON Admision.Persona = Persona.ID
LEFT JOIN Sexo ON Persona.Sexo = Sexo.ID
LEFT JOIN InstalacionPrestadorServicio ON InstalacionPrestador.ID = InstalacionPrestadorServicio.InstalacionPrestador
LEFT JOIN Servicio ON InstalacionPrestadorServicio.Servicio = Servicio.ID
LEFT JOIN GrupoHabilitacion ON Servicio.GrupoHabilitacion = GrupoHabilitacion.ID
LEFT JOIN Prestador ON InstalacionPrestador.Prestador = Prestador.ID
LEFT JOIN AdmisionContratoPlan ON Admision.ID = AdmisionContratoPlan.Admision
LEFT JOIN ContratoPlan ON AdmisionContratoPlan.ContratoPlan = ContratoPlan.ID
LEFT JOIN Contrato ON ContratoPlan.Contrato = Contrato.ID
LEFT JOIN Pagador ON Contrato.Pagador = Pagador.ID
LEFT JOIN Tarifario ON ContratoPlan.Tarifario = Tarifario.ID

```
