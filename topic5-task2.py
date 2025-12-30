def binary_search_with_upper_bound(arr, x):
    """
    Двійковий пошук для відсортованого масиву з дробовими числами.
    
    Параметри:
    arr - відсортований список (масив) чисел
    x - значення для пошуку
    
    Повертає:
    Кортеж (кількість_ітерацій, верхня_межа)
    - кількість_ітерацій: скільки ітерацій знадобилось
    - верхня_межа: найменший елемент >= x, або None якщо такого немає
    """
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None
    
    while low <= high:
        iterations += 1
        mid = (high + low) // 2
        
        # Якщо знайшли точне значення
        if arr[mid] == x:
            upper_bound = arr[mid]
            return (iterations, upper_bound)
        
        # Якщо середній елемент менший за x, шукаємо у правій половині
        elif arr[mid] < x:
            low = mid + 1
        
        # Якщо середній елемент більший за x, шукаємо у лівій половині
        else:
            upper_bound = arr[mid]  # Зберігаємо як потенційну верхню межу
            high = mid - 1
    
    return (iterations, upper_bound)


# Приклади використання
arr1 = [1.5, 2.3, 4.7, 6.1, 8.9, 10.2, 15.5]
x1 = 6.1
result = binary_search_with_upper_bound(arr1, x1)
print(result)
x2 = 7.5
result = binary_search_with_upper_bound(arr1, x2)
print(result)