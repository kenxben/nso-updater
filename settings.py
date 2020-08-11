
GSHEET_CREDS = "keys/verifynso-dd9a44c0a761.json"
EMAIL_CREDS = "keys/email_creds.yaml"

# test
# targetID = "14L_TE8SluitJBsnNCJCvZHeSH2jh_-9_W8tIIUPV6sk"

# real target
TARGET_ID = "1fM4UC4Y9uxkzJxIKFnW0h_YVAlB5qQ2cQdl4VuxmnnA"

URLS = [
    {
        "label": "Cosmeticos",
        "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7458&force=1",
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
        "label": "Productos higienicos",
        "url": "https://drive.google.com/uc?export=download&id=1yFfLJabAQyEbHanLIWMKweH22dwq_T65",
    },
    {
        "label": "Productos higienicos",
        "url": "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7457&force=1",
    },
]

# Rules to rename variables to be the same
COL_RENAMER = {
    "No. de Registro Sanitario": "Codigo de identificacion de NSO",
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