# ============================================================
# ДКА, допускающий цепочки над {0,1}, в которых
# число нулей делится на 5, а число единиц делится на 3
# Вариант 7а
# ============================================================

# ---------- 1. АЛФАВИТ ----------
ALPHABET = ['0', '1']


# ---------- 2. ТАБЛИЦА ПЕРЕХОДОВ ----------
# Нумерация: q = j*5 + i, где i = остаток нулей mod 5, j = остаток единиц mod 3.
# Мнемоника: '0' — шаг вправо (i+1 mod 5), '1' — шаг вниз (j+1 mod 3).
TRANS = [
    # q0  (0,0)
    [1, 5],
    # q1  (1,0)
    [2, 6],
    # q2  (2,0)
    [3, 7],
    # q3  (3,0)
    [4, 8],
    # q4  (4,0)
    [0, 9],
    # q5  (0,1)
    [6, 10],
    # q6  (1,1)
    [7, 11],
    # q7  (2,1)
    [8, 12],
    # q8  (3,1)
    [9, 13],
    # q9  (4,1)
    [5, 14],
    # q10 (0,2)
    [11, 0],
    # q11 (1,2)
    [12, 1],
    # q12 (2,2)
    [13, 2],
    # q13 (3,2)
    [14, 3],
    # q14 (4,2)
    [10, 4],
]

# ---------- 3. НАЧАЛЬНОЕ И ДОПУСКАЮЩИЕ СОСТОЯНИЯ ----------
START_STATE = 0
N_STATES = 15
ACCEPTING = [False] * N_STATES
ACCEPTING[0] = True  # только (0,0)


# ---------- 4. ВСПОМОГАТЕЛЬНЫЕ ПРОЦЕДУРЫ ----------

def symbol_index(ch):
    """Индекс символа в алфавите. Без строковых функций."""
    if ch == '0':
        return 0
    if ch == '1':
        return 1
    return -1


def state_name(q):
    """Имя состояния как пара (i,j)."""
    i = q % 5
    j = q // 5
    return "(" + str(i) + "," + str(j) + ")"


def to_symbols(s):
    """Строка -> список символов. Без строковых функций."""
    result = []
    for ch in s:
        result.append(ch)
    return result


def is_valid_string(chars):
    """Проверка: все ли символы в алфавите."""
    for ch in chars:
        if ch != '0' and ch != '1':
            return False
    return True


# ---------- 5. ЭМУЛЯЦИЯ ДКА ----------

def run_dfa(chars, verbose=False):
    """Прогон ДКА по списку символов. Возвращает True/False."""
    state = START_STATE
    if verbose:
        print("  Старт: " + state_name(state))
    for ch in chars:
        idx = symbol_index(ch)
        if idx < 0:
            if verbose:
                print("  Ошибка: символ '" + ch + "' вне алфавита")
            return False
        prev = state
        state = TRANS[state][idx]
        if verbose:
            print("  '" + ch + "': " + state_name(prev) +
                  " -> " + state_name(state))
    if verbose:
        print("  Финал: " + state_name(state) +
              ("  [допускающее]" if ACCEPTING[state] else "  [не допускающее]"))
    return ACCEPTING[state]


# ---------- 6. ВЫВОД ТАБЛИЦЫ АВТОМАТА ----------

def print_transition_table():
    print("=" * 62)
    print("Таблица переходов ДКА (вариант 7а)")
    print("=" * 62)
    print("+------+----------+--------+--------+------------+")
    print("|  №   | Состояние|   '0'  |   '1'  | Допускающее|")
    print("+------+----------+--------+--------+------------+")
    for q in range(N_STATES):
        acc = "да" if ACCEPTING[q] else "нет"
        print("| {0:>4} | {1:>8} | {2:>6} | {3:>6} | {4:>10} |".format(
            q, state_name(q), TRANS[q][0], TRANS[q][1], acc))
    print("+------+----------+--------+--------+------------+")
    print("Начальное состояние: " + state_name(START_STATE))
    print()


# ---------- 7. ДЕМОНСТРАЦИЯ ----------

def demo():
    print_transition_table()

    tests = [
        "", "00000", "111", "00000111", "0", "1",
        "0000", "11", "0000000000", "111111",
        "0101010101", "0000011100000",
    ]

    print("=" * 62)
    print("Результаты распознавания (аналог JFLAP Multiple Run)")
    print("=" * 62)
    print("+----------------------+------------+")
    print("|        Input         |   Result   |")
    print("+----------------------+------------+")

    for s in tests:
        chars = to_symbols(s)
        if not is_valid_string(chars):
            print("| {0:<20} | {1:<10} |".format(s, "INVALID"))
            continue
        accepted = run_dfa(chars, verbose=False)
        verdict = "Accept" if accepted else "Reject"
        shown = s if s != "" else "ε"
        print("| {0:<20} | {1:<10} |".format(shown, verdict))
    print("+----------------------+------------+")
    print()

    # Пошаговая трасса для одной цепочки
    print("=" * 62)
    print("Пошаговая трасса для '00000111'")
    print("=" * 62)
    run_dfa(to_symbols("00000111"), verbose=True)
    print()


if __name__ == "__main__":
    demo()