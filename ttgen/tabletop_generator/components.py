from dataclasses import dataclass, field
from typing import Dict

from dataclasses_json import DataClassJsonMixin

from ttgen.dataclass_ import Point3D
from ttgen.tabletop_generator.annotations import Annotations


class Globals:
    DECK_ID = 0

    @classmethod
    def get_deck_id(cls):
        cls.DECK_ID += 1
        return cls.DECK_ID

    @classmethod
    def gen_guid(cls):
        import uuid
        return str(uuid.uuid4())[:6]

    @classmethod
    def gen_image_url(cls, base_dir, path):
        from pathlib import Path, PureWindowsPath

        for i_extension in (".png", ".jpg"):
            filename = Path(f"{base_dir}/{path}{i_extension}")
            if filename.is_file():
                filename = PureWindowsPath(
                    '{}:/{}'.format(
                        filename.parts[1],
                        '/'.join(filename.parts[2:])
                    )
                )
                break
        else:
            raise RuntimeError(f"Image file not found for {base_dir}/{path}")

        return f"file:///{filename}"


@dataclass
class _Base(DataClassJsonMixin):
    name: str = ""
    position: Point3D = Point3D()
    rotation: Point3D = Point3D()
    scale: Point3D = Point3D()

    def get_key(self):
        prefix = self.__class__.__name__.lower()
        return f"{prefix}:{self.name}"

    def get_path(self):
        prefix = self.__class__.__name__.lower()
        return f"{prefix}s/{self.name}"

    @classmethod
    def from_dict(cls, d, name):
        result = cls.schema().load(d)
        result.name = name
        return result


@dataclass
class Board(_Base):
    image_url: str = ""
    # snap_points: List[int] = field(default_factory=list)

    def generate(self, dest_directory):
        from ttgen.tabletop_simulator import TabletopCustomBoard

        if not self.image_url:
            self.image_url = Globals.gen_image_url(dest_directory, self.get_path())

        return [
            TabletopCustomBoard.from_dict(
                Transform=dict(
                    posX=self.position.x,
                    posZ=self.position.y,
                    rotX=self.rotation.x,
                    rotY=self.rotation.y,
                    rotZ=self.rotation.z,
                    scaleX=self.scale.x,
                    scaleY=self.scale.y,
                    scaleZ=self.scale.z,
                ),
                CustomImage=dict(
                    ImageURL=self.image_url,
                ),
                GUID=Globals.gen_guid(),
            )
        ]

    @property
    def width(self):
        return 10.0

    @property
    def height(self):
        return 3.0


@dataclass
class Deck(_Base):
    face_url: str = ""
    back_url: str = ""
    num_dim: str = "10x7"
    metadata: Dict[str, str] = field(default_factory=dict)
    count: int = 52

    def generate(self, dest_directory):
        from ttgen.tabletop_simulator import TabletopDeckCustom, TabletopCard

        deck_id = Globals.get_deck_id()

        if not self.face_url:
            self.face_url = Globals.gen_image_url(dest_directory, self.get_path())
        if not self.back_url:
            self.back_url = Globals.gen_image_url(dest_directory, self.get_path() + "_back")

        cards = []
        for i in range(self.count):
            card_id = (100 * deck_id) + i
            c = TabletopCard(
                CardID=card_id,
                GUID=Globals.gen_guid(),
            )
            cards.append(c)

        num_dim = [int(i) for i in self.num_dim.split('x')]

        return [
            TabletopDeckCustom.from_dict(
                Nickname=self.name,
                Transform=dict(
                    posX=self.position.x,
                    posY=2.0,
                    posZ=self.position.y,
                    rotY=180.0,
                    rotZ=180.0,
                    scaleX=1.0,
                    scaleZ=1.0,
                ),
                DeckIDs=[i.CardID for i in cards],
                CustomDeck={
                    str(deck_id): dict(
                        FaceURL=self.face_url,
                        BackURL=self.back_url,
                        NumWidth=num_dim[0],
                        NumHeight=num_dim[1],
                    )
                },
                ContainedObjects=cards
            )
        ]


@dataclass
class Model(_Base):
    mesh_url: str = ""
    diffuse_url: str = ""
    collide_url: str = ""

    def generate(self, dest_directory):
        from ttgen.tabletop_simulator import TabletopCustomModel

        return [
            TabletopCustomModel.from_dict(
                Transform=dict(
                    posX=self.position.x,
                    posZ=self.position.y,
                ),
                CustomMesh=dict(
                    MeshURL = self.mesh_url,
                    DiffuseURL = self.diffuse_url,
                    ColliderURL = self.collide_url,
                ),
                GUID=Globals.gen_guid(),
            )
        ]


@dataclass
class TokenStack(_Base):
    image_url: str = ""

    def generate(self, dest_directory):
        from ttgen.tabletop_simulator import TabletopCustomTokenStack

        if not self.image_url:
            self.image_url = f"{dest_directory}\\{self.get_path()}.png"

        return [
            TabletopCustomTokenStack.from_dict(
                Transform=dict(
                    posX=self.position.x,
                    posZ=self.position.y,
                ),
                CustomImage=dict(
                    ImageURL=self.image_url,
                    WidthScale=0.0,
                ),
                GUID=Globals.gen_guid(),
            )
        ]


class _BaseTable(_Base):

    annotations: Annotations = Annotations()

    def get_key(self):
        return 'table'


@dataclass
class FlexTable(_BaseTable):

    DEFAULT_SIZE = 18.0

    table_width: float = 18.0
    table_height: float = 18.0

    surface_y: float = 10.4915

    def generate(self, dest_directory):
        from ttgen.tabletop_simulator import TabletopCustomAssetBundle, TabletopCustomModel

        width_scale = self.table_width / self.DEFAULT_SIZE
        depth_scale = self.table_height / self.DEFAULT_SIZE
        width_pos = (width_scale - 1.0) * self.DEFAULT_SIZE
        depth_pos = (depth_scale - 1.0) * self.DEFAULT_SIZE

        transform_legs = [
            dict(posY=-9.0, rotY=0.0, posX=-width_pos, posZ=-depth_pos),
            dict(posY=-9.0, rotY=90.0, posX=-width_pos, posZ=depth_pos),
            dict(posY=-9.0, rotY=180.0, posX=width_pos, posZ=depth_pos),
            dict(posY=-9.0, rotY=270.0, posX=width_pos, posZ=-depth_pos),
        ]
        transform_sides = [
            dict(posY=-9.0, rotY=0.0, posZ=-depth_pos, scaleX=width_scale),
            dict(posY=-9.0, rotY=90.0, posX=-width_pos, scaleX=depth_scale),
            dict(posY=-9.0, rotY=180.0, posZ=depth_pos, scaleX=width_scale),
            dict(posY=-9.0, rotY=270.0, posX=width_pos, scaleX=depth_scale),
        ]

        result = []
        for i in range(4):
            obj = TabletopCustomAssetBundle.from_dict(
                Locked=True,
                Transform=transform_legs[i],
                CustomAssetbundle={
                    "AssetbundleURL": "http://cloud-3.steamusercontent.com/ugc/879750610978795929/723C50F43FAB3DE3DC12CB8460536E8CB34B60A3/",
                    "AssetbundleSecondaryURL": "",
                    "MaterialIndex": 2,
                    "TypeIndex": 4,
                    "LoopingEffectIndex": 0,
                },
                GUID=Globals.gen_guid()
            )
            result.append(obj)
            obj = TabletopCustomAssetBundle.from_dict(
                Locked=True,
                Transform=transform_sides[i],
                CustomAssetbundle={
                    "AssetbundleURL": "http://cloud-3.steamusercontent.com/ugc/879750610978796471/14ED0DBD593370733A0309B0950004F33EB9FACA/",
                    "AssetbundleSecondaryURL": "",
                    "MaterialIndex": 1,
                    "TypeIndex": 4,
                    "LoopingEffectIndex": 0,
                },
                GUID=Globals.gen_guid()
            )
            result.append(obj)

        obj = TabletopCustomModel.from_dict(
            Transform=dict(
                posY=-9.0,
                scaleX=width_scale,
                scaleZ=depth_scale,
            ),
            Locked=True,
            CustomMesh=dict(
                MeshURL="http://cloud-3.steamusercontent.com/ugc/879750610978796176/4A5A65543B98BCFBF57E910D06EC984208223D38/",
                DiffuseURL="https://i.imgur.com/N0O6aqj.jpg",
            ),
        )
        for i_annotation in self.annotations:
            i_annotation.configure_surface(self, obj)
        result.append(obj)

        return result


@dataclass
class HardwoodTable(_BaseTable):

    def generate(self, dest_directory):
        from ttgen.tabletop_simulator import TabletopCustomAssetBundle

        result = []

        obj = TabletopCustomAssetBundle.from_dict(
            Locked=True,
            Transform=dict(
                posX=0.0,
                posY=-1.9,
                posZ=0.0,
                rotY=90.0,
                scaleX=7.5,
                scaleY=6.75,
                scaleZ=7.0,
            ),
            ColorDiffuse=dict(r=0.6103, g=0.4045, b=0.3860),
            CustomAssetbundle=dict(
                AssetbundleURL="chry.me/tts/3droom/hardwood_table.unity3d",
                AssetbundleSecondaryURL="",
                MaterialIndex=1,
                TypeIndex=4,
                LoopingEffectIndex=0,
            ),
            GUID=Globals.gen_guid()
        )
        result.append(obj)

        return result
