from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import itertools
from PySide2 import QtGui

# import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class CopyLightDialog(QtWidgets.QDialog):
    # constant to keep clean code
    # double values to get the right aspect ratio!
    LIGHTS_SRC_ITEMS = []
    LIGHTS_DEST_ITEMS = []
    ATTRIBUTES_SRC_ITEMS = []

    lights_items_in_scene = []  # {"transformName" : "shapeName"}

    # Creating all the lists of wanted attributes for each type of light
    point_light_attr = []
    spot_light_attr = []
    volume_light_attr = []
    directional_light_attr = []
    ambient_light_attr = []
    area_light_attr = []
    ai_area_light_attr = []
    ai_sky_dome_light_attr = []
    ai_mesh_light_attr = []
    ai_photometric_light_attr = []
    all_wanted_attributes = []

    # Creating all the generic variable to use
    FONT_LIST = QtGui.QFont("Turis Light")
    FONT_LABEL_DESC = QtGui.QFont("Retro Computer")
    # Color for the widgets
    MAIN_BACKGROUND_COLOR = "#192E5B"
    SECOND_BACKGROUND_COLOR = "#1D65A6"
    THIRD_BACKGROUND_COLOR = "#72A2C0"
    BTN_BACKGROUND_COLOR = "#00743F"
    FONT_COLOR_DESC = "#F2A104"
    FONT_COLOR_TITLE = "white"
    # Font for the widgets
    FONT_SIZE_TITLE = "17"
    FONT_SIZE_LABEL = "12"
    FONT_SIZE_DESC = "10"

    # Description creation
    DESCRIPTION_TE = QtWidgets.QTextEdit()
    DESCRIPTION_TE.setReadOnly(True)
    DESCRIPTION_TE.setHtml(
        f"""
        <ul>
            <p>To use this tool do the following instructions : </p>
            <li>Select one light source</li>
            <br>
            <li>Select the source light attributes you want to copy on the destination lights</li>
            <br>
            <li>Select one or many light you want to copy the aqttributes</li>
            <br>
            <li>Click the copy button</li>
            <br>
            <li>If you create a new light click on the update button to make her appear</li>
        </ul>"""
    )

    def __init__(self, parent=maya_main_window()):
        print("init()")
        super(CopyLightDialog, self).__init__(parent)
        self.create_all_list_wanted_attr()
        self.setWindowTitle("LIGHTS COPY ATTRIBUTES")
        # self.setFixedWidth(220)
        # self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.custom_set_style_sheet()

        self.populate_lights_items_in_scene_list()
        self.populate_lights_src_wdg_list()
        self.populate_lights_dest_wdg_list()
        print(self.lights_items_in_scene)

        # ["1920x1080 (1080p)", 1920.0, 1080.0],
        # ["lightTransformName", "lightShapeName"],

        # populate lists

        # self.populate_attrs_list()
        # self.populate_lights_dest_list()

    def custom_set_style_sheet(self):
        print("function style for widget")
        self.setStyleSheet("background-color : #192E5B;")
        self.set_style_sheet_list_wdg(self.attributes_src_list_wdg, self.THIRD_BACKGROUND_COLOR, self.FONT_LIST)
        self.set_style_sheet_list_wdg(self.lights_src_list_wdg, self.SECOND_BACKGROUND_COLOR, self.FONT_LIST)
        self.set_style_sheet_list_wdg(self.lights_dest_list_wdg, self.SECOND_BACKGROUND_COLOR, self.FONT_LIST)
        self.set_style_sheet_Desc_Label_wdg(
            self.title_lbl, self.FONT_COLOR_TITLE, self.FONT_LABEL_DESC, self.FONT_SIZE_TITLE
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.light_src_lbl, self.FONT_COLOR_TITLE, self.FONT_LABEL_DESC, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.light_dest_lbl, self.FONT_COLOR_TITLE, self.FONT_LABEL_DESC, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.description_lbl, self.FONT_COLOR_DESC, self.FONT_LABEL_DESC, self.FONT_SIZE_DESC
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.attr_lbl, self.FONT_COLOR_TITLE, self.FONT_LABEL_DESC, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_btn(self.copy_btn_wdg, self.BTN_BACKGROUND_COLOR, self.FONT_LABEL_DESC)
        self.set_style_sheet_btn(self.update_btn_wdg, self.BTN_BACKGROUND_COLOR, self.FONT_LABEL_DESC)
        self.set_style_sheet_btn(self.update_btn_wdg, self.BTN_BACKGROUND_COLOR, self.FONT_LABEL_DESC)
        self.set_style_sheet_btn(self.close_btn, self.BTN_BACKGROUND_COLOR, self.FONT_LABEL_DESC)

    def set_style_sheet_list_wdg(self, wdg_list, background_color, font_type):
        wdg_list.setFont(font_type)
        wdg_list.setStyleSheet(
            f"""
                                    QListWidget{{
                                            background-color : {background_color};
                                            border-radius : 5px;
                                                }}
                            """
        )

    def set_style_sheet_Desc_Label_wdg(self, wdg_list, font_color, font_type, font_size):
        wdg_list.setFont(font_type)
        wdg_list.setStyleSheet(
            f"""color : {font_color};
                                font-size : {font_size}px;"""
        )

    def set_style_sheet_btn(self, wdg_btn, background_color, font_type):
        wdg_btn.setFont(font_type)
        wdg_btn.setStyleSheet(
            f"""
                                QPushButton{{
                                            background-color : {background_color};
                                            border-radius : 3px;
                                            padding: 5px
                                            }}
                                QPushButton:hover{{
                                            background-color :{self.THIRD_BACKGROUND_COLOR};
                                            color : {self.MAIN_BACKGROUND_COLOR}
                                            }}
                            """
        )

    # initialize all lists and create the
    def create_all_list_wanted_attr(self):
        self.point_light_attr = [
            "color",
            "intensity",
            "emitDiffuse",
            "emitSpecular",
            "decayRate",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "aiExposure",
            "aiSamples",
            "aiRadius",
            "aiNormalize",
            "aiRoundness",
            "aiCastShadows",
            "aiShadowDensity",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiCamera",
            "aiTransmission",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.spot_light_attr = [
            "color",
            "intensity",
            "emitDiffuse",
            "emitSpecular",
            "decayRate",
            "coneAngle",
            "penumbraAngle",
            "dropoff",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "aiExposure",
            "aiSamples",
            "aiRadius",
            "aiNormalize",
            "aiRoundness",
            "aiCastShadows",
            "aiShadowDensity",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiAspectRatio",
            "aiLensRadius",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.volume_light_attr = [
            "color",
            "intensity",
            "emitDiffuse",
            "emitSpecular",
            "lightShape",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "aiExposure",
            "aiSamples",
            "aiNormalize",
            "aiCastShadows",
            "aiShadowDensity",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiCamera",
            "aiTransmission",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
            "aiRadius",
        ]
        self.directional_light_attr = [
            "color",
            "intensity",
            "emitDiffuse",
            "emitSpecular",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "aiExposure",
            "aiAngle",
            "aiSamples",
            "aiNormalize",
            "aiCastShadows",
            "aiShadowDensity",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.ambient_light_attr = ["color", "intensity", "ambientShade"]
        self.area_light_attr = [
            "color",
            "intensity",
            "emitDiffuse",
            "emitSpecular",
            "decayRate",
            "normalize",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "aiExposure",
            "aiSamples",
            "aiNormalize",
            "aiCastShadows",
            "aiShadowDensity",
            "aiResolution",
            "aiSpread",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiCamera",
            "aiTransmission",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]

        # Same as above for Arnold light
        self.ai_area_light_attr = [
            "color",
            "intensity",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "aiExposure",
            "aiSamples",
            "aiNormalize",
            "aiShadowColor",
            "aiCastShadows",
            "aiShadowDensity",
            "aiResolution",
            "aiSpread",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiCamera",
            "aiTransmission",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.ai_sky_dome_light_attr = [
            "color",
            "intensity",
            "resolution",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "format",
            "aiExposure",
            "aiSamples",
            "aiNormalize",
            "aiCastShadows",
            "aiShadowColor",
            "portalMode",
            "aiAovIndirect",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiCamera",
            "aiTransmission",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.ai_mesh_light_attr = [
            "color",
            "intensity",
            "aiExposure",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "lightVisible",
            "aiSamples",
            "aiNormalize",
            "aiCastShadows",
            "aiShadowDensity",
            "aiShadowColor",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.ai_photometric_light_attr = [
            "color",
            "intensity",
            "aiUseColorTemperature",
            "aiColorTemperature",
            "exposure",
            "aiSamples",
            "aiRadius",
            "aiNormalize",
            "aiCastShadows",
            "aiShadowDensity",
            "aiShadowColor",
            "aiCastVolumetricShadows",
            "aiVolumeSamples",
            "aiDiffuse",
            "aiSpecular",
            "aiSss",
            "aiIndirect",
            "aiVolume",
            "aiMaxBounces",
        ]
        self.all_wanted_attributes = set(
            itertools.chain(
                self.point_light_attr,
                self.volume_light_attr,
                self.directional_light_attr,
                self.ambient_light_attr,
                self.area_light_attr,
                self.ai_area_light_attr,
                self.ai_sky_dome_light_attr,
                self.ai_mesh_light_attr,
                self.ai_photometric_light_attr,
                self.spot_light_attr,
            )
        )

    def create_widgets(self):
        self.lights_src_list_wdg = QtWidgets.QListWidget()
        self.attributes_src_list_wdg = QtWidgets.QListWidget()
        self.attributes_src_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.lights_dest_list_wdg = QtWidgets.QListWidget()
        self.lights_dest_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.copy_btn_wdg = QtWidgets.QPushButton(">>Copy>>")
        self.update_btn_wdg = QtWidgets.QPushButton("Update")
        # self.resolution_list_wdg.addItems(
        #     [
        #         "1920x1080 (1080p)",
        #         "1280x720 (720p)",
        #         "960x540 (540p)",
        # ])

        # header widgets (QLabel)
        self.light_src_lbl = QtWidgets.QLabel("LIGHT SRC")
        self.light_src_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.attr_lbl = QtWidgets.QLabel("ATTRIBUTES")
        self.attr_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.light_dest_lbl = QtWidgets.QLabel("LIGHT DEST")
        self.light_dest_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # description label
        self.description_lbl = self.DESCRIPTION_TE
        self.description_lbl.setFixedWidth(500)

        # title label
        self.title_lbl = QtWidgets.QLabel(
            "GUILIC <span style='color:green'>Copy</span> Light <span style='color:green'>Attributes</span>"
        )

        # TODO ajouter un btn test "get lights" pour populate la liste src

        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(self.title_lbl)
        # layout.setAlignment(QtCore.Qt.AlignTop)
        title_layout.setAlignment(QtCore.Qt.AlignCenter)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.description_lbl)
        button_layout.addStretch()
        button_layout.addWidget(self.update_btn_wdg)
        button_layout.addWidget(self.close_btn)

        light_src_layout = QtWidgets.QVBoxLayout()
        attr_layout = QtWidgets.QVBoxLayout()
        light_dest_layout = QtWidgets.QVBoxLayout()

        light_src_layout.addWidget(self.light_src_lbl)
        light_src_layout.addWidget(self.lights_src_list_wdg)
        attr_layout.addWidget(self.attr_lbl)
        attr_layout.addWidget(self.attributes_src_list_wdg)
        light_dest_layout.addWidget(self.light_dest_lbl)
        light_dest_layout.addWidget(self.lights_dest_list_wdg)

        list_layout = QtWidgets.QHBoxLayout()
        list_layout.setContentsMargins(2, 2, 2, 2)
        list_layout.setSpacing(2)
        list_layout.addLayout(light_src_layout)
        list_layout.addSpacing(5)
        list_layout.addLayout(attr_layout)
        list_layout.addSpacing(10)
        list_layout.addWidget(self.copy_btn_wdg)
        list_layout.addSpacing(10)
        list_layout.addLayout(light_dest_layout)
        list_layout.addStretch()

        main_layout.addLayout(title_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        # self.lights_src_list_wdg.itemClicked.connect(self.set_output_res)
        # self.close_btn.clicked.connect(self.close)
        self.copy_btn_wdg.clicked.connect(self.on_click_copy_attributes)
        self.lights_src_list_wdg.itemClicked.connect(self.display_attributes_src_light)
        self.update_btn_wdg.clicked.connect(self.update_ui)

    def populate_lights_items_in_scene_list(self):
        self.lights_shapes = self.get_lights_in_scene()
        # populate dict
        for shape_name in self.lights_shapes:
            transform_name = self.get_transform_name(shape_name)
            print(transform_name, shape_name)
            self.lights_items_in_scene.append([transform_name, shape_name])

    def update_ui(self):
        print("update_ui()")
        self.lights_items_in_scene = []
        self.lights_src_list_wdg.clear()
        self.lights_dest_list_wdg.clear()
        self.populate_lights_items_in_scene_list()
        self.populate_lights_src_wdg_list()
        self.populate_lights_dest_wdg_list()

    def populate_lights_src_wdg_list(self):
        print("populate_lights_src_list")
        for l_src_item in self.lights_items_in_scene:
            lst_wdg_item = QtWidgets.QListWidgetItem(l_src_item[0])
            print(l_src_item)
            lst_wdg_item.setData(QtCore.Qt.UserRole, [l_src_item[1]])
            self.lights_src_list_wdg.addItem(lst_wdg_item)

    def populate_lights_dest_wdg_list(self):
        print("populate_lights_src_list")
        for l_src_item in self.lights_items_in_scene:
            lst_wdg_item = QtWidgets.QListWidgetItem(l_src_item[0])
            print(l_src_item)
            lst_wdg_item.setData(QtCore.Qt.UserRole, [l_src_item[1]])
            self.lights_dest_list_wdg.addItem(lst_wdg_item)

    def populate_attrs_list(self, attrs):
        print("populate_attrs_list")
        self.attributes_src_list_wdg.clear()
        for attr in attrs:
            lst_wdg_item = QtWidgets.QListWidgetItem(attr)

            # lst_wdg_item.setData(
            #     QtCore.Qt.UserRole, [attr_item[1], attr_item[2]]
            # )
            self.attributes_src_list_wdg.addItem(lst_wdg_item)

    def display_attributes_src_light(self, item):
        print("display_attributes_src_light()")

        light_transform = item.text()
        item_data = item.data(QtCore.Qt.UserRole)
        light_shape = item_data[0]
        attrs = self.listing_attributes(light_shape)
        print(len(attrs), light_transform, attrs)
        self.populate_attrs_list(attrs)

    def on_click_copy_attributes(self):
        print("copy_attributes()")

        light_src_item = self.lights_src_list_wdg.selectedItems()[0]
        shape_light_src = light_src_item.data(QtCore.Qt.UserRole)[0]
        print(shape_light_src)
        lights_dest_items = self.lights_dest_list_wdg.selectedItems()
        shapes_lights_dest = [x.data(QtCore.Qt.UserRole)[0] for x in lights_dest_items]
        print(shapes_lights_dest)
        attrs_items = self.attributes_src_list_wdg.selectedItems()
        attr_names_list = [x.text() for x in attrs_items]
        print(attr_names_list)

        self.copy_arguments(shape_light_src, attr_names_list, shapes_lights_dest)

    def copy_arguments(self, light_src, attribute_name_list, lights_dest):
        types3_accepted = ["double3", "float3"]
        types_accepted = ["float", "bool", "double"]
        print("in copy argument")
        print(light_src, attribute_name_list, lights_dest)
        attr_not_in_dest_light = []
        attr_copy_success_dest_light = []
        for light_shape_node in lights_dest:
            light_dest_attr = self.listing_attributes(light_shape_node)
            for attribute_name in attribute_name_list:
                if (
                    attribute_name in light_dest_attr or attribute_name == "exposure" or attribute_name == "aiExposure"
                ):  #  and self.check_list_arg(list_attr_light_src,attribute_name):
                    attribute_dest = "{0}.{1}".format(light_shape_node, attribute_name)
                    attribute_source = "{0}.{1}".format(light_src, attribute_name)
                    type_attribute = cmds.getAttr(attribute_source, type=True)
                    try:
                        if attribute_name == "aiExposure" and "exposure" in light_dest_attr:
                            cmds.setAttr(
                                light_shape_node + "." + "exposure", cmds.getAttr(light_src + "." + attribute_name)
                            )
                            attr_copy_success_dest_light.append("{0}.{1}".format(light_shape_node, attribute_name))
                        elif attribute_name == "exposure" and "aiExposure" in light_dest_attr:
                            cmds.setAttr(
                                light_shape_node + "." + "aiExposure", cmds.getAttr(light_src + "." + attribute_name)
                            )
                            attr_copy_success_dest_light.append("{0}.{1}".format(light_shape_node, attribute_name))
                        elif type_attribute in types3_accepted:
                            d0 = cmds.getAttr(attribute_source)[0][0]
                            d1 = cmds.getAttr(attribute_source)[0][1]
                            d2 = cmds.getAttr(attribute_source)[0][2]
                            cmds.getAttr(
                                attribute_source, cmds.setAttr(attribute_dest, d0, d1, d2, type=type_attribute)
                            )
                        elif type_attribute in types_accepted:
                            print(cmds.getAttr(light_shape_node + "." + attribute_name))
                            cmds.setAttr(
                                light_shape_node + "." + attribute_name, cmds.getAttr(light_src + "." + attribute_name)
                            )
                            attr_copy_success_dest_light.append("{0}.{1}".format(light_shape_node, attribute_name))
                        else:
                            print("attribute type not recognized : " + type_attribute)
                    except RuntimeError:
                        print("type not supported")
                        attr_not_in_dest_light.append("{0}.{1}".format(light_shape_node, attribute_name))
                else:
                    print("Attribute " + attribute_name + " don't exist in : " + light_shape_node)
                    attr_not_in_dest_light.append("{0}.{1}".format(light_shape_node, attribute_name))
        print("not copy attributes")
        print(attr_not_in_dest_light)
        print("copy attributes success")
        print(attr_copy_success_dest_light)

    def check_list_arg(self, list_attr_light, argument):
        if argument not in list_attr_light:
            print("attribut not in the src list : " + str(argument))
            return False
        else:
            print("Attribut in the src list : " + str(argument))
            return True

    def listing_attributes(self, node):
        print("in listing attribute!!")
        print(node)
        # debug_attrs = [
        #     "publishedNodeInfo.publishedNode",
        #     "publishedNodeInfo.isHierarchicalNode",
        #     "publishedNodeInfo.publishedNodeType",
        #     "instObjGroups.objectGroups.objectGrpCompList",
        #     "instObjGroups.objectGroups.objectGroupId",
        #     "instObjGroups.objectGroups.objectGrpColor" "renderLayerInfo.renderLayerId",
        #     "instObjGroups.objectGroups.objectGrpColor",
        #     "renderLayerInfo.renderLayerId",
        #     "renderLayerInfo.renderLayerRenderable" "renderLayerInfo.renderLayerColor",
        #     "renderLayerInfo.renderLayerRenderable",
        #     "renderLayerInfo.renderLayerColor",
        #     "compInstObjGroups.compObjectGroups.compObjectGrpCompList",
        #     "compInstObjGroups.compObjectGroups.compObjectGroupId",
        #     "componentTags.componentTagName",
        #     "componentTags.componentTagContents",
        # ]

        types_not_allowed = ["message", "TdataCompound", "attributeAlias"]
        attrs = cmds.listAttr(node)
        list_attrs_of_light = []
        print(attrs)
        for attr in attrs:
            if attr in self.all_wanted_attributes:
                type = cmds.getAttr("{}.{}".format(node, attr), typ=True)
                if type in types_not_allowed:
                    print("type not allowed :" + type)
                lastChar = attr[-1]
                if lastChar == "R" or lastChar == "G" or lastChar == "B":
                    print("don't use ColorR etc... instead use Color attribute")
                else:
                    list_attrs_of_light.append(attr)
        return list_attrs_of_light

    def get_lights_in_scene(self):
        return cmds.ls(type=cmds.listNodeTypes("light"))

    def get_transform_name(self, shape_name):
        return cmds.listRelatives(shape_name, parent=True)[0]

    # def set_output_res(self, item):
    #     # we get dit and height: [1280.0, 720.0] ... [960.0, 540.0] with data() method
    #     resolution = item.data(QtCore.Qt.UserRole)

    #     cmds.setAttr("defaultResolution.width", resolution[0])
    #     cmds.setAttr("defaultResolution.height", resolution[1])
    #     # pour avoir le bon pixel ratio
    #     cmds.setAttr("defaultResolution.deviceAspectRatio", resolution[0] / resolution[1])


if __name__ == "__main__":

    # try:
    #     copy_light_dialog.close()  # pylint: disable=E0601
    #     copy_light_dialog.deleteLater()
    # except:
    #     pass

    copy_light_dialog = CopyLightDialog()
    copy_light_dialog.show()
