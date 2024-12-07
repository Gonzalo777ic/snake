import turtle
import time
import random
import tkinter as tk
from tkinter import simpledialog
from ai_model import AIModule  # Importa el modelo de IA

# Configuración inicial
delay = 0.1
score = 0
high_score = 0
difficulty = 1  # Nivel inicial de dificultad

# Instancia del módulo de IA
ai_module = AIModule()

# Configuración de la pantalla
wn = turtle.Screen()
wn.title("Snake Game with AI-Driven Math Questions")
wn.bgcolor("#F0C808")
wn.setup(width=600, height=600)
wn.tracer(0)

# Configuración de la serpiente y comida
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#DD1C1A")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#1B998B")
food.penup()
food.goto(0, 100)

segments = []

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Mostrar "Isique Production"
def show_isique_production():
    isique = turtle.Turtle()
    isique.speed(0)
    isique.color("black")
    isique.penup()
    isique.hideturtle()
    isique.goto(0, 0)
    isique.write("Isique Production", align="center", font=("Courier", 36, "bold"))
    time.sleep(7)  # Mostrar el mensaje por 2 segundos
    isique.clear()

# Llamar a la función antes de iniciar el juego
show_isique_production()

# Función para dibujar los límites del área de juego
def draw_border():
    border = turtle.Turtle()
    border.speed(0)
    border.color("black")
    border.penup()
    border.goto(-290, 290)
    border.pendown()
    for _ in range(4):
        border.forward(580)  # Dibuja un cuadrado de 600x600
        border.right(90)
    border.hideturtle()

# Agregar una marca de agua
def add_watermark():
    watermark = turtle.Turtle()
    watermark.speed(0)
    watermark.color("gray")
    watermark.penup()
    watermark.hideturtle()
    watermark.goto(-270, -270)  # Ajusta la posición según sea necesario
    watermark.write("Isique Production", align="left", font=("Courier", 12, "italic"))

# Llamar a la función para mostrar la marca de agua
add_watermark()

# Llamar a la función para dibujar los límites una sola vez
draw_border()

# Actualiza el puntaje de manera eficiente
def update_score():
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))



# Funciones de movimiento
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Crear la ventana Tkinter solo una vez
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

def ask_math_question():
    global difficulty
    num1 = random.randint(1, 10 * difficulty)
    num2 = random.randint(1, 10 * difficulty)
    operation = random.choice(["+", "-", "*", "/"])

    # Calcular el resultado y la pregunta basada en la operación
    if operation == "+":
        answer = num1 + num2
        question = f"Cuánto es {num1} + {num2}?"
        operation_type = "addition"
    elif operation == "-":
        answer = num1 - num2
        question = f"Cuánto es {num1} - {num2}?"
        operation_type = "subtraction"
    elif operation == "*":
        answer = num1 * num2
        question = f"Cuánto es {num1} * {num2}?"
        operation_type = "multiplication"
    elif operation == "/":
        answer = round(num1 / num2, 2)
        question = f"Cuánto es {num1} / {num2}?"
        operation_type = "division"

    # Mostrar la pregunta sin crear una nueva ventana cada vez
    start_time = time.time()
    user_answer = simpledialog.askfloat("Math Question", question)
    end_time = time.time()

    time_taken = end_time - start_time
    correct = user_answer == answer

    # Registrar el desempeño y ajustar la dificultad
    ai_module.registrar_desempeno(correct, time_taken, difficulty, operation_type, max(len(str(abs(num1))), len(str(abs(num2)))))
    difficulty = ai_module.ajustar_dificultad(time_taken, difficulty, operation_type, max(len(str(abs(num1))), len(str(abs(num2)))))
    
    return correct

# Finalmente, destruir la ventana cuando ya no se necesite
root.quit()



# Teclado
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Bucle principal
while True:
    wn.update()

    # Colisión con bordes
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)

        segments.clear()
        score = max(0, score - 20)  # Penaliza con -20 puntos
        delay = 0.1

        # Pregunta matemática para revivir
        if ask_math_question():
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
        else:
            pen.clear()
            pen.write("Incorrect! Penalty applied!", align="center", font=("Courier", 24, "normal"))
            # Continúa el juego sin reiniciar del todo

    # Colisión con comida
    if head.distance(food) < 20:
        food.goto(random.randint(-290, 290), random.randint(-290, 290))

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#E84855")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001
        score += 10

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Mover segmentos del cuerpo
    for index in range(len(segments) - 1, 0, -1):
        segments[index].goto(segments[index - 1].xcor(), segments[index - 1].ycor())

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Colisión con el cuerpo
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for segment in segments:
                segment.goto(1000, 1000)

            segments.clear()
            score = max(0, score - 20)  # Penaliza con -20 puntos
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()
