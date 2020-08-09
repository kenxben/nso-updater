
creds_file = "keys/verifynso-dd9a44c0a761.json"

# test
# targetID = "14L_TE8SluitJBsnNCJCvZHeSH2jh_-9_W8tIIUPV6sk"

# real target
targetID = "1fM4UC4Y9uxkzJxIKFnW0h_YVAlB5qQ2cQdl4VuxmnnA"

urls = [
    "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7458&force=1",
    "http://permisosfuncionamiento.controlsanitario.gob.ec/consulta/reporte2excel_new.php",

    # This link redirects to not found:
    # "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=1636&force=1",
    # Since it is a fixed file we use instead a mirror:

    "https://drive.google.com/uc?export=download&id=1yFfLJabAQyEbHanLIWMKweH22dwq_T65",
    "https://www.controlsanitario.gob.ec/wp-content/plugins/download-monitor/download.php?id=7457&force=1"

]

# To guarantee
col_renamer = {
    "No. de Registro Sanitario": "Codigo de identificacion de NSO",
    "Fecha de Emisión": "Fecha de emisión del certificado",
    "Fecha de Vigencia": "Fecha de vigencia de  NSO",
    "Titular del Producto": "Titular del producto",
    "Nombre del Producto": "Nombre del producto",
    "Marca del producto": "Marca del producto",
    "MARCA" : "Marca del producto",
    "PRODUCTO": "Nombre del producto",
    "SOLICITANTE": "Titular del producto",
    "R. SANITARIO": "Codigo de identificacion de NSO",
    "EMISION": "Fecha de emisión del certificado",
    "CADUCIDAD": "Fecha de vigencia de  NSO",
    "Fecha de vigencia de código de identificacion de NSO": "Fecha de vigencia de  NSO",
}

# Columns must be sorted in this order to be read by api engine
cols_sorted = [
    "Codigo de identificacion de NSO",
    "Nombre del producto",
    "Marca del producto",
    "Titular del producto",
    "Fecha de emisión del certificado",
    "Fecha de vigencia de  NSO",
]