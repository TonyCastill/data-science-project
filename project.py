import pandas as pd
import os # To read raw data

dataframes = []
directory_path = "data/raw_data/"

for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.lower()
        dataframes.append(df)

len(dataframes)
# dataframes["conjunto_de_datos_divorcios_2017"]
# divorces_in_2023 = pd.read_csv("data/2023/conjunto_de_datos_ed2023.csv", header=0)

def load_catalog_as_dict(csv_path):
    """
    Loads a CSV catalog into a dictionary using 'clave' as key and 'descripción' as value.
    """
    df = pd.read_csv(csv_path, dtype={"clave": int})
    return dict(zip(df["clave"], df["descripción"]))

divorce_type_dict = load_catalog_as_dict("data/catalogs/tipo_divorcio.csv")
location_catalog2 = pd.read_csv("data/catalogs/entidad_municipio_localidad_2023.csv", dtype={"cve_ent": str, "cve_mun": str, "cve_loc": str})
# Build nested dictionary
location_dict = {}

for _, row in location_catalog2.iterrows():
    ent = row['cve_ent']
    mun = row['cve_mun']
    loc = row['cve_loc']
    name = row['nom_loc']

    location_dict.setdefault(ent, {}).setdefault(mun, {})[loc] = name
petitioner_dict = load_catalog_as_dict("data/catalogs/persona_que_inicio.csv")
winner_dict = load_catalog_as_dict("data/catalogs/a_favor.csv")
divorce_reason_dict = load_catalog_as_dict("data/catalogs/causas_divorcio.csv")
custody_dict = load_catalog_as_dict("data/catalogs/custodia.csv")
parental_authority_dict = load_catalog_as_dict("data/catalogs/patria_potestad.csv")
child_maintenance_dict = load_catalog_as_dict("data/catalogs/pension_alimenticia.csv")
nationality_dict = load_catalog_as_dict("data/catalogs/nacionalidad.csv")
marital_status_dict = load_catalog_as_dict("data/catalogs/estado_conyugal.csv")
education_level_dict = load_catalog_as_dict("data/catalogs/escolaridad.csv")
economic_situation_dict = load_catalog_as_dict("data/catalogs/condicion_actividad_economica.csv")
dedication_dict = load_catalog_as_dict("data/catalogs/dedicado_a.csv")
job_dict = load_catalog_as_dict("data/catalogs/posicion_trabajo.csv")
gender_dict = load_catalog_as_dict("data/catalogs/condicion_biologica.csv")

# Get divorce type
def get_divorce_type(divorce_type_param):
    #Use catalogs to assign values
    # return divorce_type_catalog.query("clave == @divorce_type_param")["descripción"].item()
    return divorce_type_dict.get(divorce_type_param, "Valor desconocido")

# def get_divorce_type2(divorce_type_param):
#     #Use catalogs to assign values
#     return "Administrativo" if divorce_type_param == 2 else "Judicial"
#     # return divorce_type_catalog.query("clave == @divorce_type_param")["descripción"].item()
    
def get_location2(state_id, municipality_id, locality_id):
    state_id = str(state_id).zfill(2)
    municipality_id = str(municipality_id).zfill(3)
    locality_id = str(locality_id).zfill(4)

    state = location_dict.get(state_id, {}).get("000", {}).get("0000", "Unknown State")
    municipality = location_dict.get(state_id, {}).get(municipality_id, {}).get("0000", "Unknown Municipality")
    locality = location_dict.get(state_id, {}).get(municipality_id, {}).get(locality_id, "Unknown Locality")

    return {"state": state, "municipality": municipality, "locality": locality}
# Get location name
# def get_location(state_id,municipality_id, locality_id):
#     state = location_catalog.query("cve_ent == @state_id and cve_mun == 0 and cve_loc == 0")["nom_loc"].item()
#     municipality = location_catalog.query("cve_ent == @state_id and cve_mun == @municipality_id and cve_loc == 0")["nom_loc"].item()
#     locality = location_catalog.query("cve_ent == @state_id and cve_mun == @municipality_id and cve_loc == @locality_id")["nom_loc"].item()
#     return {"state":state,"municipality":municipality,"locality":locality}

# Function to reformat column names to "mm-dd-yyyy"
def get_formated_date(day,month,year):
    # print(date["day"])
    day_valid = day != 99
    month_valid = month != 99
    year_valid = year != 9999
    
    date_obj = {
        "day": day if day_valid else None,
        "month": month if month_valid else None,
        "year": year if year_valid else None
    }

    # Construct full_date only if all parts are valid
    if day_valid and month_valid and year_valid:
        full_date = f"{month:02d}-{day:02d}-{year:04d}"
    else:
        full_date = None
    date_obj["full_date"]=full_date
    return date_obj
def get_age(age):
    # if(age != 99 and age != 999):
    #     age_valid = age
    # age_valid = age
    age_valid = age not in(999,99)
    # age_valid = age != 999
    return age if age_valid else None

def get_petitioner(petitioner_id):
    # return petitioner_catalog.query("clave == @petitioner_id")["descripción"].item()
    return petitioner_dict.get(petitioner_id, "Valor desconocido")
def get_winner(winner_id):
    # return winner_catalog.query("clave == @winner_id")["descripción"].item()
    return winner_dict.get(winner_id, "Valor desconocido")
def get_divorce_reason(divorce_reason_id):
    # return divorce_reason_catalog.query("clave == @divorce_reason_id")["descripción"].item()
    return divorce_reason_dict.get(divorce_reason_id, "Valor desconocido")

def get_custody_winner(custody_id):
    return custody_dict.get(custody_id, "Valor desconocido")

def get_parental_authority(pp_id):
    return parental_authority_dict.get(pp_id, "Valor desconocido")
    # return parental_authority_catalog.query("clave == @pp_id")["descripción"].item()
def get_child_maintenance_individual(child_mantenance_id):
    return child_maintenance_dict.get(child_mantenance_id, "Valor desconocido")
    # return child_maintenance_catalog.query("clave == @child_mantenance_id")["descripción"].item()
def get_nationality(nationality_id):
    return nationality_dict.get(nationality_id, "Valor desconocido")
    # return nationality_catalog.query("clave == @nationality_id")["descripción"].item()
def get_marital_status(marital_status_id):
    return marital_status_dict.get(marital_status_id, "Valor desconocido")
    # return marital_status_catalog.query("clave == @marital_status_id")["descripción"].item()
def get_education_level(education_id):
    return education_level_dict.get(education_id, "Valor desconocido")
    # return education_level_catalog.query("clave == @education_id")["descripción"].item()
def get_economic_situation(economic_situation_id):
    return economic_situation_dict.get(economic_situation_id, "Valor desconocido")
    # return economic_situation_catalog.query("clave == @economic_situation_id")["descripción"].item()
def get_dedication(dedication_id):
    return dedication_dict.get(dedication_id, "Valor desconocido")
    # return dedication_catalog.query("clave == @dedication_id")["descripción"].item()
def get_job(job_id):
    return job_dict.get(job_id, "Valor desconocido")
    # return job_catalog.query("clave == @job_id")["descripción"].item()
def get_gender(gender_id):
    return gender_dict.get(gender_id, "Valor desconocido")
    # return gender_catalog.query("clave == @gender_id")["descripción"].item()

data = []

# Get data from a single file
for dataframe in dataframes:
    for _, row in dataframe.iterrows():
        
        data.append(
            {
                "divorce_type": get_divorce_type(row["tipo_div"]),
                "divorce_registration_location":get_location2(row["ent_regis"],row["mun_regis"],row["loc_regis"]),
                "marriage_registration_location":get_location2(row["ent_mat"],row["mun_mat"],row["local_mat"]),
                "marriage_date":get_formated_date(row["dia_mat"],row["mes_mat"],row["anio_mat"]),
                "divorce_petition_date":get_formated_date(row["dia_reg"],row["mes_reg"],row["anio_reg"]),
                "divorce_trial_date":get_formated_date(row["dia_sen"],row["mes_sen"],row["anio_sen"]),
                "divorce_final_order" : get_formated_date(row["dia_eje"],row["mes_eje"],row["anio_eje"]),
                "petitioner":get_petitioner(row["ini_juic"]),
                "winner":get_winner(row["favor"]),
                "divorce_reason":get_divorce_reason(row["causa"]),
                "childs_total":row["hijos"],
                "underage_childs":row["hij_men"],
                "custody":get_custody_winner(row["custodia"]),
                "childs_in_custody":row["cus_hij"],
                "parental_authority":get_parental_authority(row["pat_pot"]),
                "childs_in_parental_authority":row["pat_hij"],
                "child_maintenance":get_child_maintenance_individual(row["pension"]),
                "childs_in_child_maintenance":row["pen_hij"],
                
                # Divorcee 1
                "divorcee_1": {
                    "nationality": get_nationality(row["naci_div1"]),
                    "age": get_age(row["edad_div1"]),
                    "marital_status": get_marital_status(row["eciv_adiv1"]),
                    "location": get_location2(row["ent_rhdiv1"], row["mun_rhdiv1"], row["loc_rhdiv1"]),
                    "education_level": get_education_level(row["escol_div1"]),
                    "economic_situation": get_economic_situation(row["con_acdiv1"]),  # Uncomment if function is available
                    "dedication": get_dedication(row["dedic_div1"]),
                    "job": get_job(row["postr_div1"]),
                    "gender": get_gender(row["sexo_div1"]),
                    "age_at_marriage": get_age(row["edad_mdiv1"])
                },
                # Divorcee 2
                "divorcee_2": {
                    "nationality": get_nationality(row["naci_div2"]),
                    "age": get_age(row["edad_div2"]),
                    "marital_status": get_marital_status(row["eciv_adiv2"]),
                    "location": get_location2(row["ent_rhdiv2"], row["mun_rhdiv2"], row["loc_rhdiv2"]),
                    "education_level": get_education_level(row["escol_div2"]),
                    "economic_situation": get_economic_situation(row["con_acdiv2"]),  # Uncomment if function is available
                    "dedication": get_dedication(row["dedic_div2"]),
                    "job": get_job(row["postr_div2"]),
                    "gender": get_gender(row["sexo_div2"]),
                    "age_at_marriage": get_age(row["edad_mdiv2"])
                } 
            }
        )

    
print(data[0])
print(len(data))
from ElasticSearchProvider import ElasticSearchProvider

#LOAD
try:
    with ElasticSearchProvider() as es:
        response = es.bulk_insert(data=data)  # ID de doc, y doc
        # print(response)
        print(response)
    es_handler = ElasticSearchProvider()
    print("es_handler", es_handler)
except Exception as error:
    print(error)


# print(divorces_in_2023.describe())