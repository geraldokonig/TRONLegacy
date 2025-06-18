# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="Recursos/icone.ico") ]
cx_Freeze.setup(
    name = "TRON: Legacy",
    options={
        "build_exe":{
            "packages":["pygame", "math", "random", "datetime", "json", "tkinter"],
            "include_files":["Recursos", "log.dat"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
