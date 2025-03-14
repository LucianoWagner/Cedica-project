from src import calculator


def main():
    num1 = float(input("Escribe el primer número: "))
    num2 = float(input("Escribe el segundo número: "))
    operator = input("Escribe el operador (+, -, *, /): ")
    result = calculator.calculate(num1, num2, operator)
    print(f"El resultado es: {result}")


if __name__ == "__main__":
    main()
