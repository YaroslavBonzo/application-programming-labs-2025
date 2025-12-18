import argparse
import pandas as pd
import funcs


def get_args() -> list[str]:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--file",
        type=str,
        help="Path to file.csv",
    )
    parser.add_argument(
        "-o",
        "--out_file",
        type=str,
        help="Path to out_file.csv",
    )
    args = parser.parse_args()

    if args.file is None or args.out_file is None:
        return None
    return [args.file, args.out_file]


def main() -> None:
    """Main function"""

    args = get_args()
    if args is None:
        print("Usage: python main.py -c file.csv -o out_file.csv")
        return

    csv, out = args

    try:
        df = pd.read_csv(csv)
        print(f"Successfully read {len(df)} rows from {csv}")
    except Exception as e:
        print(f"Error: Cannot read {csv}: {e}")
        return

    # 1. Добавляем колонку с доминирующим цветом
    print("Calculating dominant colors...")
    df['dominant_color'] = df["Relative Path"].apply(funcs.get_dominant_color)

    # 2. Добавляем колонку с яркостью
    print("Calculating brightness...")
    df['brightness_value'] = df['dominant_color'].apply(funcs.get_brightness_value)

    # 3. Добавляем колонку с диапазоном яркости
    df['brightness_range'] = df['dominant_color'].apply(funcs.get_brightness_range)

    # 4. Добавляем колонку с цветовой категорией (опционально)
    df['color_category'] = df['dominant_color'].apply(funcs.get_color_category)

    # 5. Сортируем по яркости
    df_sort = funcs.sort_by_column(df, "brightness_value")

    # 6. Показываем и сохраняем гистограммы
    print("Generating histograms...")
    funcs.show_and_save(df_sort)

    # 7. Сохраняем результаты
    try:
        df_sort.to_csv(out, index=False)
        print(f"Results saved to {out}")

        # Выводим статистику
        print("\n=== COLOR ANALYSIS STATISTICS ===")
        print(f"Total images: {len(df)}")
        print(f"Average color: R={df['dominant_color'].apply(lambda x: x[0]).mean():.1f}, "
              f"G={df['dominant_color'].apply(lambda x: x[1]).mean():.1f}, "
              f"B={df['dominant_color'].apply(lambda x: x[2]).mean():.1f}")
        print(f"Average brightness: {df['brightness_value'].mean():.1f}")

        # Распределение по категориям
        print("\nColor categories distribution:")
        for category, count in df['color_category'].value_counts().items():
            percentage = (count / len(df)) * 100
            print(f"  {category}: {count} images ({percentage:.1f}%)")

    except Exception as e:
        print(f"Cannot save dataframe: {e}")


if __name__ == "__main__":
    main()