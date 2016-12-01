from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from brainminer.base.models import Base, BaseModel

FileSetFiles = Table(
    'file_set_files', Base.metadata,
    Column('file_set_id', Integer, ForeignKey('file_set.id')),
    Column('file_id', Integer, ForeignKey('file.id')))


# ----------------------------------------------------------------------------------------------------------------------
class Repository(BaseModel):

    __tablename__ = 'repository'
    __mapper_args__ = {
        'polymorphic_identity': 'repository',
    }

    # Repository ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Repository name
    name = Column(String(255), nullable=False, unique=True)

    def to_dict(self):
        files = []
        for f in self.files:
            files.append(f.to_dict())
        file_sets = []
        for file_set in self.file_sets:
            file_sets.append(file_set.to_dict())
        obj = super(Repository, self).to_dict()
        obj.update({
            'name': self.name,
            'files': files,
            'file_sets': file_sets,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class File(BaseModel):

    __tablename__ = 'file'
    __mapper_args__ = {
        'polymorphic_identity': 'file',
    }

    # File ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # File name without path information
    name = Column(String(255), nullable=False)
    # File extension
    _extension = Column(String(8), nullable=False)
    # File content type
    content_type = Column(String(64), nullable=False)
    # File size
    size = Column(Integer, nullable=False)
    # Storage ID in storage backend
    storage_id = Column(String, nullable=False)
    # Storage path in storage backend
    storage_path = Column(String, nullable=False)
    # Media link for downloading the file
    media_link = Column(String, nullable=False)
    # File repository ID
    repository_id = Column(Integer, ForeignKey('repository.id'), nullable=False)
    # File repository
    repository = relationship('Repository', backref='files', foreign_keys=[repository_id])

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, extension):
        self._extension = extension
        if self._extension.startswith('.'):
            self._extension = self._extension[1:]

    def to_dict(self):
        file_sets = []
        for file_set in self.file_sets:
            file_sets.append(file_set.name)
        obj = super(File, self).to_dict()
        obj.update({
            'name': self.name,
            'extension': self.extension,
            'content_type': self.content_type,
            'size': self.size,
            'storage_id': self.storage_id,
            'storage_path': self.storage_path,
            'media_link': self.media_link,
            'repository': self.repository.name,
            'file_sets': file_sets,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class FileSet(BaseModel):

    __tablename__ = 'file_set'
    __mapper_args__ = {
        'polymorphic_identity': 'file_set',
    }

    # File set ID
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # File set name
    name = Column(String(255), nullable=False)
    # Files inside this file set
    files = relationship('File', secondary=FileSetFiles, backref='file_sets')
    # File repository ID
    repository_id = Column(Integer, ForeignKey('repository.id'), nullable=False)
    # File repository
    repository = relationship('Repository', backref='file_sets', foreign_keys=[repository_id])
    
    def add_file(self, f):
        if f in self.files:
            return
        self.files.append(f)
        
    def remove_file(self, f):
        if f not in self.files:
            return
        self.files.remove(f)

    def to_dict(self):
        files = []
        for f in self.files:
            files.append(f.id)
        obj = super(FileSet, self).to_dict()
        obj.update({
            'name': self.name,
            'files': files,
            'repository': self.repository.name,
        })
        return obj
