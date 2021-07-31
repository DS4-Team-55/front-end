master_query = """
select  -- variables de la tabla que las tenga
        coalesce(morb.num_ide_, mort.num_ide_, numero_documento_madre) as identificacion,
        coalesce(morb.nombre_nacionalidad, mort.nombre_nacionalidad) as nombre_nacionalidad,
        coalesce(morb.cod_dpto_r, mort.cod_dpto_r) as codigo_departamento_r,
        coalesce(morb.cod_mun_r, mort.cod_mun_r) as codigo_municipio_r,
        coalesce(morb.fecha_nto_, mort.fecha_nto_) as fecha_nacimiento,
        coalesce(morb.ocupacion_, mort.ocupacion_) as ocupacion,
        coalesce(morb.tip_ss_, mort.tip_ss_) as tip_ss_,
        coalesce(morb.cod_ase_, mort.cod_ase_) as cod_ase_,
        coalesce(morb.per_etn_, mort.per_etn_) as per_etn_,
        coalesce(morb.estrato_, mort.estrato_) as estrato_, 
        -- variables de mortalidad
         sem_ges_mort, fec_defunsion,  causa_muerte,
        --variables de morbilidad
        fec_not_morb, sem_ges_morb, num_gestac,	num_parvag,	num_cesare,	num_aborto,	num_molas,	num_ectopi,	num_muerto,	num_vivos,	fec_ul_ges,	no_con_pre,	sem_c_pren,
        term_gesta,	moc_rel_tg,	falla_card,	falla_rena,	falla_hepa,	falla_cere,	falla_resp,	falla_coag,	eclampsia,	preclampsi,	choq_septi,	
        hemorragia_obstetrica_severa,	rupt_uteri,	cir_adicio, caus_princ, caus_agrup,
        --variables nacidos vivos
        fecha_nacimiento as fecha_nto_bebe, tiempo_de_gestacion as sem_ges_mort_parto, edad_madre as edad_madre_parto, estado_conyugal_madre, 
        nivel_educativo_madre,  departamento_residencia, municipio_residencia, 
        --varaiable de hopitalizacion
        case when hosp.no_hospitalizaciones is null then 0 else hosp.no_hospitalizaciones end as no_hospitalizaciones,
        --variable de consultas
        case when cons.consultas is null then 0 else cons.consultas end as no_consultas,
        --variables de covid
        covid.ini_sin_covid,  gp_gestan_covid, sem_ges_covid

from
  -- Datos de morbilidad (se están duplicando 9 casos)
  (select distinct num_ide_, fec_not as fec_not_morb, area_, nombre_nacionalidad, cod_dpto_r,	cod_mun_r,	area_, ocupacion_,	tip_ss_,	cod_ase_,	per_etn_,	 
          estrato_,	gp_gestan, fecha_nto_, sem_ges_ as sem_ges_morb, 
          num_gestac,	num_parvag,	num_cesare,	num_aborto,	num_molas,	num_ectopi,	num_muerto,	num_vivos,	fec_ul_ges,	no_con_pre,	sem_c_pren,
          term_gesta,	moc_rel_tg,	falla_card,	falla_rena,	falla_hepa,	falla_cere,	falla_resp,	falla_coag,	eclampsia,	preclampsi,	choq_septi,	
          hemorragia_obstetrica_severa,	rupt_uteri,	cir_adicio, caus_princ, caus_agrup
  from saludata.morbilidad --239 registros
  )morb

full outer join
  -- Datos de mortalidad
  (select distinct cast(num_ide_ as varchar) as num_ide_,  fec_not, area_, nombre_nacionalidad, cod_dpto_r,	cod_mun_r,	area_,	ocupacion_, tip_ss_,	cod_ase_,	per_etn_,	 
          estrato_,	gp_gestan, fecha_nto_, sem_ges_ as sem_ges_mort,  
          fec_def_ as fec_defunsion,  cbmte_ as causa_muerte
  from saludata.mortalidad
  )mort
on morb.num_ide_= mort.num_ide_

full outer join
 -- Datos nacidos vivos
  (select distinct numero_documento_madre, fecha_nacimiento, tiempo_de_gestacion, numero_consultas_prenatales, edad_madre, estado_conyugal_madre, nivel_educativo_madre, 
  departamento_residencia, municipio_residencia
  from saludata.nacidos_vivos
  )nacidos
on cast(morb.num_ide_ as varchar)= cast(nacidos.numero_documento_madre as varchar)

left join
  -- Conteo del número de hospitalizaciones para cada mamá
  (select  numero_de_identificacion_del_usuario_en_el_sistema, 
          count(distinct(numero_de_la_factura))no_hospitalizaciones
  from saludata.rpshospitalizacion
  group by tipo_de_documento_de_identificacion_del_usuario, numero_de_identificacion_del_usuario_en_el_sistema
  )hosp
on coalesce(morb.num_ide_, mort.num_ide_, numero_documento_madre) = hosp.numero_de_identificacion_del_usuario_en_el_sistema

left join
  -- Conteo del número de consultas para cada mamá
  (select  numero_de_identificacion_del_usuario,  count(distinct(codigo_de_la_consulta)) as consultas
  from saludata.rpsconsultas
  where finalidad_de_la_consulta in (06)
  group by tipo_de_identificacion_del_usuario, numero_de_identificacion_del_usuario	
  )cons
on coalesce(morb.num_ide_, mort.num_ide_, numero_documento_madre) = cons.numero_de_identificacion_del_usuario

left join
  -- Datos de coronavirus
  (select num_ide_, ini_sin_ as ini_sin_covid,
    gp_gestan as gp_gestan_covid, sem_ges as sem_ges_covid
  from saludata.coronavirus 
  )covid
on coalesce(morb.num_ide_, mort.num_ide_, numero_documento_madre) = covid.num_ide_
order by ini_sin_covid, fec_defunsion, fec_not_morb
;
"""

morbidity_query = """
SELECT * FROM saludata.morbilidad
"""

mortality_query = """
SELECT * FROM saludata.mortalidad
"""

livebirths_query = """
SELECT * FROM saludata.nacidos_vivos
"""

covid_query = """
SELECT municipio FROM saludata.coronavirus
"""