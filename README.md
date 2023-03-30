# Вертикализация видео

В этом репозитории лежит набор скриптов, которые облегчат работу над решеним задачи вертикализации видео.

Здесь реализован бейзлайн, который всегда вырезает центральную часть кадра, какого бы размера не было видео.

Предполагается, что у вас есть ссылка на файл с датасетом, и вы можете его скачать. Из соображений конфиденциальности мы не будем публиковать ссылку здесь.

## Что тут есть?

Реализация алгоритма кропа находится в файле `video_verticalization/model.py`.
Если вы хотите заменить бейзлайн на свой алгоритм, отредактируйте класс `Verticalizer`.

Скрипт запуска ветикализации одиночного видео находится в файле `video_verticalization/verticalize.py`.
Вот какие у него есть аргументы:

```bash
verticalize [-h]
    --input_video_path INPUT_VIDEO_PATH 
    --input_features_path INPUT_FEATURES_PATH
    --output_dir_path OUTPUT_DIR_PATH
    [--visualize]

arguments:
  -h, --help            show this help message and exit
  --input_video_path INPUT_VIDEO_PATH
                        Path to input video.
  --input_features_path INPUT_FEATURES_PATH
                        Path to json file with features.
  --output_dir_path OUTPUT_DIR_PATH
                        Path to the result folder.
  --visualize           If set, save cropped video along with crop coordinates.
```

Скрипт, котторый прогоняет вертикализацию находится в файле `video_verticalization/verticalize.py`.

```bash
evaluate [-h] 
    --validation_set VALIDATION_SET_DIR
    --videos VIDEOS_DIR
    --results_dir RESULTS_DIR
    [--visualize]

arguments:
  -h, --help            show this help message and exit
  --validation_set VALIDATION_SET_DIR
                        Path to input video.
  --videos VIDEOS_DIR   Path to json file with features.
  --results_dir RESULTS_DIR
                        Path to the result folder.
  --visualize           If set, save cropped video along with crop coordinates.
```

## Как это запустить?

Проще всего это сделать через [Docker](https://www.docker.com/).

Для этого сначала нужно собрать контейнер. Для этого, находясь в директории проекта выполнте:

```bash
docker build -t verticalization .
```

После сборки контейнера, можно выполнять основные скрипты.

Запуск скрипта вертикализации одного файла из докера:

```bash
docker run -v ~/video-verticalization/verticalization_dataset:/data -v ~/video-verticalization/output:/output -it verticalization verticalize --input_video_path /data/shot_videos/beSBf5Lo_71Hz88c-AJTAw.mp4 --input_features_path /data/unlabelled_features/beSBf5Lo_71Hz88c-AJTAw.json --output_dir_path /output --visualize
```

Запуск скрипта валидации из докера:

```bash
docker run -v ~/video-verticalization/verticalization_dataset:/data -v ~/video-verticalization/evaluation_results:/evaluation_results -it verticalization evaluate --validation_set /data/validation_set/ --videos /data/shot_videos/ --results_dir /evaluation_results --visualize
```

Если я не хочу использовать Docker?

Если вы по какой-то причине не хоте использовать Docker, вы можете самостоятельно уставноить [Poetry](https://python-poetry.org/).
Перед тем как устанавливать Poetry, удостоверьтесь, что версия Python у вас 3.8.0
Установить Poetry мрожно [несколькими способами](https://python-poetry.org/docs/#installation)

После установки Poetry, находясь в директории проекта, установите окружение:

```bash
poetry install
```

Теперь можно запускать скрипты.

Пример запуска скрипта, который кропает одно видео и сохраняет кропнутое видео.

```bash
poetry run verticalize --input_video_path verticalization_dataset/shot_videos/beSBf5Lo_71Hz88c-AJTAw.mp4 --input_features_path verticalization_dataset/unlabelled_features/beSBf5Lo_71Hz88c-AJTAw.json --output_dir_path ./output/ --visualize
```

Запуск скрипта, который подсчитывает метрики на валидационном датасете:

```bash
poetry run evaluate --validation_set ./verticalization_dataset/validation_set/ --videos ./verticalization_dataset/shot_videos/ --results_dir ./evaluation_results --visualize
```
