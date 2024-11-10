import json
from MaquinaT import TuringMachine
import os

# Función para leer las cadenas de entrada
def cargar_cadenas_entrada(filepath):
    with open(filepath, 'r') as f:
        cadenas = [line.strip() for line in f if line.strip()]
    return cadenas

# Cargar las especificaciones de la máquina de Turing del JSON
def cargar_especificaciones(filepath):
    with open(filepath, 'r') as f:
        especificaciones = json.load(f)
    return especificaciones

# Función para simular la máquina de Turing con las cadenas y guardar las configuraciones
def simular_cadena(turing_machine, cadenas, output_prefix):
    for i, cadena in enumerate(cadenas, start=1):
        turing_machine.load_tape(cadena)
        configuraciones = turing_machine.run()

        # Guardar configuraciones en un archivo de salida en la carpeta "outputs"
        filename = f'outputs/{output_prefix}_{i}.txt'
        turing_machine.save_configurations(filename, configuraciones)

        # Verificar el estado final de la máquina y agregar el resultado
        if turing_machine.current_state == turing_machine.accept_state:
            result = f"La cadena {cadena} es aceptada."
        elif turing_machine.current_state == turing_machine.reject_state:
            result = f"La cadena {cadena} es rechazada."
        else:
            result = f"La cadena {cadena} entra en un loop."

        # Añadir la información de aceptación, rechazo o loop al final del archivo
        with open(filename, 'a') as f:
            f.write(f"{result}\n")

        print(f"Configuraciones guardadas en {filename}")

# Función principal
def main():
    # Leer especificaciones de la máquina de Turing desde el archivo JSON
    especificaciones = cargar_especificaciones('MDT.json')
    
    # Crear una instancia de la máquina de Turing con las especificaciones cargadas
    turing_machine = TuringMachine(
        states=especificaciones['states'],
        alphabet=especificaciones['alphabet'],
        tape_alphabet=especificaciones['tape_alphabet'],
        transitions=especificaciones['transitions'],
        start_state=especificaciones['start_state'],
        accept_state=especificaciones['accept_state'],
        reject_state=especificaciones['reject_state'],
        blank_symbol=especificaciones['blank_symbol']
    )
    
    # Cadenas de aceptación
    cadenas_aceptacion = cargar_cadenas_entrada('inputs/aceptacion.txt')

    # Cadenas de rechazo
    cadenas_rechazo = cargar_cadenas_entrada('inputs/rechazo.txt')

    # Cadenas de loop
    cadenas_loop = cargar_cadenas_entrada('inputs/loop.txt')

    # Simular y guardar configuraciones para las cadenas de aceptación
    simular_cadena(turing_machine, cadenas_aceptacion, 'configuraciones_aceptacion')
    
    # Simular y guardar configuraciones para las cadenas de rechazo
    simular_cadena(turing_machine, cadenas_rechazo, 'configuraciones_negacion')
    
    # Simular y guardar configuraciones para las cadenas de loop
    simular_cadena(turing_machine, cadenas_loop, 'configuraciones_loop')
    
    

if __name__ == "__main__":
    # Crear carpeta de outputs si no existe
    os.makedirs('outputs', exist_ok=True)
    main()
