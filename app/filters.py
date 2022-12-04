from rest_framework.filters import BaseFilterBackend
import coreapi


class CreateClientFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='phone',
                required=True,
                type='integer'
            ),
            coreapi.Field(
                name='operator_code',
                required=True,
                type='string'
            ),
            coreapi.Field(
                name='tag',
                required=True,
                type='string'
            ),
            coreapi.Field(
                name='timezone',
                required=True,
                type='string'
            )
        ]

class UpdateClientFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='id',
                required=True,
                type='integer'
            ),
            coreapi.Field(
                name='phone',
                type='integer'
            ),
            coreapi.Field(
                name='operator_code',
                type='string'
            ),
            coreapi.Field(
                name='tag',
                type='string'
            ),
            coreapi.Field(
                name='timezone',
                type='string'
            )
        ]

class DeleteClientFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='id',
                required=True,
                type='integer'
            ),
        ]

class CreateMailingFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='date_start',
                required=True,
                type='string'
            ),
            coreapi.Field(
                name='text',
                required=True,
                type='string'
            ),
            coreapi.Field(
                name='filter',
                required=True,
                type='string'
            ),
            coreapi.Field(
                name='date_end',
                required=True,
                type='string'
            ),
        ]

class UpdateMailingFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='id',
                required=True,
                type='integer'
            ),
            coreapi.Field(
                name='date_start',
                type='string'
            ),
            coreapi.Field(
                name='text',
                type='string'
            ),
            coreapi.Field(
                name='filter',
                type='string'
            ),
            coreapi.Field(
                name='date_end',
                type='string'
            ),
        ]

class DeleteMailingFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='id',
                required=True,
                type='integer'
            ),
        ]

class MailingDataSingleFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='id',
                required=True,
                type='integer'
            ),
        ]
