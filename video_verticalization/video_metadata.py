from skvideo.io import ffprobe


class VideoMetadata:
    def __init__(
            self,
            file_path: str,
    ):
        """
        Constructor.

        :param file_path: Path to video file.
        """
        try:
            metadata = ffprobe(file_path)['video']
        except KeyError as err:
            raise Exception(f'File "{file_path}" does not exist or corrupted.') from err

        self._file_path = file_path
        self._fps = int(metadata['@nb_frames']) / float(metadata['@duration'])
        self._duration_seconds = float(metadata['@duration'])
        self._total_frames = int(metadata['@nb_frames'])
        self._frame_width = int(metadata['@width'])
        self._frame_height = int(metadata['@height'])

    @property
    def file_path(self) -> str:
        """Path to video file."""
        return self._file_path

    @property
    def fps(self) -> float:
        """Video FPS."""
        return self._fps

    @property
    def duration_seconds(self) -> float:
        """Video duration in seconds."""
        return self._duration_seconds

    @property
    def total_frames(self) -> int:
        """Video frames count."""
        return self._total_frames

    @property
    def frame_width(self) -> int:
        """Frame width in pixels."""
        return self._frame_width

    @property
    def frame_height(self) -> int:
        """Frame height in pixels."""
        return self._frame_height
