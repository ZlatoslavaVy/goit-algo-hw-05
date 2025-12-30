import timeit


# --- 1. Алгоритм пошуку Кнута-Морріса-Пратта (KMP) ---
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


# --- 2. Алгоритм пошуку Боєра-Мура ---
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


# --- 3. Алгоритм пошуку Рабіна-Карпа ---
def polynomial_hash(s, base, modulus):
    hash_value = 0
    for char in s:
        hash_value = (hash_value * base + ord(char)) % modulus
    return hash_value

def rabin_karp_search(text, pattern):
    substring_length = len(pattern)
    main_string_length = len(text)
    if main_string_length < substring_length:
        return -1
    
    base = 256 
    modulus = 101 
    
    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)
    
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i+substring_length] == pattern:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1


# Функція для вимірювання часу виконання
def measure_time(algorithm, text, pattern, number=1000):
    """
    Вимірює час виконання алгоритму
    number - кількість повторень для точнішого вимірювання
    """
    time = timeit.timeit(lambda: algorithm(text, pattern), number=number)
    return time / number  # Повертаємо середній час одного виконання


# Завантаження файлів
try:
    with open("стаття 1.txt", "r", encoding="utf-8") as file1:
        main_string1 = file1.read()

    with open("стаття 2.txt", "r", encoding="utf-8") as file2:
        main_string2 = file2.read()
    
except FileNotFoundError as e:
    print("Помилка: Файли не знайдено. Створіть 'стаття 1.txt' та 'стаття 2.txt'")
    exit()

# Визначаємо підрядки для пошуку
real_pattern = "алгоритм"       # Той, що точно є
fake_pattern = "словоякогонема" # Вигаданий

# Словник для зберігання результатів
results = {
    'Стаття 1': {},
    'Стаття 2': {}
}

# Алгоритми для тестування
algorithms = {
    'Боєра-Мура': boyer_moore_search,
    'Кнута-Морріса-Пратта': kmp_search,
    'Рабіна-Карпа': rabin_karp_search
}

# Тексти для тестування
texts = {
    'Стаття 1': main_string1,
    'Стаття 2': main_string2
}

# Патерни для тестування
patterns = {
    'Реальний підрядок': real_pattern,
    'Вигаданий підрядок': fake_pattern
}

print("\n🔍 ПОЧАТОК ТЕСТУВАННЯ АЛГОРИТМІВ ПОШУКУ\n")

# Виконуємо тестування
for text_name, text in texts.items():
    print(f"\n{'='*80}")
    print(f"📄 {text_name}")
    print(f"{'='*80}\n")
    
    results[text_name] = {}
    
    for pattern_name, pattern in patterns.items():
        print(f"\n  🔎 Пошук: {pattern_name} ('{pattern}')")
        print(f"  {'-'*76}\n")
        
        results[text_name][pattern_name] = {}
        
        for algo_name, algo_func in algorithms.items():
            # Вимірюємо час
            time = measure_time(algo_func, text, pattern, number=1000)
            
            # Перевіряємо результат пошуку
            position = algo_func(text, pattern)
            
            results[text_name][pattern_name][algo_name] = time
            
            # Виводимо результат
            status = f"✓ Знайдено на позиції {position}" if position != -1 else "✗ Не знайдено"
            print(f"    {algo_name:25s}: {time*1000:.6f} мс  [{status}]")
        
        # Визначаємо найшвидший алгоритм для цього патерну
        fastest = min(results[text_name][pattern_name].items(), key=lambda x: x[1])
        print(f"\n    ⚡ Найшвидший: {fastest[0]} ({fastest[1]*1000:.6f} мс)")


# Підсумкові результати
print(f"\n\n{'='*80}")
print("📊 ПІДСУМКОВІ РЕЗУЛЬТАТИ")
print(f"{'='*80}\n")

# Середній час для кожного алгоритму по всіх тестах
avg_times = {algo: [] for algo in algorithms.keys()}

for text_name in results:
    for pattern_name in results[text_name]:
        for algo_name in results[text_name][pattern_name]:
            avg_times[algo_name].append(results[text_name][pattern_name][algo_name])

print("Середній час виконання (по всіх тестах):\n")
for algo_name in sorted(avg_times.keys(), key=lambda x: sum(avg_times[x])/len(avg_times[x])):
    avg = sum(avg_times[algo_name]) / len(avg_times[algo_name])
    print(f"  {algo_name:25s}: {avg*1000:.6f} мс")

overall_fastest = min(avg_times.items(), key=lambda x: sum(x[1])/len(x[1]))
print(f"\n🏆 ЗАГАЛЬНИЙ ПЕРЕМОЖЕЦЬ: {overall_fastest[0]}")
print(f"\n{'='*80}")