# я не нашел код, который бы уже не содержал описанные в теории способы, поэтому прикреплю примеры использования того
# или иного подхода
# 7.1 DI

class AccessControlService:

    def __init__(self, account, cached_codex: CachedCodex, information_point: InformationPoint):
        self._account = account
        self._cached_codex = cached_codex
        self._information_point = information_point

    def can(self, subject, action, resource) -> bool:
        request = self._make_decision_request(subject, action, resource)
        policy_tree = self._get_policy_tree()
        return policy_tree.evaluate(request).decision == abac.Decision.PERMIT
    
    def reset_codex(self):
        self._cached_codex.reset()

    def _get_policy_tree(self) -> abac.PolicyTree:
        # TODO:
        #   После реализации подгрузки политик из БД, подгрузку
        #   кодекса необходимо пересмотреть учитывая кэширование с таймаутом.
        return self._cached_codex.get_data()

    def _make_decision_request(self, subject: SubjectType, action: ActionType, resource: ResourceType) -> abac.DecisionRequest:

        res = [
            self._information_point.make_subj_entity(subject),
            self._information_point.make_action_mapping(action),
            self._information_point.make_obj_entity(resource),
            self._information_point.get_env_mapping(subject),
        ]

        return abac.DecisionRequest(*res)
    

# 7.2 Полиморфизм
class _BaseAvatarStrategy(IFileTypeStrategy):

    def __init__(self):
        self._allowed_media_types: FrozenSet[str] = RASTER_IMAGE_MEDIA_TYPES
        self._allowed_max_size: int = 1024 * 1024

    def get_allowed_media_types(self) -> FrozenSet[str]:
        return self._allowed_media_types

    def get_max_size(self) -> int:
        return self._allowed_max_size

    async def process_file(self, file: File) -> Optional[ErrorObject]:
        dest_file_path = file.path + '.postprocessed'

        try:
            await image_to_png(file.path, dest_file_path)
        except InvalidImageException:
            logging.warning(f'{type(self).__name__}: file processing failed. file_id={file.id!r}', exc_info=True)
            return FileProcessingFailed()

        os.remove(file.path)
        dest_file_size = os.stat(dest_file_path).st_size

        file.path = dest_file_path
        file.media_type = 'image/png'
        file.size = dest_file_size


class DepartmentLogoStrategy(_BaseAvatarStrategy):
    pass


class AgentAvatarStrategy(_BaseAvatarStrategy):
    pass


class AccountLogoStrategy(_BaseAvatarStrategy):
    pass


class ChatLogoStrategy(_BaseAvatarStrategy):
    pass


class InvitationAvatarStrategy(_BaseAvatarStrategy):
    pass


class ButtonImageStrategy(IFileTypeStrategy):

    def __init__(self):
        self._allowed_media_types: FrozenSet[str] = BUTTON_IMAGE_MEDIA_TYPES
        self._allowed_max_size: int = 1024 * 1024 * 10

    def get_allowed_media_types(self) -> FrozenSet[str]:
        return self._allowed_media_types

    def get_max_size(self) -> int:
        return self._allowed_max_size

    async def process_file(self, file: File) -> Optional[ErrorObject]:
        dest_file_path = file.path + '.postprocessed'

        if file.media_type not in ('image/gif', 'image/svg'):
            try:
                await image_to_png(file.path, dest_file_path)
            except InvalidImageException:
                logging.warning(f'{type(self).__name__}: file processing failed. file_id={file.id!r}', exc_info=True)
                return FileProcessingFailed()
            Path(file.path).unlink()
            file.media_type = 'image/png'

        else:
            Path(file.path).replace(dest_file_path)

        dest_file_size = Path(dest_file_path).stat().st_size

        file.path = dest_file_path
        file.size = dest_file_size


# В другом месте определяем, какой страегией пользуемся
    @staticmethod
    def _get_strategy(file_type: FileType) -> IFileTypeStrategy:
        if file_type is FileType.DEPARTMENT_LOGO:
            return DepartmentLogoStrategy()
        elif file_type is FileType.AGENT_AVATAR:
            return AgentAvatarStrategy()
        elif file_type is FileType.COMPANY_LOGO:
            return AccountLogoStrategy()
        elif file_type is FileType.CHAT_LOGO:
            return ChatLogoStrategy()
        elif file_type is FileType.INVITATION_AVATAR:
            return InvitationAvatarStrategy()
        elif file_type is FileType.BUTTON_IMAGE:
            return ButtonImageStrategy()
        else:
            raise ValueError(f'No strategy for {file_type!r}')
        
# и полиморфно вызываем
    strategy = self._get_strategy(file.type)
    err = await strategy.process_file(file)


# 7.3 Конфигурации и метаданные через файлы свойств
def _obtain_data(self):
    p = Properties()
    file_names = [
        os.path.join(..., 'locales', self.lang, 'properties.txt'),
        # account-specific, partner-specific пути...
    ]
    for file_name in file_names:
        if os.path.exists(file_name):
            p.load(Path(file_name))
    return p.getPropertyDict()
