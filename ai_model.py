import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Archivo donde se registrarán los datos del jugador
DATA_FILE = "data/player_data.json"

# Modelo de aprendizaje automático
class AIModule:
    def __init__(self):
        self.model = RandomForestRegressor()  # Usar RandomForestRegressor
        self.data = self.load_data()
        self.train_model()

    def load_data(self):
        # Cargar datos desde el archivo o inicializar con valores ficticios
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = [json.loads(line) for line in file]
            return data
        else:
            initial_data = [
                {"correct": True, "time": 2.0, "difficulty": 1, "operation_type": "addition", "digits": 1},
                {"correct": False, "time": 5.0, "difficulty": 1, "operation_type": "division", "digits": 1}
            ]
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, "w") as file:
                for entry in initial_data:
                    file.write(json.dumps(entry) + "\n")
            return initial_data

    def encode_operation(self, operation_type):
        # Convertir el tipo de operación en un valor numérico
        operations = {"addition": 1, "subtraction": 2, "multiplication": 3, "division": 4}
        return operations.get(operation_type, 0)

    def train_model(self):
        # Entrenar el modelo con los datos actuales
        if len(self.data) < 5:  # Necesitamos al menos 5 registros para entrenar
            print("Insuficientes datos para entrenar el modelo.")
            return

        # Crear las características y la variable objetivo
        X = [
            [d["time"], d["difficulty"], self.encode_operation(d["operation_type"]), d["digits"]]
            for d in self.data
        ]
        y = [1 if d["correct"] else 0 for d in self.data]

        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)
            print("Modelo entrenado exitosamente.")
        except Exception as e:
            print(f"Error al entrenar el modelo: {e}")

    def ajustar_dificultad(self, tiempo_respuesta, dificultad_actual, operation_type, digits):
        operation_encoded = self.encode_operation(operation_type)

        try:
            prediccion = self.model.predict([[tiempo_respuesta, dificultad_actual, operation_encoded, digits]])[0]
            print(f"Predicción del modelo: {prediccion:.2f} (Tiempo: {tiempo_respuesta}, Dificultad: {dificultad_actual}, Operación: {operation_type}, Dígitos: {digits})")
        except Exception as e:
            print(f"Error en la predicción: {e}")
            return dificultad_actual  # Mantener dificultad actual si falla

        # Ajustar dificultad suavemente
        if prediccion > 0.9:  # Desempeño sobresaliente
            incremento = 1.01
        elif prediccion > 0.7:  # Buen desempeño
            incremento = 0.777
        elif prediccion < 0.3:  # Mal desempeño
            incremento = -0.7
        else:  # Desempeño promedio
            incremento = 0

        # Aplicar incremento con suavizado
        nueva_dificultad = dificultad_actual + incremento
        nueva_dificultad = max(1, round(nueva_dificultad, 1))  # Asegurar dificultad >= 1 y permitir decimales

        print(f"Dificultad ajustada suavemente de {dificultad_actual} a {nueva_dificultad}")
        return nueva_dificultad



    def registrar_desempeno(self, correcto, tiempo, dificultad, operation_type, digits):
        # Agregar nuevos datos y guardar en el archivo
        nuevo_dato = {
            "correct": correcto,
            "time": tiempo,
            "difficulty": dificultad,
            "operation_type": operation_type,
            "digits": digits
        }
        self.data.append(nuevo_dato)

        # Guardar datos en el archivo
        with open(DATA_FILE, "a") as file:
            file.write(json.dumps(nuevo_dato) + "\n")

        # Reentrenar el modelo dinámicamente
        self.train_model()
