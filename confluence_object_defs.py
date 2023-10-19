from dataclasses import dataclass

# Warning: these have been inferred from export results, rather than written from spec


@dataclass(kw_only = True)
class ContentPermissionSet:
    Id: str
    Type: str
    OwningContentId: str
    CreationDate: str
    LastModificationDate: str
    ContentPermissionsIds: list[str]


@dataclass(kw_only = True)
class User2ContentRelationEntity:
    Id: str
    TargetContentId: str
    SourceContentId: str
    TargetType: str
    RelationName: str
    CreationDate: str
    LastModificationDate: str
    CreatorId: str
    LastModifierId: str


@dataclass(kw_only = True)
class Labelling:
    Id: str
    CreationDate: str
    LastModificationDate: str
    LabelableId: str
    LabelableType: str
    LabelId: str
    ContentId: str
    OwningUserId: str


@dataclass(kw_only = True)
class Comment:
    Id: str
    ContainerContentId: str = None
    HibernateVersion: str
    Title: str
    Version: str
    VersionComment: str
    LastModificationDate: str
    ContentStatus: str
    ParentId: str = None
    OriginalVersionId: str = None
    LowerTitle: str
    CreatorId: str
    CreationDate: str
    LastModifierId: str
    HistoricalVersionsIds: list[str] = None
    OutgoingLinksIds: list[str] = None
    ChildrenIds: list[str] = None
    BodyContentsIds: list[str]
    ContentPropertiesIds: list[str]
    CustomContentIds: list[str] = None


@dataclass(kw_only = True)
class SpacePermission:
    Id: str
    CreationDate: str
    LastModifierId: str
    CreatorId: str
    SpaceId: str
    Type: str
    UserSubjectId: str = None
    Group: str = None
    AllUsersSubject: str
    LastModificationDate: str


@dataclass(kw_only = True)
class Label:
    Id: str
    Namespace: str
    CreationDate: str
    LastModificationDate: str
    OwningUserId: str = None
    Name: str


@dataclass(kw_only = True)
class ContentPermission:
    Id: str
    GroupName: str
    OwningSetId: str
    CreatorId: str
    CreationDate: str
    LastModifierId: str
    LastModificationDate: str
    Type: str
    UserSubjectId: str


@dataclass(kw_only = True)
class BucketPropertySetItem:
    Id: str
    Type: str
    BooleanVal: str
    DoubleVal: str
    StringVal: str
    TextVal: str
    LongVal: str
    IntVal: str
    DateVal: str


@dataclass(kw_only = True)
class Page:
    Id: str
    ContentStatus: str
    SpaceId: str = None # I'm guessing this only *isn't* none if the page is not at the root?
    OriginalVersionId: str = None
    LowerTitle: str
    Version: str
    CreationDate: str
    LastModifierId: str
    LastModificationDate: str
    Position: str
    HibernateVersion: str
    CreatorId: str
    Title: str
    VersionComment: str
    ParentId: str = None
    OutgoingLinksIds: list[str] = None
    ContentPropertiesIds: list[str] = None
    AttachmentsIds: list[str] = None
    AncestorsIds: list[str] = None
    ChildrenIds: list[str] = None
    LabellingsIds: list[str] = None
    CommentsIds: list[str] = None
    ContentPermissionSetsIds: list[str] = None
    # I wouldn't have thought BodyContentsIds were allowed to be empty *or* have more than one entry, but I don't know for sure and it *is* a collection tag
    BodyContentsIds: list[str]
    HistoricalVersionsIds: list[str] = None


@dataclass(kw_only = True)
class ConfluenceBandanaRecord:
    Id: str
    Context: str
    Key: str
    Value: str


@dataclass(kw_only = True)
class OutgoingLink:
    Id: str
    LowerDestinationPageTitle: str
    DestinationSpaceKey: str
    LastModifierId: str
    DestinationPageTitle: str
    SourceContentId: str
    CreatorId: str
    CreationDate: str
    LastModificationDate: str
    LowerDestinationSpaceKey: str


@dataclass(kw_only = True)
class Space:
    Id: str
    SpaceType: str
    HomePageId: str
    CreationDate: str
    LastModifierId: str
    LastModificationDate: str
    CreatorId: str
    SpaceStatus: str
    Name: str
    Key: str
    LowerKey: str
    DescriptionId: str
    PermissionsIds: list[str]


@dataclass(kw_only = True)
class ContentProperty:
    Id: str
    Name: str
    StringValue: str
    LongValue: str
    DateValue: str


@dataclass(kw_only = True)
class Attachment:
    Id: str
    CreationDate: str
    LastModificationDate: str
    VersionComment: str
    SpaceId: str
    Title: str
    Version: str
    CreatorId: str
    LastModifierId: str
    ContentStatus: str
    ContainerContentId: str
    OriginalVersionId: str = None
    HibernateVersion: str
    LowerTitle: str
    ContentPropertiesIds: list[str]
    HistoricalVersionsIds: list[str] = None
    ImageDetailsDTOIds: list[str] = None


@dataclass(kw_only = True)
class SpaceDescription:
    Id: str
    HibernateVersion: str
    LowerTitle: str
    LastModifierId: str
    VersionComment: str
    OriginalVersionId: str = None
    SpaceId: str
    Title: str
    Version: str
    CreatorId: str
    CreationDate: str
    LastModificationDate: str
    ContentStatus: str
    BodyContentsIds: list[str]
    HistoricalVersionsIds: list[str] = None
    AttachmentsIds: list[str] = None
    LabellingsIds: list[str]


@dataclass(kw_only = True)
class Notification:
    Id: str
    Type: str
    ReceiverId: str
    CreatorId: str
    CreationDate: str
    LastModifierId: str
    LastModificationDate: str
    Digest: str
    Network: str
    SpaceId: str = None
    ContentId: str


@dataclass(kw_only = True)
class ConfluenceUserImpl:
    Id: str
    Email: str
    Name: str
    LowerName: str


@dataclass(kw_only = True)
class BodyContent:
    Id: str
    Body: str
    ContentId: str
    BodyType: str # Observed values: 0 for wiki, 2 for XML storage format, 1 for comments. Comment body seems to encode text *and* location, comma-separated. Let's use 1000 for converted view format.
