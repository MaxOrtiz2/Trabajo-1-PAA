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

def main():
    lista_tareas = cargar_tareas("tareas.txt")
    lista_recursos = cargar_recursos("recursos.txt")

    lista_tareas = ordenar_tareas_duracion(lista_tareas)

    print("Tareas ordenadas de mayor a menor duracion:")
    for tarea in lista_tareas:
        print(tarea.id_tarea, tarea.duracion, tarea.categoria)

    print(f"Listos para procesar {len(lista_tareas)} tareas y {len(lista_recursos)} recursos.")

    print("Recursos compatibles para cada tarea")
    for tarea in lista_tareas:
        print(f"\nTarea {tarea.id_tarea} ({tarea.categoria}):")
        for recursos in lista_recursos:
             if recurso_para_tarea(tarea, recursos):
                 print(f"  - Compatible con {recursos.id_recurso}")


if __name__ == "__main__":
    main()
