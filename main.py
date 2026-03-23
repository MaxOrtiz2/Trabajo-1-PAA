import sys

class Tarea:
    def __init__(self, id_tarea: str, duracion: int, categoria: str):
        self.id_tarea: str = id_tarea
        self.duracion: int = duracion
        self.categoria: str = categoria
        self.tiempo_inicio: int = 0 
        self.recurso_asignado: str = ""

class Recurso:
    def __init__(self, id_recurso: str, categorias: list[str]):
        self.id_recurso: str = id_recurso
        self.categorias_soportadas: list[str] = categorias
        self.tiempo_disponible: int = 0

def cargar_tareas(nombre: str) -> list[Tarea]:
    tareas = []
    with open(nombre, "r") as f:
        for fila in f:
            d = fila.strip().split(",")
            tareas.append(Tarea(d[0], int(d[1]), d[2]))
    return tareas

def cargar_recursos(nombre: str) -> list[Recurso]:
    recursos = []
    with open(nombre, "r") as f:
        for fila in f:
            d = fila.strip().split(",")
            recursos.append(Recurso(d[0], d[1:]))
    return recursos

def ordenar_tareas_duracion(tareas: list[Tarea]) -> list[Tarea]:
    return sorted(tareas, key=lambda tarea: tarea.duracion, reverse=True)

def recurso_para_tarea(tarea: Tarea, recurso: Recurso) -> bool:
    return tarea.categoria in recurso.categorias_soportadas

def guardar_resultado(tareas: list[Tarea], nombre_archivo: str):
    with open(nombre_archivo, "w") as f:
        for t in tareas:
            fila = f"{t.id_tarea},{t.recurso_asignado},{t.tiempo_inicio},{t.tiempo_inicio + t.duracion}\n"
            f.write(fila)

def main() -> None:
    makespan_objetivo: int = int(sys.argv[1])

    lista_tareas = cargar_tareas("tareas_EP.txt")
    lista_recursos = cargar_recursos("recursos_EP.txt")
    lista_tareas = ordenar_tareas_duracion(lista_tareas)
        
    for tarea in lista_tareas:
        recurso_elegido = None
        mejor_tiempo = float('inf')
        for recurso in lista_recursos:
            if recurso_para_tarea(tarea, recurso):
                if recurso.tiempo_disponible < mejor_tiempo:
                    mejor_tiempo = recurso.tiempo_disponible
                    recurso_elegido = recurso
        if recurso_elegido:
            tarea.recurso_asignado = recurso_elegido.id_recurso
            tarea.tiempo_inicio = recurso_elegido.tiempo_disponible
            recurso_elegido.tiempo_disponible += tarea.duracion

    guardar_resultado(lista_tareas, "output.txt")
    print("Cronograma generado en output.txt")

    makespan_final = 0
    for t in lista_tareas:
        tiempo_termino = t.tiempo_inicio + t.duracion
        if tiempo_termino > makespan_final:
            makespan_final = tiempo_termino

    print(f"\n--- Resumen de Ejecución ---")
    print(f"Makespan Objetivo: {makespan_objetivo}")
    print(f"Makespan Obtenido: {makespan_final}")

if __name__ == "__main__":
    main()
