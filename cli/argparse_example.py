import argparse
from pathlib import Path


def _router(directory: Path, validation: bool, connect: bool) -> None:
    print(directory, type(directory))
    print(validation, type(validation))
    print(connect, type(connect))


def main() -> None:
    '''CLI для валидации конфигурационных yaml файлов.
        -h, --help
            Вывод справки
        -d, --directory
            Путь до файлов конфигурация
        -v, --validation
            Валидация конфигураций
        -c, --connect
            Тест конфигураций
    '''
    parser = argparse.ArgumentParser(description='Validate yaml configuration files')
    parser.add_argument('-d', '--directory', default='./', nargs='?', type=Path,
                        help='Directory with configs to validate. Default is current directory.')
    parser.add_argument('-v', '--validation', action='store_true',
                        help='validate configuration files')
    parser.add_argument('-c', '--connect', action='store_true',
                        help='test connections collected in configuretion files')
    args = parser.parse_args()
    try:
        _router(args.directory, args.validation, args.connect)
    except (SyntaxError, NameError, TypeError, ValueError) as e:
        print(f'Validation failed!\n{e}')
        exit(1)
    print('Validation success!')


if __name__ == '__main__':
    main()
