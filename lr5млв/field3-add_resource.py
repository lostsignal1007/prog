import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Параметры симуляции ---
GRID_SIZE = 100      # Размер поля N x N
VIEW_WINDOW = 200    # Сколько поколений одновременно показывать на графике

# Параметры травы (Ресурса)
MAX_GRASS = 1        
P_GRASS_GROW = 0.15  # УВЕЛИЧЕНО (с 0.05): Трава растет быстрее, чтобы прокормить больше зайцев

# Параметры зайцев
INIT_RABBIT_PROB = 0.20  # УВЕЛИЧЕНО (с 0.12): Больше зайцев на старте для еды волкам
P_RABBIT_REPRODUCE = 0.30 # УВЕЛИЧЕНО (с 0.20): Зайцы плодятся быстрее, компенсируя съедение
RABBIT_MAX_ENERGY = 4     # СНИЖЕНО (с 5): Чтобы зайцы сами не перенаселили поле

# Параметры волков
INIT_WOLF_PROB = 0.04    
P_WOLF_STARVE = 0.02      # СНИЖЕНО (с 0.08): Волки почти не умирают «просто так» от случайности
P_WOLF_REPRODUCE = 0.40   # УВЕЛИЧЕНО (с 0.15): Волки гарантированно плодятся, если нашли еду
WOLF_MAX_ENERGY = 20      # УВЕЛИЧЕНО (с 12): Волки могут ОЧЕНЬ долго ходить без еды в поисках жертвы


# Коды существ в логической матрице `grid`
EMPTY = 0
RABBIT = 1
WOLF = 2

# --- Инициализация полей ---
grid = np.random.choice([EMPTY, RABBIT, WOLF], size=(GRID_SIZE, GRID_SIZE), 
                        p=[1 - INIT_RABBIT_PROB - INIT_WOLF_PROB, INIT_RABBIT_PROB, INIT_WOLF_PROB])

# ФОНОВЫЙ СЛОЙ ТРАВЫ: теперь состоит строго из 0 и 1
grass_grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.4, 0.6]).astype(float)

rabbit_energy = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
rabbit_energy[grid == RABBIT] = RABBIT_MAX_ENERGY

wolf_energy = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
wolf_energy[grid == WOLF] = WOLF_MAX_ENERGY

# История для графиков
grass_history = []
rabbit_history = []
wolf_history = []

def update(frame):
    global grid, grass_grid, rabbit_energy, wolf_energy
    
    new_grid = grid.copy()
    new_grass_grid = grass_grid.copy()
    new_rabbit_energy = rabbit_energy.copy()
    new_wolf_energy = wolf_energy.copy()
    
    # Сбор статистики
    total_grass = np.sum(grass_grid == 1)
    rabbits_count = np.sum(grid == RABBIT)
    wolves_count = np.sum(grid == WOLF)
    
    grass_history.append(total_grass)
    rabbit_history.append(rabbits_count)
    wolf_history.append(wolves_count)
    
    # 1. Трава случайно вырастает (0 -> 1) на клетках, где её нет
    grow_mask = (grass_grid == 0) & (np.random.rand(GRID_SIZE, GRID_SIZE) < P_GRASS_GROW)
    new_grass_grid[grow_mask] = 1.0
    
    # 2. Обработка жизненного цикла животных
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            
            # --- ЛОГИКА ЗАЙЦЕВ ---
            if grid[r, c] == RABBIT:
                if new_grass_grid[r, c] == 1.0:
                    new_grass_grid[r, c] = 0.0  # Заяц полностью съедает траву на клетке
                    new_rabbit_energy[r, c] = RABBIT_MAX_ENERGY  
                    
                    dr, dc = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                    nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                    if grid[nr, nc] == EMPTY and np.random.rand() < P_RABBIT_REPRODUCE:
                        new_grid[nr, nc] = RABBIT
                        new_rabbit_energy[nr, nc] = RABBIT_MAX_ENERGY // 2
                else:
                    new_rabbit_energy[r, c] -= 1
                    if new_rabbit_energy[r, c] <= 0:
                        new_grid[r, c] = EMPTY
                    else:
                        dr, dc = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                        nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                        if grid[nr, nc] == EMPTY:
                            new_grid[nr, nc] = RABBIT
                            new_rabbit_energy[nr, nc] = new_rabbit_energy[r, c]
                            new_grid[r, c] = EMPTY
            
            # --- ЛОГИКА ВОЛКОВ ---
            elif grid[r, c] == WOLF:
                rabbit_neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                        if grid[nr, nc] == RABBIT:
                            rabbit_neighbors.append((nr, nc))
                
                if rabbit_neighbors:
                    target_r, target_c = rabbit_neighbors[np.random.choice(len(rabbit_neighbors))]
                    new_grid[target_r, target_c] = WOLF
                    new_wolf_energy[target_r, target_c] = WOLF_MAX_ENERGY
                    
                    if np.random.rand() < P_WOLF_REPRODUCE:
                        new_grid[r, c] = WOLF
                        new_wolf_energy[r, c] = WOLF_MAX_ENERGY // 2
                    else:
                        new_grid[r, c] = EMPTY
                else:
                    new_wolf_energy[r, c] -= 1
                    if new_wolf_energy[r, c] <= 0 or np.random.rand() < P_WOLF_STARVE:
                        new_grid[r, c] = EMPTY
                    else:
                        dr, dc = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                        nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                        if grid[nr, nc] == EMPTY:
                            new_grid[nr, nc] = WOLF
                            new_wolf_energy[nr, nc] = new_wolf_energy[r, c]
                            new_grid[r, c] = EMPTY

    grid = new_grid
    grass_grid = new_grass_grid
    rabbit_energy = new_rabbit_energy
    wolf_energy = new_wolf_energy
    
    # 3. ВИЗУАЛИЗАЦИЯ ТРАВЫ (Фон на левом графике)
    mat.set_data(grass_grid)
    
    # 4. ВИЗУАЛИЗАЦИЯ ЖИВОТНЫХ (Точки поверх травы)
    global rabbit_scatter, wolf_scatter
    if rabbit_scatter: rabbit_scatter.remove()
    if wolf_scatter: wolf_scatter.remove()
    
    r_indices, c_indices = np.where(grid == RABBIT)
    w_indices, w_cols = np.where(grid == WOLF)
    
    rabbit_scatter = ax_map.scatter(c_indices, r_indices, color='#00bfff', s=25, marker='o', label='Зайцы')
    wolf_scatter = ax_map.scatter(w_cols, w_indices, color='#e74c3c', s=35, marker='^', label='Волки')
    
    # 5. ОБНОВЛЕНИЕ ГРАФИКОВ ДИНАМИКИ
    ax_graph.clear()
    ax_graph.plot(rabbit_history, color='#00bfff', linewidth=2, label='Зайцы (ось L)')
    ax_graph.plot(wolf_history, color='#e74c3c', linewidth=2, label='Волки (ось L)')
    ax_graph.set_ylabel("Число животных")
    ax_graph.set_xlabel("Поколения")
    ax_graph.grid(True)
    
    ax2.clear()
    ax2.plot(grass_history, color='#f1c40f', linestyle='--', alpha=0.7, label='Трава (ось R)')
    ax2.set_ylabel("Клеток с травой")
    
    # Ограничение скользящего окна
    if len(rabbit_history) > VIEW_WINDOW:
        ax_graph.set_xlim(len(rabbit_history) - VIEW_WINDOW, len(rabbit_history))
        ax2.set_xlim(len(rabbit_history) - VIEW_WINDOW, len(rabbit_history))
    else:
        ax_graph.set_xlim(0, VIEW_WINDOW)
        ax2.set_xlim(0, VIEW_WINDOW)
        
    ax_graph.set_title(f"Поколение: {frame} | З: {rabbits_count} | В: {wolves_count}")
    
    # Объединение легенд
    lines1, labels1 = ax_graph.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax_graph.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    
    return [mat, rabbit_scatter, wolf_scatter]

# --- Настройка визуализации Matplotlib ---
fig, (ax_map, ax_graph) = plt.subplots(1, 2, figsize=(14, 6))

# Палитра для травы: 0 — темно-серый (нет травы), 1 — чисто желтый (есть трава)
yellow_shades = [
    '#2c2c2c', # 0: Трава съедена
    '#f1c40f'  # 1: Клетка с травой
]
cmap = plt.cm.colors.ListedColormap(yellow_shades)

# Настройка фона карты
mat = ax_map.imshow(grass_grid, cmap=cmap, vmin=0, vmax=MAX_GRASS)
ax_map.axis('off')
ax_map.set_title("Карта ресурсов и животных")

# Глобальные переменные для маркеров существ
rabbit_scatter = None
wolf_scatter = None

# Инициализируем правую ось Y для графиков один раз здесь
ax2 = ax_graph.twinx()

ani = animation.FuncAnimation(fig, update, interval=100, save_count=100, cache_frame_data=False)
plt.show()
