import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import os


def get_dominant_color(image_path: str) -> list[int]:
    """Calculate dominant color as average of every channel"""
    try:
        if not os.path.exists(image_path):
            print(f"Warning: File {image_path} not found")
            return [0, 0, 0]

        with Image.open(image_path) as img:
            img = img.convert('RGB')
            pixels = np.array(img)
            r_mean = pixels[:, :, 0].mean()
            g_mean = pixels[:, :, 1].mean()
            b_mean = pixels[:, :, 2].mean()

        return [int(r_mean), int(g_mean), int(b_mean)]
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return [0, 0, 0]


def get_brightness_value(rgb: list[int]) -> float:
    """Calculate brightness value from RGB"""
    if not rgb or len(rgb) < 3:
        return 0.0

    brightness = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return brightness


def get_brightness_range(rgb: list[int]) -> str:
    """Calculate brightness range for visualizing distribution"""
    brightness = get_brightness_value(rgb)
    range_start = (brightness // 50) * 50
    range_start = max(0, min(range_start, 250))
    return f"{int(range_start)}-{int(range_start + 49)}"


def get_color_category(rgb: list[int]) -> str:
    """Определяет цветовую категорию по доминирующему каналу"""
    if not rgb or len(rgb) < 3:
        return "Unknown"

    r, g, b = rgb

    # Находим самый сильный канал
    max_value = max(r, g, b)

    # Определяем порог (20 единиц) для уверенности в доминировании
    if max_value == r and r > g + 20 and r > b + 20:
        return "Red Dominant"
    elif max_value == g and g > r + 20 and g > b + 20:
        return "Green Dominant"
    elif max_value == b and b > r + 20 and b > g + 20:
        return "Blue Dominant"
    elif r > 200 and g > 200 and b < 100:
        return "Yellow/Orange"
    elif r > 200 and b > 200 and g < 100:
        return "Purple/Violet"
    elif r > 180 and g > 100 and g < 150 and b < 100:
        return "Orange/Warm"
    elif abs(r - g) < 30 and abs(g - b) < 30:
        if max_value > 200:
            return "White/Gray"
        elif max_value < 80:
            return "Black/Dark Gray"
        else:
            return "Gray"
    else:
        return "Mixed Colors"


def sort_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Sorting DataFrame by column"""
    return df.sort_values(by=column)


def filter_by_range(df: pd.DataFrame, range_str: str) -> pd.DataFrame:
    """Filter DataFrame by brightness range"""
    return df[df['brightness_range'] == range_str]


def show_and_save(df_sort: pd.DataFrame) -> None:
    """Show and save histograms of dominant color distribution"""

    if df_sort.empty:
        print("No data to display")
        return

    # Создаём фигуру с 4 графиками (3 для цветов + 1 общий)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # ============================================
    # 1. Извлекаем значения R, G, B
    # ============================================

    red_values = []
    green_values = []
    blue_values = []

    for color_list in df_sort['dominant_color']:
        if isinstance(color_list, list) and len(color_list) >= 3:
            red_values.append(color_list[0])
            green_values.append(color_list[1])
            blue_values.append(color_list[2])

    # Настройки для гистограмм
    bins = 20
    alpha = 0.7

    # ============================================
    # 2. ГИСТОГРАММА КРАСНОГО КАНАЛА
    # ============================================
    axes[0, 0].hist(red_values, bins=bins, color='red', alpha=alpha,
                    edgecolor='black', density=False)
    axes[0, 0].set_xlabel('Red Channel Value (0-255)')
    axes[0, 0].set_ylabel('Number of Images')
    axes[0, 0].set_title('Red Channel Distribution')
    axes[0, 0].grid(True, alpha=0.3)

    if red_values:
        mean_red = sum(red_values) / len(red_values)
        axes[0, 0].axvline(mean_red, color='darkred', linestyle='--',
                           linewidth=2, label=f'Mean: {mean_red:.1f}')
        axes[0, 0].legend()

    # ============================================
    # 3. ГИСТОГРАММА ЗЕЛЁНОГО КАНАЛА
    # ============================================
    axes[0, 1].hist(green_values, bins=bins, color='green', alpha=alpha,
                    edgecolor='black', density=False)
    axes[0, 1].set_xlabel('Green Channel Value (0-255)')
    axes[0, 1].set_ylabel('Number of Images')
    axes[0, 1].set_title('Green Channel Distribution')
    axes[0, 1].grid(True, alpha=0.3)

    if green_values:
        mean_green = sum(green_values) / len(green_values)
        axes[0, 1].axvline(mean_green, color='darkgreen', linestyle='--',
                           linewidth=2, label=f'Mean: {mean_green:.1f}')
        axes[0, 1].legend()

    # ============================================
    # 4. ГИСТОГРАММА СИНЕГО КАНАЛА
    # ============================================
    axes[1, 0].hist(blue_values, bins=bins, color='blue', alpha=alpha,
                    edgecolor='black', density=False)
    axes[1, 0].set_xlabel('Blue Channel Value (0-255)')
    axes[1, 0].set_ylabel('Number of Images')
    axes[1, 0].set_title('Blue Channel Distribution')
    axes[1, 0].grid(True, alpha=0.3)

    if blue_values:
        mean_blue = sum(blue_values) / len(blue_values)
        axes[1, 0].axvline(mean_blue, color='darkblue', linestyle='--',
                           linewidth=2, label=f'Mean: {mean_blue:.1f}')
        axes[1, 0].legend()

    # ============================================
    # 5. СОВМЕЩЁННАЯ ГИСТОГРАММА ВСЕХ КАНАЛОВ
    # ============================================
    axes[1, 1].hist([red_values, green_values, blue_values],
                    bins=bins,
                    color=['red', 'green', 'blue'],
                    alpha=0.6,
                    edgecolor='black',
                    label=['Red', 'Green', 'Blue'],
                    density=False)

    axes[1, 1].set_xlabel('Channel Value (0-255)')
    axes[1, 1].set_ylabel('Number of Images')
    axes[1, 1].set_title('Combined RGB Distribution')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()

    # ============================================
    # 6. НАСТРОЙКА И СОХРАНЕНИЕ
    # ============================================
    plt.suptitle('Dominant Color Distribution Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()

    try:
        plt.savefig("dominant_color_histogram.png", dpi=150, bbox_inches='tight')
        print("Histogram saved as: dominant_color_histogram.png")
    except Exception as e:
        print(f"Cannot save histogram: {e}")

    # ============================================
    # 7. ДОПОЛНИТЕЛЬНАЯ ГИСТОГРАММА: ЦВЕТОВЫЕ КАТЕГОРИИ
    # ============================================
    plt.figure(figsize=(12, 6))

    color_counts = df_sort['color_category'].value_counts()

    # Раскрашиваем столбцы в соответствующие цвета
    colors = []
    color_map = {
        'Red Dominant': 'red',
        'Green Dominant': 'green',
        'Blue Dominant': 'blue',
        'Yellow/Orange': 'orange',
        'Orange/Warm': 'darkorange',
        'Purple/Violet': 'purple',
        'White/Gray': 'lightgray',
        'Gray': 'gray',
        'Black/Dark Gray': 'dimgray',
        'Mixed Colors': 'skyblue',
        'Unknown': 'black'
    }

    for category in color_counts.index:
        colors.append(color_map.get(category, 'gray'))

    bars = plt.bar(color_counts.index, color_counts.values,
                   color=colors, edgecolor='black', alpha=0.8)

    plt.xlabel('Color Category')
    plt.ylabel('Number of Images')
    plt.title('Distribution by Color Categories')
    plt.xticks(rotation=45, ha='right')

    # Добавляем значения над столбцами
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()

    try:
        plt.savefig("color_categories.png", dpi=150, bbox_inches='tight')
        print("Color categories chart saved as: color_categories.png")
    except Exception as e:
        print(f"Cannot save color categories chart: {e}")

    plt.show()