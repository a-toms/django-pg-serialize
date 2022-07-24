class PGSerializer:
    def __init__(
            self, model: models.Model, target_fields: List[str],
            target_ids: Optional[List[int]] = None
    ) -> None:
        self.model = model
        self.target_fields = set(target_fields)
        self.target_ids = target_ids
        self.warn_if_not_postgres()

    def warn_if_not_postgres(self):
        db_in_use = connection.vendor
        if db_in_use != 'postgresql':
            message = "\n{} is designed for postgresql.\nYou are using {}, which" \
                      "is unsupported.".format(
                self.__class__.__name__, db_in_use
            )
            warnings.warn(message)

    @property
    def db_table(self) -> str:
        """
        We use this method to get the model's db_table. This method prevents
        SQL injection by avoiding accessing a table by an arbitrary string.
        """
        if not type(self.model) == ModelBase:
            invalid_type_message = "The argument '{}' has type {}.\n" \
                                   "{} requires an argument of a valid django model type.".format(
                self.model, type(self.model), self.__class__.__name__
            )
            raise Exception(invalid_type_message)
        return self.model._meta.db_table

    @property
    def sql_query(self) -> str:
        return open("shared/json_maker.sql", "r").read()

    def validate_fields(self) -> None:
        """
        Check that the fields are valid fields on the model. This method
        guards against SQL injection.
        """
        fields = self.model._meta._get_fields(forward=True, reverse=False)
        field_names = {field.name for field in fields}
        if self.target_fields.issubset(field_names):
            pass
        else:
            foreign_fields = self.target_fields.difference(field_names)
            message = "The model {} does not have the fields " \
                      "{}. Please enter valid fields." \
                .format(self.model, foreign_fields)
            raise KeyError(message)

    def to_json(self) -> dict:
        self.validate_fields()

        with connection.cursor() as cursor:
            cursor.execute(
                self.sql_query, params={
                    'fields': AsIs(",".join(self.target_fields)),
                    'table': AsIs(self.db_table),
                    'ids': self.target_ids
                }
            )
            return cursor.fetchall()[0][0]
