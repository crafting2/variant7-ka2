# ============================================================
# НКА для языка L = {a^n : n >= 0} U {b^n a : n >= 1}
# Вариант 7б. Алфавит {a, b}. Состояний: 4.
# Табличное представление автомата.
# ============================================================

# ---------- 1. АЛФАВИТ ----------
ALPHABET = ['a', 'b']


# ---------- 2. ТАБЛИЦА ПЕРЕХОДОВ НКА ----------
# TRANS_NFA[state][symbol_index] = список состояний (возможно пустой)
# symbol_index: 0 -> 'a', 1 -> 'b'
TRANS_NFA = [
    # q0: по 'a' -> {q1}, по 'b' -> {q2}
    [[1], [2]],
    # q1: по 'a' -> {q1}, по 'b' -> {}
    [[1], []],
    # q2: по 'a' -> {q3}, по 'b' -> {q2}
    [[3], [2]],
    # q3: тупиковое, переходов нет
    [[], []],
]


# ---------- 3. НАЧАЛЬНОЕ И ДОПУСКАЮЩИЕ СОСТОЯНИЯ ----------
START_STATE = 0
N_STATES = 4
ACCEPTING = [False] * N_STATES
ACCEPTING[0] = True  # q0 — для epsilon
ACCEPTING[1] = True  # q1 — для a^n, n>=1
ACCEPTING[3] = True  # q3 — для b^n a, n>=1


# ---------- 4. ВСПОМОГАТЕЛЬНЫЕ ПРОЦЕДУРЫ ----------

def symbol_index(ch):
    """Индекс символа в алфавите. Без строковых функций."""
    if ch == 'a':
        return 0
    if ch == 'b':
        return 1
    return -1


def state_name(q):
    """Имя состояния."""
    return "q" + str(q)


def to_symbols(s):
    """Строка -> список символов. Без строковых функций."""
    result = []
    for ch in s:
        result.append(ch)
    return result


def is_valid_string(chars):
    """Проверка, что все символы в алфавите."""
    for ch in chars:
        if ch != 'a' and ch != 'b':
            return False
    return True


# ---------- 5. ЭМУЛЯЦИЯ НКА ----------
# Ключевая идея: держим МНОЖЕСТВО активных состояний.
# После каждого символа заменяем множество на объединение
# всех состояний, достижимых из текущих по этому символу.

def run_nfa(chars, verbose=False):
    """
    Эмуляция НКА по списку символов.
    Возвращает True, если после чтения всей цепочки
    хотя бы одно активное состояние — допускающее.
    """
    current = [START_STATE]
    if verbose:
        print("  Старт: {" + ", ".join(state_name(q) for q in current) + "}")

    for ch in chars:
        idx = symbol_index(ch)
        if idx < 0:
            if verbose:
                print("  Ошибка: символ '" + ch + "' вне алфавита")
            return False

        # Объединение переходов из всех текущих состояний
        nxt = []
        for q in current:
            for p in TRANS_NFA[q][idx]:
                # добавляем без дубликатов
                found = False
                for x in nxt:
                    if x == p:
                        found = True
                        break
                if not found:
                    nxt.append(p)

        current = nxt

        if verbose:
            if current:
                print("  '" + ch + "': {" +
                      ", ".join(state_name(q) for q in current) + "}")
            else:
                print("  '" + ch + "': {} (тупик)")
        if not current:
            break

    accepted = False
    for q in current:
        if ACCEPTING[q]:
            accepted = True
            break

    if verbose:
        print("  Финал: {" + ", ".join(state_name(q) for q in current) +
              "}  ->  " + ("Accept" if accepted else "Reject"))
    return accepted


# ---------- 6. ВЫВОД ТАБЛИЦЫ ПЕРЕХОДОВ ----------

def print_transition_table():
    print("=" * 60)
    print("Таблица переходов НКА (вариант 7б)")
    print("=" * 60)
    print("+------+--------+--------+------------+")
    print("|  N   |   'a'  |   'b'  | Допускающее|")
    print("+------+--------+--------+------------+")
    for q in range(N_STATES):
        a_set = TRANS_NFA[q][0]
        b_set = TRANS_NFA[q][1]
        if a_set:
            a_str = "{" + ",".join(state_name(x) for x in a_set) + "}"
        else:
            a_str = "{}"
        if b_set:
            b_str = "{" + ",".join(state_name(x) for x in b_set) + "}"
        else:
            b_str = "{}"
        acc = "да" if ACCEPTING[q] else "нет"
        print("| {0:>4} | {1:>6} | {2:>6} | {3:>10} |".format(
            q, a_str, b_str, acc))
    print("+------+--------+--------+------------+")
    print("Начальное состояние: " + state_name(START_STATE))
    acc_list = []
    for q in range(N_STATES):
        if ACCEPTING[q]:
            acc_list.append(state_name(q))
    print("Допускающие: " + ", ".join(acc_list))
    print()


# ---------- 7. ДЕМОНСТРАЦИЯ ----------

def demo():
    print_transition_table()

    tests = [
        "", "a", "aa", "aaa", "aaaa",
        "ba", "bba", "bbba",
        "b", "bb", "bbb",
        "ab", "aab", "baa", "bbaa", "bab", "abba",
    ]

    print("=" * 60)
    print("Результаты распознавания (аналог JFLAP Multiple Run)")
    print("=" * 60)
    print("+----------------------+------------+")
    print("|        Input         |   Result   |")
    print("+----------------------+------------+")

    for s in tests:
        chars = to_symbols(s)
        if not is_valid_string(chars):
            print("| {0:<20} | {1:<10} |".format(s, "INVALID"))
            continue
        accepted = run_nfa(chars, verbose=False)
        verdict = "Accept" if accepted else "Reject"
        shown = s if s != "" else "epsilon"
        print("| {0:<20} | {1:<10} |".format(shown, verdict))
    print("+----------------------+------------+")
    print()

    # Пошаговая трасса для 'bba' (должно принять)
    print("=" * 60)
    print("Пошаговая трасса для 'bba'")
    print("=" * 60)
    run_nfa(to_symbols("bba"), verbose=True)
    print()

    # Пошаговая трасса для 'b' (должно отвергнуть)
    print("=" * 60)
    print("Пошаговая трасса для 'b'")
    print("=" * 60)
    run_nfa(to_symbols("b"), verbose=True)
    print()

    # Пошаговая трасса для 'aab' (должно отвергнуть)
    print("=" * 60)
    print("Пошаговая трасса для 'aab'")
    print("=" * 60)
    run_nfa(to_symbols("aab"), verbose=True)
    print()


if __name__ == "__main__":
    demo()