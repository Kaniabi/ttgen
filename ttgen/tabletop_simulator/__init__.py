from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict

from ttgen.dataclass_ import Point3D, RgbType


class _TabletopBase:

    @classmethod
    def from_dict(cls, **d):
        from ttgen.dataclass_ import dataclass_from_dict
        return dataclass_from_dict(cls, **d)


@dataclass
class TabletopGrid(_TabletopBase):
    Type: int = 0
    Lines: bool = False
    Color: RgbType = RgbType()
    Opacity: float = 0.75
    ThickLines: bool = False
    Snapping: bool = False
    Offset: bool = False
    BothSnapping: bool = False
    xSize: float = 2.0
    ySize: float = 2.0
    PosOffset: Point3D = Point3D(x=0.0, y=1.0, z=0.0)


@dataclass
class TabletopLighting(_TabletopBase):
    LightIntensity: float = 0.54
    LightColor: RgbType = RgbType(1.0, 0.9804, 0.8902)
    AmbientIntensity: float = 1.3
    AmbientType: int = 0
    AmbientSkyColor: RgbType = RgbType(0.5, 0.5, 0.5)
    AmbientEquatorColor: RgbType = RgbType(0.5, 0.5, 0.5)
    AmbientGroundColor: RgbType = RgbType(0.5, 0.5, 0.5)
    ReflectionIntensity: float = 1.0
    LutIndex: int = 0
    LutContribution: float = 1.0


@dataclass
class TabletopTransform(_TabletopBase):
    posX: float = 0.0
    posY: float = 0.0
    posZ: float = 0.0
    rotX: float = 0.0
    rotY: float = 0.0
    rotZ: float = 0.0
    scaleX: float = 1.0
    scaleY: float = 1.0
    scaleZ: float = 1.0


@dataclass
class TabletopHandTransform(_TabletopBase):
    Color: str = ""
    Transform: List[TabletopTransform] = field(default_factory=list)


@dataclass
class TabletopHands(_TabletopBase):
    Enable: bool = True
    DisableUnused: bool = False
    Hiding: int = 0
    HandTransforms: List[TabletopHandTransform] = field(default_factory=list)


@dataclass
class TabletopTurns(_TabletopBase):
    Enable: bool = False
    Type: int = 0
    TurnOrder: list = field(default_factory=list)
    Reverse: bool = False
    SkipEmpty: bool = False
    DisableInteractions: bool = False
    PassTurns: bool = True


@dataclass
class AttachedSnapPoint(_TabletopBase):
    Position: Point3D = Point3D()


@dataclass
class AttachedVectorLine(_TabletopBase):
    points3: List[Point3D] = field(default_factory=Point3D)
    color: RgbType = RgbType()
    thickness: float = 0.1
    loop: bool = True


@dataclass
class TabletopObjectState(_TabletopBase):
    Name: str = 0
    Transform: TabletopTransform = TabletopTransform()
    Nickname: str = ""
    Description: str = ""
    ColorDiffuse: RgbType = RgbType(1.0, 1.0, 1.0)
    Locked: bool = False
    Grid: bool = True
    Snap: bool = True
    IgnoreFoW: bool = False
    Autoraise: bool = True
    Sticky: bool = True
    Tooltip: bool = True
    GridProjection: bool = False
    Hands: bool = False
    XmlUI: str = ""
    LuaScript: str = ""
    LuaScriptState: str = ""
    GUID: str = ""
    AttachedSnapPoints: List[AttachedSnapPoint] = field(default_factory=list)
    AttachedVectorLines: List[AttachedVectorLine] = field(default_factory=list)


@dataclass
class TabletopObjectStateContainer(TabletopObjectState):
    ContainedObjects: List[TabletopObjectState] = field(default_factory=list)


@dataclass
class TabletopCustomAssetBundle(TabletopObjectState):

    @dataclass
    class CustomAssetBundleField(_TabletopBase):
        AssetbundleURL: str = ""
        AssetbundleSecondaryURL: str = ""

        MaterialIndex: int = 0
        TypeIndex: int = 0
        LoopingEffectIndex: int = 0

    Name: str = "Custom_Assetbundle"
    CustomAssetbundle: CustomAssetBundleField = CustomAssetBundleField()


@dataclass
class TabletopCustomModel(TabletopObjectState):

    @dataclass
    class CustomMeshField(_TabletopBase):

        @dataclass
        class CustomShaderField(_TabletopBase):
            SpecularColor: RgbType = RgbType(1, 1, 1)
            SpecularIntensity: float = 0.0
            SpecularSharpness: float = 2.0
            FresnelStrength: float = 0.0

        MeshURL: str = ""
        DiffuseURL: str = ""
        NormalURL: str = ""
        ColliderURL: str = ""
        Convex: bool = True

        MaterialIndex: int = 0
        TypeIndex: int = 0

        CustomShader: CustomShaderField = CustomShaderField()
        CastShadows: bool = True

    Name: str = "Custom_Model"
    CustomMesh: CustomMeshField = CustomMeshField()


@dataclass
class TabletopCustomImage(_TabletopBase):

    @dataclass
    class CustomToken(_TabletopBase):
        Thickness: float = 0.1
        MergeDistancePixels: float = 15.0
        Stackable: bool = True

    ImageURL: str = ""
    ImageSecondaryURL: str = ""
    WidthScale: float = 1.58566439


@dataclass
class TabletopCustomTokenStack(TabletopObjectState):

    Name: str = "Custom_Token_Stack"
    MaterialIndex: int = -1
    MeshIndex: int = 1
    Number: int = 6
    CustomImage: TabletopCustomImage = TabletopCustomImage()


# Deck


@dataclass
class TabletopCard(TabletopObjectState):
    Name: str = "Card"
    CardID: int = 0
    SidewaysCard: bool = False


@dataclass
class TabletopCustomDeck(_TabletopBase):
    FaceURL: str = ""
    BackURL: str = ""
    NumWidth: int = 10
    NumHeight: int = 7
    BackIsHidden: bool = False
    UniqueBack: bool = False


@dataclass
class TabletopDeckCustom(TabletopObjectStateContainer):
    Name: str = "DeckCustom"
    HideWhenFaceDown: bool = False
    DeckIDs: List[int] = field(default_factory=list)
    CustomDeck: Dict[str, TabletopCustomDeck] = field(default_factory=dict)


# Board


@dataclass
class TabletopCustomBoard(TabletopObjectState):
    Name: str = "Custom_Board"
    Locked: bool = False
    Transform: TabletopTransform = TabletopTransform(posY=2.0, rotY=180.0)
    ColorDiffuse: RgbType = RgbType(0.7867647, 0.7867647, 0.7867647)
    HideWhenFaceDown: bool = False
    CustomImage: TabletopCustomImage = TabletopCustomImage()


@dataclass
class TabletopTabState(_TabletopBase):
    title: str = ""
    body: str = ""
    color: str = "Black"  # PlayerColor
    visibleColor: RgbType = RgbType()
    id: int = 0

    @classmethod
    def default_container(cls):
        return {
            "0": cls(
                title="Rules", color="Grey", visibleColor=RgbType(0.5, 0.5, 0.5), id=0
            ),
            "1": cls(
                title="White", color="White", visibleColor=RgbType(1.0, 1.0, 1.0), id=1
            ),
            "2": cls(
                title="Brown",
                color="Brown",
                visibleColor=RgbType(0.443, 0.231, 0.09),
                id=2,
            ),
            "3": cls(
                title="Red", color="Red", visibleColor=RgbType(0.856, 0.1, 0.094), id=3
            ),
            "4": cls(
                title="Orange",
                color="Orange",
                visibleColor=RgbType(0.956, 0.392, 0.113),
                id=4,
            ),
            "5": cls(
                title="Yellow",
                color="Yellow",
                visibleColor=RgbType(0.905, 0.898, 0.172),
                id=5,
            ),
            "6": cls(
                title="Green",
                color="Green",
                visibleColor=RgbType(0.192, 0.701, 0.168),
                id=6,
            ),
            "7": cls(
                title="Blue",
                color="Blue",
                visibleColor=RgbType(0.118, 0.53, 1.0),
                id=7,
            ),
            "8": cls(
                title="Teal",
                color="Teal",
                visibleColor=RgbType(0.129, 0.694, 0.607),
                id=8,
            ),
            "9": cls(
                title="Purple",
                color="Purple",
                visibleColor=RgbType(0.627, 0.125, 0.941),
                id=9,
            ),
            "10": cls(
                title="Pink",
                color="Pink",
                visibleColor=RgbType(0.96, 0.439, 0.807),
                id=10,
            ),
            "11": cls(
                title="Black",
                color="Black",
                visibleColor=RgbType(0.25, 0.25, 0.25),
                id=11,
            ),
        }


@dataclass
class TabletopSimulator(_TabletopBase):
    SaveName: str = "Tabletop Generator"
    GameMode: str = "Tabletop Generator"
    Gravity: float = 0.5
    PlayArea: float = 0.5
    Date: str = datetime(2019, 5, 6).isoformat()
    Table: str = "Table_None"
    TableURL: str = "http://i.imgur.com/NGDZtRM.jpg"
    Sky: str = "Sky_Museum"
    SkyUrl: str = "http://cloud-3.steamusercontent.com/ugc/931557769819239972/B4E92C79E65DB06185978CE7F0E1D2A36EF55476/"
    Note: str = ""
    Rules: str = ""
    XmlUI: str = ""
    LuaScript: str = ""
    LuaScriptState: str = ""
    Grid: TabletopGrid = TabletopGrid()
    Lighting: TabletopLighting = TabletopLighting()
    Hands: TabletopHands = TabletopHands()
    Turns: TabletopTurns = TabletopTurns()
    ObjectStates: List[TabletopObjectState] = field(default_factory=list)
    DecalPallet: List[str] = field(default_factory=list)
    TabStates: Dict[str, TabletopTabState] = field(
        default_factory=TabletopTabState.default_container
    )
    VersionNumber: str = "v12.0.1"

    def save(self, filename):
        import json
        from pprint import pprint

        # pprint(self, width=120, indent=2)
        contents = asdict(self)
        pprint(contents, width=120, indent=2)
        contents = json.dumps(contents, indent=2)
        filename.write_text(contents)
