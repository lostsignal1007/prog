import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Параметры симуляции ---
GRID_SIZE = 100       # Размер поля N x N
VIEW_WINDOW = 200    # Сколько поколений одновременно показывать на графике

# Начальные плотности населения
INIT_RABBIT_PROB = 0.25  
INIT_WOLF_PROB = 0.05    

# Вероятности процессов
P_RABBIT_REPRODUCE = 0.20 
P_WOLF_STARVE = 0.15       
WOLF_MAX_ENERGY = 5        
P_WOLF_REPRODUCE = 0.25   # <--- НОВЫЙ ПАРАМЕТР: Вероятность размножения волка при наличии энергии

# Коды клеток на поле
EMPTY = 0
RABBIT = 1
WOLF = 2

# --- Инициализация поля ---
grid = np.random.choice([EMPTY, RABBIT, WOLF], size=(GRID_SIZE, GRID_SIZE), 
                        p=[1 - INIT_RABBIT_PROB - INIT_WOLF_PROB, INIT_RABBIT_PROB, INIT_WOLF_PROB])

energy_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
energy_grid[grid == WOLF] = WOLF_MAX_ENERGY

rabbit_history = []
wolf_history = []

def update(frame):
    global grid, energy_grid
    new_grid = grid.copy()
    new_energy_grid = energy_grid.copy()
    
    # Считаем текущую численность
    rabbits_count = np.sum(grid == RABBIT)
    wolves_count = np.sum(grid == WOLF)
    rabbit_history.append(rabbits_count)
    wolf_history.append(wolves_count)
    
    # Проходим по каждой клетке поля
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            # --- ЛОГИКА ЗАЙЦЕВ ---
            if grid[r, c] == RABBIT:
                dr, dc = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                if grid[nr, nc] == EMPTY and np.random.rand() < P_RABBIT_REPRODUCE:
                    new_grid[nr, nc] = RABBIT
            
            # --- ЛОГИКА ВОЛКОВ ---
            elif grid[r, c] == WOLF:
                # Ищем зайцев вокруг
                neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                        if grid[nr, nc] == RABBIT:
                            neighbors.append((nr, nc))
                
                # Если нашли зайца — волк атакует (ест)
                if neighbors:
                    target_r, target_c = neighbors[np.random.choice(len(neighbors))]
                    new_grid[target_r, target_c] = WOLF
                    new_energy_grid[target_r, target_c] = WOLF_MAX_ENERGY
                    
                    # МЕХАНИКА РАЗМНОЖЕНИЯ:
                    # Если волк сыт и срабатывает вероятность, он оставляет потомка на старом месте
                    if np.random.rand() < P_WOLF_REPRODUCE:
                        new_grid[r, c] = WOLF
                        new_energy_grid[r, c] = WOLF_MAX_ENERGY // 2  # Потомок получает половину энергии
                    else:
                        # Если не размножился, старая клетка пустеет
                        if new_grid[r, c] == WOLF: 
                            new_grid[r, c] = EMPTY
                            new_energy_grid[r, c] = 0
                
                # Если зайцев нет — волк теряет энергию и пытается переместиться
                else:
                    new_energy_grid[r, c] -= 1
                    # Волк умирает от голода или случайной смерти
                    if new_energy_grid[r, c] <= 0 or np.random.rand() < P_WOLF_STARVE:
                        new_grid[r, c] = EMPTY
                        new_energy_grid[r, c] = 0
                    else:
                        # Движение волка на пустую клетку
                        dr, dc = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                        nr, nc = (r + dr) % GRID_SIZE, (c + dc) % GRID_SIZE
                        if grid[nr, nc] == EMPTY:
                            new_grid[nr, nc] = WOLF
                            new_energy_grid[nr, nc] = new_energy_grid[r, c]
                            new_grid[r, c] = EMPTY
                            new_energy_grid[r, c] = 0

    grid = new_grid
    energy_grid = new_energy_grid
    
    # Обновление левого графика (поле клеток)
    mat.set_data(grid)
    
    # Обновление правого графика (динамика популяций)
    ax[1].clear()
    ax[1].plot(rabbit_history, color='green', label='Зайцы')
    ax[1].plot(wolf_history, color='red', label='Волки')
    
    # Настройка скользящего окна для оси X
    if len(rabbit_history) > VIEW_WINDOW:
        ax[1].set_xlim(len(rabbit_history) - VIEW_WINDOW, len(rabbit_history))
    else:
        ax[1].set_xlim(0, VIEW_WINDOW)
        
    ax[1].set_xlabel("Поколения")
    ax[1].set_ylabel("Численность")
    ax[1].set_title(f"Поколение: {frame} | З: {rabbits_count} | В: {wolves_count}")
    ax[1].legend(loc="upper right")
    ax[1].grid(True)
    
    return [mat]

# --- Настройка визуализации Matplotlib ---
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# ax[0] - Левое поле (визуализация клеток)
cmap = plt.cm.colors.ListedColormap(['black', '#2ecc71', '#e74c3c'])
mat = ax[0].imshow(grid, cmap=cmap, vmin=0, vmax=2)
ax[0].axis('off')
ax[0].set_title("Карта популяции")

# Запуск бесконечной анимации
ani = animation.FuncAnimation(fig, update, interval=100, save_count=100)
plt.show()
