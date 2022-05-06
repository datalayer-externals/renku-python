# Copyright 2020 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Models for providers."""

from marshmallow import EXCLUDE

from renku.command.schema.dataset import DatasetSchema
from renku.domain_model.dataset import Dataset


class ProviderDataset(Dataset):
    """A Dataset that is imported from a provider."""

    def __init__(self, **kwargs):
        kwargs.setdefault("initial_identifier", "invalid-initial-id")
        super().__init__(**kwargs)
        self.dataset_files = []  # TODO Make this a property

    @classmethod
    def from_jsonld(cls, data, schema_class=None) -> "ProviderDataset":
        """Create an instance from JSON-LD data."""
        assert isinstance(data, (dict, list)), f"Invalid data type: {data}"

        schema_class = schema_class or DatasetSchema
        self = schema_class(flattened=True).load(data)
        return self

    @classmethod
    def from_dataset(cls, dataset: Dataset) -> "ProviderDataset":
        """Create an instance from a Dataset."""
        return ProviderDataset(
            annotations=dataset.annotations,
            creators=dataset.creators,
            dataset_files=[],
            date_created=dataset.date_created,
            date_published=dataset.date_published,
            date_removed=dataset.date_removed,
            derived_from=dataset.derived_from,
            description=dataset.description,
            id=dataset.id,
            identifier=dataset.identifier,
            images=dataset.images,
            in_language=dataset.in_language,
            initial_identifier=dataset.initial_identifier,
            keywords=dataset.keywords,
            license=dataset.license,
            name=dataset.name,
            project_id=dataset.project_id,
            same_as=dataset.same_as,
            title=dataset.title,
            version=dataset.version,
        )

    @property
    def files(self):
        """Return list of existing files."""
        raise NotImplementedError("ProviderDataset has no files.")


class ProviderDatasetFile:
    """Store metadata for dataset files that will be downloaded from a provider."""

    def __init__(self, source: str, filename: str, checksum: str, size_in_mb: int, filetype: str, path: str):
        self.source: str = source
        self.filename: str = filename
        self.checksum: str = checksum
        self.size_in_mb: int = size_in_mb
        self.filetype: str = filetype
        self.path: str = path


class ProviderDatasetSchema(DatasetSchema):
    """ProviderDataset schema."""

    class Meta:
        """Meta class."""

        model = ProviderDataset
        unknown = EXCLUDE