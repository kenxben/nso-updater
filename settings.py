
GSHEET_CREDS = "keys/verifynso-dd9a44c0a761.json"
EMAIL_CREDS = "keys/email_creds.yaml"

# test
# targetID = "14L_TE8SluitJBsnNCJCvZHeSH2jh_-9_W8tIIUPV6sk"

# real target
TARGET_ID = "1fM4UC4Y9uxkzJxIKFnW0h_YVAlB5qQ2cQdl4VuxmnnA"

URLS = [
    {
        "label": "Cosmeticos",
        # "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7458&force=1",

        # cambio de url 2020-09-17
        # "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7770&force=1",

        # cambio de url 2020-11-12
        # "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7929&force=1",

        # cambio de url 2021-01-04
        # "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=8119&force=1",

        # cambio de url 2021-06-22
        "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=8729&force=1",
    },
    {
        "label": "Cosmeticos",  # new D833 system
        "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=8728&force=1"
    },
    {
        "label": "Cosmeticos",  # old inh (mirror)
        "url": "https://drive.google.com/uc?export=download&id=1gCD2U4yIt-j-bTklq5sJPSnCxwIUCc5k",
    },
    {
        "label": "Medicamentos",
        "url": "http://permisosfuncionamiento.controlsanitario.gob.ec/consulta/reporte2excel_new.php",
    },

    # This link redirects to not found:
    # {
    # "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=1636&force=1"
    # },
    # Since it is a fixed file we use instead a mirror:
    {
        "label": "Productos higienicos",  # old inh (mirror)
        # "url": "https://drive.google.com/uc?export=download&id=1yFfLJabAQyEbHanLIWMKweH22dwq_T65",
        "url": "https://drive.google.com/uc?export=download&id=1Lrycp2q4WeCSWtgSKjY84OIn0HoZyhTX",
    },

    {
        "label": "Productos higienicos",
        # "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7769&force=1",

        # Cambio 5 ene 2021, redirecciona a gdrive
        # "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=8118&force=1"
        "url": "https://drive.google.com/uc?export=download&id=1BlL6tLn2wMRmeHKrSy3z-TuHM55_YYRp"
    },
]

# Rules to rename variables to be the same
COL_RENAMER = {
    "No. de Registro Sanitario": "Codigo de identificacion de NSO",
    "Codigo de identificación de NSO": "Codigo de identificacion de NSO",
    "Codigo de identificacion de NSO": "Codigo de identificacion de NSO",
    "Código de identificación de NSO": "Codigo de identificacion de NSO",
    "Fecha de Emisión": "Fecha de emisión del certificado",
    "Fecha de Vigencia": "Fecha de vigencia de  NSO",
    "Titular del Producto": "Titular del producto",
    "Nombre del Producto": "Nombre del producto",
    "Marca del producto": "Marca del producto",
    "MARCA": "Marca del producto",
    "PRODUCTO": "Nombre del producto",
    "SOLICITANTE": "Titular del producto",
    "R. SANITARIO": "Codigo de identificacion de NSO",
    "EMISION": "Fecha de emisión del certificado",
    "CADUCIDAD": "Fecha de vigencia de  NSO",
    "Fecha de vigencia de código de identificacion de NSO": "Fecha de vigencia de  NSO",
    "Fecha de vigencia de código de identificación de NSO": "Fecha de vigencia de  NSO",
}

# Columns must be sorted in this order to be read by api engine
COLS_SORTED = [
    "Codigo de identificacion de NSO",
    "Nombre del producto",
    "Marca del producto",
    "Titular del producto",
    "Fecha de emisión del certificado",
    "Fecha de vigencia de  NSO",
    "Tipo de producto",
]