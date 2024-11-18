
import argparse

def main():
    parser = argparse.ArgumentParser(description='Rozpoznanie i rozwiązania równania matematycznego z obrazu')
    parser.add_argument('-s', '--source', required=True, help='Path to image')
    args = parser.parse_args()

    print(f'Źródło zdjęcia: {args.source}')


if __name__ == "__main__":
    main()