import random
import copy
import heapq
import matplotlib.pyplot as plt

# ==========================================
# 1. ГЕНЕРАЦИЯ КАРТ
# ==========================================

def generate_random_map(n):
    """Случайная карта n x n со значениями от 1 до 9"""
    return [[random.randint(1, 9) for _ in range(n)] for _ in range(n)]

def generate_topography_map(n):
    """Плавная (топографическая) карта n x n на основе сглаживания соседей"""
    raw = [[random.randint(1, 9) for _ in range(n)] for _ in range(n)]
    smooth = [[0 for _ in range(n)] for _ in range(n)]
    
    for r in range(n):
        for c in range(n):
            vals = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < n and 0 <= c + dc < n:
                        vals.append(raw[r + dr][c + dc])
            smooth[r][c] = int(round(sum(vals) / len(vals)))
            if smooth[r][c] < 1: smooth[r][c] = 1
            if smooth[r][c] > 9: smooth[r][c] = 9
    return smooth

def generate_100x100_preset_map():
    """Карта 100х100, где искусственно проложен дешевый путь лесенкой (по 10 шагов)"""
    n = 100
    grid = [[random.randint(7, 9) for _ in range(n)] for _ in range(n)]
    
    curr_r, curr_c = n - 1, 0
    grid[curr_r][curr_c] = 1
    
    for step in range(10):
        for _ in range(10):
            if curr_c < n - 1:
                curr_c += 1
                grid[curr_r][curr_c] = 1
        for _ in range(10):
            if curr_r > 0:
                curr_r -= 1
                grid[curr_r][curr_c] = 1
                
    return grid

# ==========================================
# 1.5. ТОЧНЫЙ РАСЧЕТ ИДЕАЛЬНОГО ПУТИ (ДИЙКСТРА)
# ==========================================

def find_absolute_shortest_path(grid, n):
    """Находит абсолютно минимальную стоимость пути по клеткам (вверх/вниз/влево/вправо)"""
    start = (n - 1, 0)
    finish = (0, n - 1)
    
    # ИСПРАВЛЕНО: Правильный доступ к элементу матрицы по координатам start[0] и start[1]
    start_cost = grid[start[0]][start[1]]
    queue = [(start_cost, start)]
    distances = {start: start_cost}
    
    while queue:
        current_dist, (r, c) = heapq.heappop(queue)
        
        if (r, c) == finish:
            return current_dist
            
        if current_dist > distances.get((r, c), float('inf')):
            continue
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                distance = current_dist + grid[nr][nc]
                if distance < distances.get((nr, nc), float('inf')):
                    distances[(nr, nc)] = distance
                    heapq.heappush(queue, (distance, (nr, nc)))
                    
    return distances.get(finish, float('inf'))

# ==========================================
# 2. СУЩЕСТВО И ЛОГИКА ДВИЖЕНИЯ
# ==========================================

class Individual:
    def __init__(self, n, points=None):
        self.n = n
        self.start = (n - 1, 0)
        self.finish = (0, n - 1)
        
        if points is None:
            self.points = [self.start]
            # Умная инициализация: создаем от 5 до 12 промежуточных точек
            # Точки распределяем последовательно по оси X, добавляя небольшой случайный шум по Y
            num_intermediates = random.randint(5, 12)
            for i in range(1, num_intermediates + 1):
                # Пропорционально продвигаемся от старта к финишу
                progress = i / (num_intermediates + 1)
                
                # Идеальная диагональная траектория
                ideal_c = int(progress * (n - 1))
                ideal_r = int((1 - progress) * (n - 1))
                
                # Добавляем "коридорный" шум (+/- 15 клеток), чтобы не подсказывать идеальный путь напрямую,
                # но сузить область поиска для ГА
                noise_r = random.randint(-15, 15)
                noise_c = random.randint(-15, 15)
                
                r = max(0, min(n - 1, ideal_r + noise_r))
                c = max(0, min(n - 1, ideal_c + noise_c))
                self.points.append((r, c))
                
            self.points.append(self.finish)
        else:
            self.points = points
        
        self.fitness = float('inf')

    def get_full_path(self):
        if not self.points:
            return []
        full_path = [self.points[0]]
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            curr_r, curr_c = p1
            target_r, target_c = p2
            
            step_c = 1 if target_c >= curr_c else -1
            while curr_c != target_c:
                curr_c += step_c
                full_path.append((curr_r, curr_c))
                
            step_r = 1 if target_r >= curr_r else -1
            while curr_r != target_r:
                curr_r += step_r
                full_path.append((curr_r, curr_c))
        return full_path

    def calculate_fitness(self, grid):
        full_path = self.get_full_path()
        total_cost = 0
        for r, c in full_path:
            if not (0 <= r < self.n and 0 <= c < self.n):
                total_cost += 5000  
            else:
                total_cost += grid[r][c]
        self.fitness = total_cost
        return self.fitness

# ==========================================
# 3. ОПЕРАТОРЫ ГЕНЕТИЧЕСКОГО АЛГОРИТМА
# ==========================================

def selection_tournament(population, k=3):
    selected = random.sample(population, k)
    return min(selected, key=lambda ind: ind.fitness)




def mutate_optimized(individual, mutation_rate, radius):
    """Модифицированная функция мутации, принимающая динамический радиус"""
    if random.random() > mutation_rate:
        return copy.deepcopy(individual)

    new_points = copy.deepcopy(individual.points)
    
    if len(new_points) <= 2:
        mutation_type = 'add'
    elif len(new_points) == 3:
        mutation_type = random.choice(['change', 'add'])
    else:
        mutation_type = random.choice(['change', 'add', 'remove'])

    if mutation_type == 'change':
        idx = random.randint(1, len(new_points) - 2)
        r, c = new_points[idx]
        new_r = max(0, min(individual.n - 1, r + random.randint(-radius, radius)))
        new_c = max(0, min(individual.n - 1, c + random.randint(-radius, radius)))
        new_points[idx] = (new_r, new_c)
        
    elif mutation_type == 'add':
        idx = random.randint(1, len(new_points) - 1)
        p1 = new_points[idx-1]  # Кортеж (r1, c1)
        p2 = new_points[idx]    # Кортеж (r2, c2)
        
        shift = max(1, radius // 2)
        
        # ИСПРАВЛЕНО: считаем среднее для r и c по отдельности
        mid_r = (p1[0] + p2[0]) // 2 + random.randint(-shift, shift)
        mid_c = (p1[1] + p2[1]) // 2 + random.randint(-shift, shift)
        
        new_r = max(0, min(individual.n - 1, mid_r))
        new_c = max(0, min(individual.n - 1, mid_c))
        new_points.insert(idx, (new_r, new_c))
        
    elif mutation_type == 'remove':
        idx = random.randint(1, len(new_points) - 2)
        new_points.pop(idx)

    return Individual(individual.n, new_points)



def crossover(parent1, parent2):
    if len(parent1.points) <= 3 or len(parent2.points) <= 3:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
    cut1 = random.randint(1, len(parent1.points) - 2)
    cut2 = random.randint(1, len(parent2.points) - 2)
    
    child1_points = parent1.points[:cut1] + parent2.points[cut2:]
    child2_points = parent2.points[:cut2] + parent1.points[cut1:]
    
    if len(child1_points) >= 2:
        child1_points[0] = parent1.start
        child1_points[-1] = parent1.finish
    if len(child2_points) >= 2:
        child2_points[0] = parent1.start
        child2_points[-1] = parent1.finish
    
    return Individual(parent1.n, child1_points), Individual(parent1.n, child2_points)

# ==========================================
# 4. ГЛАВНЫЙ ЗАПУСК АЛГОРИТМА
# ==========================================

def run_genetic_algorithm(grid, n, pop_size=300, generations=500):
    # Создаем начальную популяцию
    population = [Individual(n) for _ in range(pop_size)]
    
    for ind in population:
        ind.calculate_fitness(grid)
        
    best_individual = copy.deepcopy(min(population, key=lambda ind: ind.fitness))

    for gen in range(generations):
        # ---------------------------------------------------------
        # ОПТИМИЗАЦИЯ ГИПЕРПАРАМЕТРОВ НА ОСНОВЕ ТЕКУЩЕГО ПОКОЛЕНИЯ
        # ---------------------------------------------------------
        # Прогресс от 0.0 (старт) до 1.0 (финиш)
        progress = gen / generations
        
        # 1. Адаптивный шанс мутации: падает с 60% до 15%
        current_mutation_rate = 0.60 - (0.45 * progress)
        
        # 2. Адаптивный радиус мутации: сужается с каждым поколением
        if progress < 0.3:
            current_radius = 12  # Грубый поиск траектории
        elif progress < 0.7:
            current_radius = 5   # Схождение к лесенке
        else:
            current_radius = 1   # Ювелирная подгонка ступенек под единицы
            
        # 3. Адаптивное давление отбора (размер турнира): растет с 3 до 6
        current_k = 3 if progress < 0.5 else 6
        
        # Сортируем текущее поколение по фитнесу (лучшие в начале)
        population.sort(key=lambda ind: ind.fitness)
        
        new_population = []
        
        # 4. Расширенный элитизм: сохраняем топ-5% лучших без изменений
        num_elites = max(1, int(pop_size * 0.05))
        for i in range(num_elites):
            new_population.append(copy.deepcopy(population[i]))
        
        # Заполняем остаток популяции потомками
        while len(new_population) < pop_size:
            # Передаем адаптированный размер турнира current_k
            p1 = selection_tournament(population, k=current_k)
            p2 = selection_tournament(population, k=current_k)
            
            ch1, ch2 = crossover(p1, p2)
            
            # Передаем в мутацию измененные на ходу параметры
            ch1 = mutate_optimized(ch1, mutation_rate=current_mutation_rate, radius=current_radius)
            ch2 = mutate_optimized(ch2, mutation_rate=current_mutation_rate, radius=current_radius)
            
            ch1.calculate_fitness(grid)
            ch2.calculate_fitness(grid)
            
            new_population.append(ch1)
            if len(new_population) < pop_size:
                new_population.append(ch2)
                
        population = new_population
        current_best = min(population, key=lambda ind: ind.fitness)
        
        if current_best.fitness < best_individual.fitness:
            best_individual = copy.deepcopy(current_best)
            
        if gen % max(1, (generations // 5)) == 0 or gen == generations - 1:
            print(f"Поколение {gen:03d} (Мутация: {current_mutation_rate:.2f}, Радиус: {current_radius}): Лучшая стоимость = {best_individual.fitness}")
            
    return best_individual





# ==========================================
# 5. ВИЗУАЛИЗАЦИЯ КАРТЫ И ПУТИ
# ==========================================

def visualize_map_and_path(grid, individual, ideal_cost, title="Карта пути"):
    n = individual.n
    full_path = individual.get_full_path()
    
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap='YlOrBr', origin='upper', vmin=1, vmax=9)
    plt.colorbar(label='Стоимость клетки (высота рельефа)')
    
    path_x = [c for r, c in full_path]
    path_y = [r for r, c in full_path]
    
    plt.plot(path_x, path_y, color='blue', linewidth=2.5, label='Путь ГА', zorder=2)
    
    pts_x = [c for r, c in individual.points]
    pts_y = [r for r, c in individual.points]
    plt.scatter(pts_x, pts_y, color='red', s=40, edgecolors='black', label='Точки хромосомы', zorder=3)
    
    plt.scatter(0, n - 1, color='lime', marker='*', s=200, edgecolors='black', label='Старт', zorder=4)
    plt.scatter(n - 1, 0, color='green', marker='*', s=200, edgecolors='black', label='Финиш', zorder=4)
    
    if n <= 15:
        for r in range(n):
            for c in range(n):
                plt.text(c, r, str(grid[r][c]), va='center', ha='center', color='black', fontsize=10, weight='bold')

    plt.title(f"{title}\nРезультат ГА = {individual.fitness} | Идеал = {ideal_cost}", fontsize=12)
    plt.xlabel("Координата X (Столбцы)")
    plt.ylabel("Координата Y (Строки)")
    plt.legend(loc='upper left')
    plt.grid(True, which='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.show()

# ==========================================
# ЗАПУСК И СРАВНЕНИЕ РЕЗУЛЬТАТОВ
# ==========================================
if __name__ == "__main__":
    print("Запуск расчетов Генетического Алгоритма...")
    # Сценарий 1: 10х10
    map_10 = generate_topography_map(10)
    best_10 = run_genetic_algorithm(map_10, n=10, pop_size=100, generations=200)
    ideal_10 = find_absolute_shortest_path(map_10, 10)
    # Сценарий 2: 100х100
    map_100 = generate_100x100_preset_map()
    best_100 = run_genetic_algorithm(map_100, n=100, pop_size=200, generations=500)
    ideal_100 = 199
    # Сравнительный отчет в консоли
    print("\n" + "="*50)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ ЭФФЕКТИВНОСТИ ГА")
    print("="*50)
    print(f"{'Параметр':<20} | {'Карта 10х10':<12} | {'Карта 100х100':<12}")
    print("-"*50)
    print(f"{'Результат ГА':<20} | {best_10.fitness:<12} | {best_100.fitness:<12}")
    print(f"{'Идеальный путь':<20} | {ideal_10:<12} | {ideal_100:<12}")
    dev_10 = ((best_10.fitness - ideal_10) / ideal_10) * 100
    dev_100 = ((best_100.fitness - ideal_100) / ideal_100) * 100
    print(f"{'Отклонение от идеала':<20} | {dev_10:.1f}%        | {dev_100:.1f}%")
    print("="*50)
    # Показ графиков
    visualize_map_and_path(map_10, best_10, ideal_10, title="Задание 1: Топографическая карта 10x10")
    visualize_map_and_path(map_100, best_100, ideal_100, title="Задание 2: Карта 100x100 с искусственным пресетом")