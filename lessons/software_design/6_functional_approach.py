# класс, реализующий хранение и чтение из файла
class FileRepository(DatasetRepositoryPort):
    def __init__(self, file_path: Path, seed_records: Sequence[DatasetRecord] | None = None) -> None:
        self._file_path = file_path
        self._records = self._load_or_seed(seed_records=seed_records)
        self._by_h3_index: dict[int, list[DatasetRecord]] | None = None
        self._children_by_parent: dict[int, dict[int, list[DatasetRecord]]] = {}

    def _load_or_seed(self, seed_records: Sequence[DatasetRecord] | None) -> list[DatasetRecord]:
        if self._file_path.exists():
            with self._file_path.open("r", encoding="utf-8") as source:
                rows = json.load(source)
            return [DatasetRecord.from_row(row) for row in rows]

        if seed_records is None:
            return []

        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        rows = [record.to_row() for record in seed_records]
        with self._file_path.open("w", encoding="utf-8") as target:
            json.dump(rows, target, ensure_ascii=True)
        return list(seed_records)

    def _persist(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as target:
            json.dump([record.to_row() for record in self._records], target, ensure_ascii=True)

    def get_records(self) -> Sequence[DatasetRecord]:
        return self._records

    def _ensure_h3_index(self) -> dict[int, list[DatasetRecord]]:
        if self._by_h3_index is None:
            index: dict[int, list[DatasetRecord]] = defaultdict(list)
            for record in self._records:
                index[record.h3_index].append(record)
            self._by_h3_index = index
        return self._by_h3_index

    def _ensure_parent_index(self, resolution: int) -> dict[int, list[DatasetRecord]]:
        if resolution not in self._children_by_parent:
            index: dict[int, list[DatasetRecord]] = defaultdict(list)
            for record in self._records:
                parent_hex = int(h3n.cell_to_parent(record.h3_index, resolution))
                index[parent_hex].append(record)
            self._children_by_parent[resolution] = index
        return self._children_by_parent[resolution]

    def get_children(self, parent_hex: str) -> list[DatasetRecord]:
        parent_hex_int = int(h3n.str_to_int(parent_hex))
        resolution = int(h3n.get_resolution(parent_hex_int))
        if resolution == 12:
            return list(self._ensure_h3_index().get(parent_hex_int, []))
        return list(self._ensure_parent_index(resolution).get(parent_hex_int, []))

    def get_parent_groups(self, resolution: int) -> Mapping[int, list[DatasetRecord]]:
        return self._ensure_parent_index(resolution)

    # императивный подход, мутация данных на месте
    def replace_records(self, records: Sequence[DatasetRecord]) -> None:
        self._records = list(records)
        self._by_h3_index = None
        self._children_by_parent = {}
        self._persist()

    # функциланльный подход - создаем новый экземпляр репозитория при необходимости изменения данных
    @classmethod
    def _create_with_records(cls, file_path: Path, records: Sequence[DatasetRecord]) -> FileRepository:
        repo = object.__new__(cls)
        repo._file_path = file_path
        repo._records = list(records)
        repo._by_h3_index = None
        repo._children_by_parent = {}
        repo._persist()
        return repo

    def _replace_records(self, records: Sequence[DatasetRecord]) -> None:
        self._records = list(records)
        self._by_h3_index = None
        self._children_by_parent = {}
        self._persist()

    def with_records(self, records: Sequence[DatasetRecord]) -> FileRepository:
        return self._create_with_records(self._file_path, records)

# вызов:
class DatasetService:
    def __init__(self, repository: DatasetRepositoryPort) -> None:
        self._repository = repository
        self._hex_service = HexService(lambda: self._repository)
        self._avg_service = AvgService(lambda: self._repository)
        self._bbox_service = BboxService(lambda: self._repository)
        self._kml_service = KmlService()

    def generate_dataset(
        self,
        center_lat: float = 56.0,
        center_lon: float = 38.0,
        radius_km: float = 7.0,
        resolution: int = 12,
    ) -> int:
        records = generate_source_dataset(
            center_lat=center_lat,
            center_lon=center_lon,
            radius_km=radius_km,
            source_resolution=resolution,
        )
        # self._repository.replace_records(records)  <--- было
        self._repository = self._repository.with_records(records)  # <---- стало

        return len(records)
