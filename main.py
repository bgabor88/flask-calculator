#!.\venv\Scripts\python.exe
from flask import Flask, render_template, url_for, request

app = Flask(__name__)
NUMBER_1 = ""
NUMBER_2 = ""
LAST_OP = ""
OPERATOR = ""
DISPLAY_1 = []
DISPLAY_2 = []
FIRST = False


@app.route('/', methods=['POST', 'GET'])
def main():
    global DISPLAY_1, DISPLAY_2, NUMBER_1, NUMBER_2, OPERATOR, FIRST
    if request.method == 'POST':
        if 'AC' in list(request.form.keys()):
            all_clear()
        elif 'DEL' in list(request.form.keys()):
            delete()
        elif 'number' in list(request.form.keys()):
            set_number()
        elif 'operation' in list(request.form.keys()):
            set_operation()
        elif 'equals' in list(request.form.keys()):
            equals()
    else:
        DISPLAY_1 = []
        DISPLAY_2 = []

    return render_template('main.html', result_1=DISPLAY_1, result_2=DISPLAY_2)


def calculator(number_1, number_2, operator):
    if operator == "+":
        return str(number_1 + number_2)
    elif operator == "-":
        return str(number_1 - number_2)
    elif operator == "*":
        return str(number_1 * number_2)
    else:
        if number_2 != 0:
            return str(format_number((number_1 / float(number_2))))
        else:
            return "ZERO division error"


def delete():
    global FIRST, DISPLAY_1, DISPLAY_2, NUMBER_1, NUMBER_2, OPERATOR
    if len(DISPLAY_1) >= 1:
        del DISPLAY_1[-1]
        if len(DISPLAY_1) == 1:
            if DISPLAY_1[0] == "-":
                DISPLAY_1 = []
        if len(DISPLAY_1) == 0:
            OPERATOR = ""
            DISPLAY_1 = list(NUMBER_1)
            DISPLAY_2 = []
            NUMBER_1 = ""
    else:
        DISPLAY_1 = list(NUMBER_1)
        DISPLAY_2 = []
        NUMBER_1 = ""


def set_number():
    global FIRST, DISPLAY_1, DISPLAY_2, NUMBER_1, NUMBER_2, OPERATOR
    if request.form['number'] == '.' and '.' not in DISPLAY_1:
        DISPLAY_1.append(request.form['number'])
    elif request.form['number'] != '.':
        if request.form['number'] == '0' and len(DISPLAY_1) < 3:
            if len(DISPLAY_1) == 1:
                if DISPLAY_1[0] != '0':
                    DISPLAY_1.append(request.form['number'])
            elif len(DISPLAY_1) == 2:
                if DISPLAY_1[0] == '-' and DISPLAY_1[1] != '0':
                    DISPLAY_1.append(request.form['number'])
                elif DISPLAY_1[0] == '.':
                    DISPLAY_1.append(request.form['number'])
                elif DISPLAY_1[0] == '0' and DISPLAY_1[1] == '.':
                    DISPLAY_1.append(request.form['number'])
            else:
                DISPLAY_1.append(request.form['number'])
        else:
            DISPLAY_1.append(request.form['number'])


def all_clear():
    global FIRST, DISPLAY_1, DISPLAY_2, NUMBER_1, NUMBER_2, OPERATOR
    DISPLAY_1 = []
    DISPLAY_2 = []
    NUMBER_1 = ""
    NUMBER_2 = ""
    OPERATOR = ""
    FIRST = False


def set_operation():
    global FIRST, DISPLAY_1, DISPLAY_2, NUMBER_1, NUMBER_2, OPERATOR, LAST_OP
    if len(DISPLAY_1) > 0 and len(DISPLAY_2) > 0:
        if LAST_OP == request.form['operation']:
            equals()
        else:
            OPERATOR = request.form['operation']
            NUMBER_2 = "".join(DISPLAY_1)
            digit_1 = int(NUMBER_1) if '.' not in NUMBER_1 else float(NUMBER_1)
            digit_2 = int(NUMBER_2) if '.' not in NUMBER_2 else float(NUMBER_2)
            result = calculator(digit_1, digit_2, LAST_OP)
            NUMBER_1 = result
            DISPLAY_2 = list(result)
            DISPLAY_1 = []
            DISPLAY_2.append(" ")
            DISPLAY_2.append(OPERATOR)
    elif len(DISPLAY_1) > 0 and DISPLAY_1[-1] != "-":
        OPERATOR = request.form['operation']
        NUMBER_1 = "".join(DISPLAY_1)
        DISPLAY_2.append(NUMBER_1)
        DISPLAY_1 = []
        DISPLAY_2.append(" ")
        DISPLAY_2.append(OPERATOR)
        LAST_OP = OPERATOR
    elif request.form['operation'] == "-" and len(DISPLAY_1) == 0 and "-" not in DISPLAY_1:
        DISPLAY_1.append(request.form['operation'])
    elif len(DISPLAY_1) == 0:
        OPERATOR = request.form['operation']
        LAST_OP = OPERATOR
        DISPLAY_2[-1] = OPERATOR


def equals():
    global FIRST, DISPLAY_1, DISPLAY_2, NUMBER_1, NUMBER_2, OPERATOR
    if not FIRST:
        FIRST = True
        NUMBER_2 = "".join(DISPLAY_1)
        digit_1 = int(NUMBER_1) if '.' not in NUMBER_1 else float(NUMBER_1)
        digit_2 = int(NUMBER_2) if '.' not in NUMBER_2 else float(NUMBER_2)
        result = calculator(digit_1, digit_2, OPERATOR)
        DISPLAY_2.append(" ")
        DISPLAY_2.append(NUMBER_2)
        DISPLAY_2.append(" =")
        DISPLAY_1 = list(result)
    else:
        DISPLAY_2 = ""
        DISPLAY_2 = DISPLAY_1
        NUMBER_1 = "".join(DISPLAY_1)
        DISPLAY_2.append(" ")
        DISPLAY_2.append(OPERATOR)
        DISPLAY_2.append(" ")
        DISPLAY_2.append(NUMBER_2)
        DISPLAY_2.append(" =")
        digit_1 = int(NUMBER_1) if '.' not in NUMBER_1 else float(NUMBER_1)
        digit_2 = int(NUMBER_2) if '.' not in NUMBER_2 else float(NUMBER_2)
        result = calculator(digit_1, digit_2, OPERATOR)
        DISPLAY_1 = list(result)


def format_number(number):
  if number % 1 == 0:
    return int(number)
  else:
    return number


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
