
from pyscript import document
from pyodide.ffi import create_proxy

display = document.querySelector("#display")

current = "0"
previous = None
operator = None
new_number = False


def calculate():
    global current, previous, operator, new_number

    if previous is None or operator is None or new_number:
        return

    a = previous
    b = float(current)

    if operator == "+":
        result = a + b

    elif operator == "−":
        result = a - b

    elif operator == "×":
        result = a * b

    elif operator == "÷":
        if previous == 0 and b == 0:
            current = "Error"
            previous = None
            operator = None
            new_number = True
            return
        
        if b == 0:
            current = "Error"
            previous = None
            operator = None
            new_number = True
            return

        result = a / b

    current = format(result, ".10g")
    previous = None
    operator = None
    new_number = True


def press(event):
    global current, previous, operator, new_number

    key = event.currentTarget.textContent.strip()

    if key == "AC":
        current = "0"
        previous = None
        operator = None
        new_number = False

    elif key == "DEL":
        current = current[:-1] or "0"

        if current in ["-", "Erro"]:
            current = "0"

    elif key == "=":
        calculate()

    elif key in ["+", "−", "×", "÷"]:
        if current != "Error":
            calculate()

            if current != "Error":
                previous = float(current)
                operator = key
                new_number = True

    elif key == "%":
        if current != "Error":
            current = format(float(current) / 100, ".10g")

    elif key == "±":
        if current != "Error":
            current = format(-float(current), ".10g")

    else:
        if new_number or current == "Error":
            current = "0"
            new_number = False

        if key == ".":
            if "." not in current:
                current += "."

        elif len(current) < 12:
            if current == "0":
                current = key
            else:
                current += key

    display.textContent = current


# Connect Python to every calculator button
click_handler = create_proxy(press)

for button in document.querySelectorAll(".buttons button"):
    button.addEventListener("click", click_handler)
