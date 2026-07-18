from pathlib import Path


class Headers:


    def __init__(self) -> None:
        self._private: list[Path] = []
        self._public: list[Path] = []


    def _normalize(self, value: str | Path | list[str | Path]) -> list[Path]:
        if isinstance(value, (str, Path)):
            return [Path(value)]
        return [Path(item) for item in value]


    @property
    def private(self) -> list[Path]:
        return self._private


    @private.setter
    def private(self, value: str | Path | list[str | Path]) -> None:
        self._private = self._normalize(value)


    @property
    def public(self) -> list[Path]:
        return self._public


    @public.setter
    def public(self, value: str | Path | list[str | Path]) -> None:
        self._public = self._normalize(value)