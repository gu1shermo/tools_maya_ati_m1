from functools import partial


from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui

FONT_LIST = QtGui.QFont("Turis Light")
FONT_LABEL_DESC = QtGui.QFont("Retro Computer")
MAIN_BACKGROUND_COLOR = "#192E5B"
SECOND_BACKGROUND_COLOR = "#1D65A6"
SECOND_BACKGROUND_CLOSE_COLOR = "#2D75B6"
THIRD_BACKGROUND_COLOR = "#72A2C0"
BTN_BACKGROUND_COLOR = "#00743F"
FONT_COLOR_DESC = "#F2A104"
FONT_COLOR_TITLE = "white"
FONT_SIZE_TITLE = "17"
FONT_SIZE_LABEL = "12"
FONT_SIZE_DESC = "13"


def set_style_sheet_Desc_Label_wdg(wdg_list, font_color, font_type, font_size):
    wdg_list.setFont(font_type)
    wdg_list.setStyleSheet(
        f"""
                            color : {font_color};
                            font-size : {font_size}px;
                            """
    )


def set_style_sheet_title_wdg(wdg_list, font_type_title, font_size_title):
    wdg_list.setFont(font_type_title)
    wdg_list.setStyleSheet(
        f"""
                            font-size : {font_size_title}px;
                            """
    )


def set_style_sheet_btn(wdg_btn, background_color, font_type):
    wdg_btn.setFont(font_type)
    wdg_btn.setStyleSheet(
        f"""
                            QPushButton{{
                                        background-color : {background_color};
                                        border-radius : 3px;
                                        padding: 5px
                                        }}
                            QPushButton:hover{{
                                        background-color :{THIRD_BACKGROUND_COLOR};
                                        color : {MAIN_BACKGROUND_COLOR}
                                        }}
                        """
    )


def set_style_sheet_double_spine_box_edit(wdg_edit):
    wdg_edit.setStyleSheet(
        f"""
                        QDoubleSpinBox:focus{{
                            background-color : white;
                            color : black;
                        }} 
    """
    )


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class Header(QtWidgets.QWidget):
    """Header class for collapsible group"""

    # Creating all the generic variable to use

    def __init__(self, name, content_widget):
        """Header Class Constructor to initialize the object.
        Args:
            name (str): Name for the header
            content_widget (QtWidgets.QWidget): Widget containing child elements
        """
        super(Header, self).__init__()
        # self.setStyleSheet(f"""QWidget{{
        #                     background-color : {SECOND_BACKGROUND_COLOR};
        #                     }}""")
        self.content = content_widget
        self.expand_ico = QtGui.QPixmap(":teDownArrow.png")
        self.collapse_ico = QtGui.QPixmap(":teRightArrow.png")

        stacked = QtWidgets.QStackedLayout(self)
        stacked.setStackingMode(QtWidgets.QStackedLayout.StackAll)
        background = QtWidgets.QLabel()
        # background.setStyleSheet("QLabel{ background-color: rgb(93, 93, 93); border-radius:2px}")

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(self.expand_ico)
        layout.addWidget(self.icon)
        layout.setContentsMargins(11, 0, 11, 0)

        font = QtGui.QFont()
        font.setBold(True)
        label = QtWidgets.QLabel(name)
        label.setFont(font)

        layout.addWidget(label)
        layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        stacked.addWidget(widget)
        stacked.addWidget(background)
        background.setMinimumHeight(layout.sizeHint().height() * 1.5)

        self.collapse()

    def mousePressEvent(self, *args):
        """Handle mouse events, call the function to toggle groups"""
        self.expand() if not self.content.isVisible() else self.collapse()

    def expand(self):
        self.content.setVisible(True)
        self.icon.setPixmap(self.expand_ico)

    def collapse(self):
        self.content.setVisible(False)
        self.icon.setPixmap(self.collapse_ico)


class Container(QtWidgets.QWidget):
    """Class for creating a collapsible group similar to how it is implement in Maya
    Examples:
        Simple example of how to add a Container to a QVBoxLayout and attach a QGridLayout
        >>> layout = QtWidgets.QVBoxLayout()
        >>> container = Container("Group")
        >>> layout.addWidget(container)
        >>> content_layout = QtWidgets.QGridLayout(container.contentWidget)
        >>> content_layout.addWidget(QtWidgets.QPushButton("Button"))
    """

    def __init__(self, name, color_background=False):
        """Container Class Constructor to initialize the object
        Args:
            name (str): Name for the header
            color_background (bool): whether or not to color the background lighter like in maya
        """
        super(Container, self).__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._content_widget = QtWidgets.QWidget()
        if color_background:
            self._content_widget.setStyleSheet(
                ".QWidget{background-color: rgb(73, 73, 73); " "margin-left: 2px; margin-right: 2px}"
            )
        self.header = Header(name, self._content_widget)
        layout.addWidget(self.header)
        layout.addWidget(self._content_widget)

        # assign header methods to instance attributes so they can be called outside of this class
        self.collapse = self.header.collapse
        self.expand = self.header.expand
        self.toggle = self.header.mousePressEvent

    @property
    def contentWidget(self):
        """Getter for the content widget
        Returns: Content widget
        """
        return self._content_widget

    """Class for creating a collapsible group similar to how it is implement in Maya
        Examples:
            Simple example of how to add a Container to a QVBoxLayout and attach a QGridLayout
            >>> layout = QtWidgets.QVBoxLayout()
            >>> container = Container("Group")
            >>> layout.addWidget(container)
            >>> content_layout = QtWidgets.QGridLayout(container.contentWidget)
            >>> content_layout.addWidget(QtWidgets.QPushButton("Button"))
    """

    def __init__(self, name, color_background=False):
        """Container Class Constructor to initialize the object
        Args:
            name (str): Name for the header
            color_background (bool): whether or not to color the background lighter like in maya
        """
        super(Container, self).__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self._content_widget = QtWidgets.QWidget()

        if color_background:
            self._content_widget.setStyleSheet(
                ".QWidget{background-color: rgb(0, 0, 73); " "margin-left: 0px; margin-right: 0px}"
            )
        self.header = Header(name, self._content_widget)
        layout.addWidget(self.header)
        layout.addWidget(self._content_widget)

        # assign header methods to instance attributes so they can be called outside of this class
        self.collapse = self.header.collapse
        self.expand = self.header.expand
        self.toggle = self.header.mousePressEvent

    @property
    def contentWidget(self):
        """Getter for the content widget
        Returns: Content widget
        """
        return self._content_widget


class CustomColorButton(QtWidgets.QWidget):

    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, color=QtCore.Qt.white, parent=None):
        super(CustomColorButton, self).__init__(parent)

        self.setObjectName("CustomColorButton")

        self.create_control()

        self.set_size(50, 14)
        self.set_color(color)

    def create_control(self):
        """1) Create the colorSliderGrp"""
        window = cmds.window()
        color_slider_name = cmds.colorSliderGrp()

        """ 2) Find the colorSliderGrp widget """
        self._color_slider_obj = omui.MQtUtil.findControl(color_slider_name)
        if self._color_slider_obj:
            self._color_slider_widget = wrapInstance(int(self._color_slider_obj), QtWidgets.QWidget)

            """ 3) Reparent the colorSliderGrp widget to this widget """
            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.setObjectName("main_layout")
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self._color_slider_widget)

            """ 4) Identify/store the colorSliderGrp�s child widgets (and hide if necessary)  """
            # children = self._color_slider_widget.children()
            # for child in children:
            #     # print(child)
            #     # print(child.objectName())
            # # print("---")

            self._slider_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "slider")
            if self._slider_widget:
                self._slider_widget.hide()

            self._color_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "port")

            cmds.colorSliderGrp(
                self.get_full_name(),
                e=True,
                changeCommand=partial(self.on_color_changed),
            )

        cmds.deleteUI(window, window=True)

    def get_full_name(self):
        return omui.MQtUtil.fullName(int(self._color_slider_obj))

    def set_size(self, width, height):
        self._color_slider_widget.setFixedWidth(width)
        self._color_widget.setFixedHeight(height)

    def set_color(self, color):
        color = QtGui.QColor(color)
        if color != self.get_color():
            cmds.colorSliderGrp(
                self.get_full_name(),
                e=True,
                rgbValue=(color.redF(), color.greenF(), color.blueF()),
            )
            self.on_color_changed()

    def get_color(self):
        color_values = cmds.colorSliderGrp(self._color_slider_widget.objectName(), q=True, rgbValue=True)
        color = cmds.colorSliderGrp(self.get_full_name(), q=True, rgbValue=True)
        self.setStyleSheet(
            f"background-color : rgb({str(color_values[0]*255)},{color_values[1]*255},{color_values[2]*255});"
        )
        color = QtGui.QColor(color[0] * 255, color[1] * 255, color[2] * 255)
        return color

    def on_color_changed(self, *args):
        self.color_changed.emit(self.get_color())


class LightTransformShapeNodes:
    def __init__(self):
        self.dictLights = {}
        self.transform_nodes = []
        self.shape_nodes = []
        self.shape_nodes = cmds.ls(type=cmds.listNodeTypes("light"))
        for shape_node in self.shape_nodes:
            transform_node = cmds.listRelatives(shape_node, type="transform", p=True)
            self.transform_nodes.append(transform_node[0])
            self.dictLights[transform_node[0]] = [transform_node[0], shape_node]
        # print(self.transform_nodes)
        # print(self.shape_nodes)

    def getTransformNode(self, lightNameTransform):
        return self.dictLights[lightNameTransform][0]

    def getShapeNode(self, lightNameTransform):
        return self.dictLights[lightNameTransform][1]

    def print_attributes(self):
        if len(self.transform_nodes) != 0:
            listAttributes = cmds.listAttr(self.getShapeNode(self.transform_nodes[2]))
            for attr in listAttributes:
                pass

    def modifyAttribute(self, nameOfAttribute, light):
        verificationList = cmds.listAttr(light)


class LightItem(QtWidgets.QWidget):

    # SUPPORTED_TYPES = ["ambientLight", "directionalLight", "pointLight", "spotLight"]
    SUPPORTED_TYPES = cmds.listNodeTypes("light")
    # print(SUPPORTED_TYPES)
    EMIT_TYPES = ["directionalLight", "pointLight", "spotLight", "areaLight", "volumeLight"]
    # TODO add attributes declare variables
    # MAYA LIGHTS
    MAYA_TYPES = [
        "directionalLight",
        "pointLight",
        "spotLight",
        "ambientLight",
        "areaLight",
    ]

    MAYA_ATTRIBUTES_DIRECTIONALLIGHT = [
        ("intensity", "float"),
        ("aiAngle", "float"),
    ]

    MAYA_ATTRIBUTES_AMBIENTLIGHT = [
        ("intensity", "float"),
        ("ambientShade", "float"),
    ]

    MAYA_ATTRIBUTES_POINTLIGHT = [
        ("aiUseColorTemperature", "bool"),
        ("aiColorTemperature", "float"),
        ("aiExposure", "float"),
        ("aiSamples", "int"),
        ("aiNormalize", "bool"),
        ("aiCastShadows", "bool"),
        ("aiShadowDensity", "float"),
        ("aiVolumeSamples", "int"),
        ("aiRadius", "float"),
    ]

    MAYA_ATTRIBUTES_SPOTLIGHT = [
        ("coneAngle", "doubleAngle"),
        ("aiUseColorTemperature", "bool"),
        ("aiColorTemperature", "float"),
        ("aiExposure", "float"),
        ("aiSamples", "int"),
        ("aiRadius", "float"),
        ("aiNormalize", "bool"),
        ("aiRoundness", "float"),
        ("aiCastShadows", "bool"),
        ("aiShadowDensity", "float"),
        ("aiAspectRatio", "float"),
        ("aiLensRadius", "float"),
        ("aiCastVolumetricShadows", "bool"),
        ("aiVolumeSamples", "int"),
    ]

    MAYA_ATTRIBUTES_AREALIGHT = [
        ("intensity", "float"),
        ("aiShadowDensity", "float"),
    ]

    # ARNOLD LIGHTS
    ARNOLD_TYPES = [
        "aiAreaLight",
        "aiMeshLight",
        "aiPhotometricLight",
        "aiSkyDomeLight",
    ]

    ARNOLD_ATTRIBUTES_AREALIGHT = [
        ("exposure", "float"),
        ("aiUseColorTemperature", "bool"),
        ("aiColorTemperature", "float"),
        ("aiSpread", "float"),
        ("aiResolution", "int"),
        ("aiRoundness", "float"),
        ("aiSoftEdge", "float"),
        ("aiSamples", "int"),
        ("aiNormalize", "bool"),
        ("aiCastShadows", "bool"),
        ("aiShadowDensity", "float"),
        ("aiCastVolumetricShadows", "bool"),
        # if you want to add specific attributes, just integrate them in the dedicated lists
        ("aiVolumeSamples", "int"),
    ]

    ARNOLD_ATTRIBUTES_MESHLIGHT = [
        ("aiUseColorTemperature", "bool"),
        # ("aiColorTemperature", "float"),
        # ("aiSamples", "int"),
        # ("aiCastShadows", "bool"),
        # ("aiShadowDensity", "float"),
    ]

    ARNOLD_ATTRIBUTES_SKYDOMELIGHT = [
        ("intensity", "float"),
        # ("aiVolume", "float"),
        # ("aiMaxBounces", "long"),
        # ("camera", "float"),
        # ("aiDiffuse", "float"),
        # ("aiSamples", "float"),
    ]

    ARNOLD_ATTRIBUTES_PHOTOMETRICLIGHT = [
        ("intensity", "float"),
        ("exposure", "float"),
        # ("aiColor", "float"),
        ("aiUseColorTemperature", "bool"),
    ]

    node_deleted = QtCore.Signal(str)

    def __init__(self, shape_name, parent=None):
        super(LightItem, self).__init__(parent)

        # self.setFixedHeight(26)
        self.shape_name = shape_name
        self.uuid = cmds.ls(shape_name, uuid=True)

        # debug ui
        # self.minimum_size = 0

        self.script_jobs = []

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.create_script_jobs()
        self.custom_set_style_sheet()

    def custom_set_style_sheet(self):

        # self.set_style_sheet_Desc_Label_wdg(self.emit_diffuse_cb,self.FONT_COLOR_TITLE,self.FONT_LIST, self.FONT_SIZE_DESC)
        # self.set_style_sheet_Desc_Label_wdg(self.emit_specular_cb,self.FONT_COLOR_TITLE,self.FONT_LIST, self.FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.generic_attribute_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.area_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.directional_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.point_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.spot_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.ambient_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)

        # For arnold widget
        set_style_sheet_Desc_Label_wdg(self.arnold_area_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.arnold_mesh_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.arnold_photometric_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)
        set_style_sheet_Desc_Label_wdg(self.arnold_skydome_light_lbl, FONT_COLOR_DESC, FONT_LIST, FONT_SIZE_DESC)

    def create_widgets(self):
        # first line header for each light
        self.light_type_btn = QtWidgets.QPushButton()
        self.light_type_btn.setFixedSize(20, 20)
        self.light_type_btn.setFlat(True)

        # widget shown inside collapsible element
        self.generic_attribute_lbl = QtWidgets.QLabel("GENERIC ATTRIBUTES")
        self.directional_light_lbl = QtWidgets.QLabel("DIRECTIONAL LIGHT ATTRIBUTES")
        self.ambient_light_lbl = QtWidgets.QLabel("AMBIENT LIGHT ATTRIBUTES")
        self.point_light_lbl = QtWidgets.QLabel("POINT LIGHT ATTRIBUTES")
        self.spot_light_lbl = QtWidgets.QLabel("SPOT LIGHT ATTRIBUTES")
        self.area_light_lbl = QtWidgets.QLabel("AREA LIGHT ATTRIBUTES")
        self.arnold_area_light_lbl = QtWidgets.QLabel("ARNOLD AREA LIGHT ATTRIBUTES")
        self.arnold_mesh_light_lbl = QtWidgets.QLabel("ARNOLD MESH LIGHT ATTRIBUTES")
        self.arnold_skydome_light_lbl = QtWidgets.QLabel("ARNOLD SKYDOME LIGHT ATTRIBUTES")
        self.arnold_photometric_light_lbl = QtWidgets.QLabel("ARNOLD PHOTOMETRIC LIGHT ATTRIBUTES")

        # Changing background of the icon light button when hover
        self.light_type_btn.setStyleSheet(
            f"""
                                        QPushButton:hover{{
                                        background-color : #1D65A6;
                                        border-radius : 5px; 
                                            }}"""
        )

        self.visiblity_cb = QtWidgets.QCheckBox()

        self.transform_name_label = QtWidgets.QLabel("placeholder")
        self.transform_name_label.setFixedWidth(120)
        self.transform_name_label.setAlignment(QtCore.Qt.AlignCenter)
        set_style_sheet_Desc_Label_wdg(self.transform_name_label, FONT_COLOR_TITLE, FONT_LIST, FONT_SIZE_DESC)

        # light_item_scroll_area = QtWidgets.QScrollArea()
        # light_item_scroll_area.setWidgetResizable(True)
        # light_item_scroll_area.setWidget(self)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            # print("light_type in self.SUPPORTED_TYPES start")
            self.intensity_dsb = QtWidgets.QDoubleSpinBox()
            # self.intensity_dsb.setRange(0.0, 1000.0)
            self.intensity_dsb.setMinimum(0.0)
            self.intensity_dsb.setMaximum(1000.0)
            # self.intensity_dsb.setDecimals(2)
            self.intensity_dsb.setSingleStep(0.20)
            self.intensity_dsb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            set_style_sheet_double_spine_box_edit(self.intensity_dsb)

            self.color_btn = CustomColorButton()
            # # print("light_type in self.SUPPORTED_TYPES end")

            if light_type in self.EMIT_TYPES:
                # # print("light_type in self.EMIT_TYPES start")
                self.emit_diffuse_cb = QtWidgets.QCheckBox("Emit Diffuse")
                self.emit_specular_cb = QtWidgets.QCheckBox("Emit Specular")
                # # print("light_type in self.EMIT_TYPES end")

            # TODO add attributes create widgets
            if light_type in self.MAYA_TYPES:
                if light_type == "directionalLight":
                    self.directional_widgets = []

                    for nameAttr, typeAttr in self.MAYA_ATTRIBUTES_DIRECTIONALLIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.directional_widgets.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    print(self.directional_widgets)
                if light_type == "ambientLight":
                    self.ambient_lights = []

                    for nameAttr, typeAttr in self.MAYA_ATTRIBUTES_AMBIENTLIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.ambient_lights.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    print(self.ambient_lights)

                if light_type == "pointLight":
                    self.point_lights = []

                    for nameAttr, typeAttr in self.MAYA_ATTRIBUTES_POINTLIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.point_lights.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    print(self.point_lights)

                if light_type == "spotLight":
                    self.spot_lights = []

                    for nameAttr, typeAttr in self.MAYA_ATTRIBUTES_SPOTLIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.spot_lights.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    print(self.spot_lights)

                if light_type == "areaLight":
                    self.area_lights = []

                    for nameAttr, typeAttr in self.MAYA_ATTRIBUTES_AREALIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.area_lights.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    print(self.area_lights)

            if light_type in self.ARNOLD_TYPES:
                if light_type == "aiAreaLight":
                    self.area_arnold_widgets = []
                    for nameAttr, typeAttr in self.ARNOLD_ATTRIBUTES_AREALIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.area_arnold_widgets.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    # print(self.area_widgets)
                if light_type == "aiMeshLight":
                    self.mesh_widgets = []
                    for nameAttr, typeAttr in self.ARNOLD_ATTRIBUTES_MESHLIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.mesh_widgets.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    # print(self.mesh_widgets)
                if light_type == "aiSkyDomeLight":
                    self.skydome_widgets = []
                    for nameAttr, typeAttr in self.ARNOLD_ATTRIBUTES_SKYDOMELIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.skydome_widgets.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    # print(self.skydome_widgets)
                if light_type == "aiPhotometricLight":
                    self.photometric_widgets = []
                    for nameAttr, typeAttr in self.ARNOLD_ATTRIBUTES_PHOTOMETRICLIGHT:
                        # TODO dynamic types
                        typeAttr = cmds.getAttr(f"{self.shape_name}.{nameAttr}", typ=True)
                        print(typeAttr)
                        self.photometric_widgets.append(self.create_tuple_widgetLbl_widgetType(nameAttr, typeAttr))
                    # print(self.photometric_widgets)

        self.update_values()

    def create_tuple_widgetLbl_widgetType(self, nameAttr, typeAttr):
        widget_lbl = QtWidgets.QLabel(nameAttr)
        set_style_sheet_Desc_Label_wdg(widget_lbl, FONT_COLOR_TITLE, FONT_LIST, FONT_SIZE_DESC)

        types_spinbox = [
            "float",
            "long",
            "double",
            "int",
            "doubleAngle",
        ]

        if typeAttr == "bool":
            widget = QtWidgets.QCheckBox()
        elif typeAttr in types_spinbox:
            widget = QtWidgets.QDoubleSpinBox()
            widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

            # Set styleSheet to change backgroun-color to white when focus on it
            set_style_sheet_double_spine_box_edit(widget)
            ####################################################################

            mxe = cmds.attributeQuery(nameAttr, node=self.shape_name, mxe=True)
            mne = cmds.attributeQuery(nameAttr, node=self.shape_name, mne=True)
            print("mne mxe")
            print(mne, mxe)
            default_max_min = 10000.0
            if mxe:
                max = cmds.attributeQuery(nameAttr, node=self.shape_name, max=True)[0]
                print("max:")
                print(max)
                widget.setMaximum(max)
            else:
                widget.setMaximum(default_max_min)
            if mne:
                # max = cmds.attributeQuery(nameAttr, node=self.shape_name, softRange=True)
                min = cmds.attributeQuery(nameAttr, node=self.shape_name, min=True)[0]
                print("min:")
                print(min)
                widget.setMinimum(min)
            else:
                widget.setMinimum(-default_max_min)
        else:
            # print("type not recognized")
            widget = None

        return (widget_lbl, widget)

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        # main_layout.setAlignment(QtCore.Qt.AlignCenter)
        # self.setLayout(main_layout)
        # debug ui
        # self.n_lines = 0

        first_line_layout = QtWidgets.QHBoxLayout()

        first_line_layout.setContentsMargins(0, 0, 0, 0)
        first_line_layout.addWidget(self.light_type_btn)
        first_line_layout.addWidget(self.visiblity_cb)
        first_line_layout.addWidget(self.transform_name_label)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            # print("light_type in self.SUPPORTED_TYPES layout")
            first_line_layout.addWidget(self.intensity_dsb)

            first_line_layout.addSpacing(1)
            first_line_layout.addWidget(self.color_btn)

            if light_type in self.EMIT_TYPES:
                # print("light_type in self.EMIT_TYPES layout START")
                # first_line_layout.addSpacing(1)
                first_line_layout.addWidget(self.emit_diffuse_cb)
                # first_line_layout.addSpacing(2)
                first_line_layout.addWidget(self.emit_specular_cb)
                # print("light_type in self.EMIT_TYPES layout END")
            # TODO add attributes create layout
            if light_type in self.MAYA_TYPES:
                maya_main_vlayout = QtWidgets.QVBoxLayout()
                maya_layout_lines = []

                if light_type == "directionalLight":
                    first_line_maya = QtWidgets.QHBoxLayout()
                    first_line_maya.addWidget(self.directional_light_lbl)
                    maya_layout_lines.append(first_line_maya)
                    for lbl, wdg in self.directional_widgets:
                        maya_line_layout = QtWidgets.QHBoxLayout()
                        maya_line_layout.addWidget(lbl)
                        maya_line_layout.addWidget(wdg)
                        maya_layout_lines.append(maya_line_layout)

                if light_type == "ambientLight":
                    first_line_maya = QtWidgets.QHBoxLayout()
                    first_line_maya.addWidget(self.ambient_light_lbl)
                    maya_layout_lines.append(first_line_maya)
                    for lbl, wdg in self.ambient_lights:
                        maya_line_layout = QtWidgets.QHBoxLayout()
                        maya_line_layout.addWidget(lbl)
                        maya_line_layout.addWidget(wdg)
                        maya_layout_lines.append(maya_line_layout)

                if light_type == "pointLight":
                    first_line_maya = QtWidgets.QHBoxLayout()
                    first_line_maya.addWidget(self.point_light_lbl)
                    maya_layout_lines.append(first_line_maya)
                    for lbl, wdg in self.point_lights:
                        maya_line_layout = QtWidgets.QHBoxLayout()
                        maya_line_layout.addWidget(lbl)
                        maya_line_layout.addWidget(wdg)
                        maya_layout_lines.append(maya_line_layout)

                if light_type == "spotLight":
                    first_line_maya = QtWidgets.QHBoxLayout()
                    first_line_maya.addWidget(self.spot_light_lbl)
                    maya_layout_lines.append(first_line_maya)
                    for lbl, wdg in self.spot_lights:
                        maya_line_layout = QtWidgets.QHBoxLayout()
                        maya_line_layout.addWidget(lbl)
                        maya_line_layout.addWidget(wdg)
                        maya_layout_lines.append(maya_line_layout)

                if light_type == "areaLight":
                    first_line_maya = QtWidgets.QHBoxLayout()
                    first_line_maya.addWidget(self.area_light_lbl)
                    maya_layout_lines.append(first_line_maya)
                    for lbl, wdg in self.area_lights:
                        maya_line_layout = QtWidgets.QHBoxLayout()
                        maya_line_layout.addWidget(lbl)
                        maya_line_layout.addWidget(wdg)
                        maya_layout_lines.append(maya_line_layout)

                if maya_layout_lines:
                    print("if maya_layout_lines")
                    for maya_line_layout in maya_layout_lines:
                        maya_main_vlayout.addLayout(maya_line_layout)
                else:
                    print("not if maya_layout_lines")

            if light_type in self.ARNOLD_TYPES:
                arnold_main_vlayout = QtWidgets.QVBoxLayout()
                # arnold_main_vlayout.setContentsMargins(2,2,2,2)
                arnold_layout_lines = []
                if light_type == "aiAreaLight":
                    first_line_arnold = QtWidgets.QHBoxLayout()
                    first_line_arnold.addWidget(self.arnold_area_light_lbl)
                    arnold_layout_lines.append(first_line_arnold)
                    for lbl, wdg in self.area_arnold_widgets:
                        arnold_line_layout = QtWidgets.QHBoxLayout()
                        arnold_line_layout.addWidget(lbl)
                        arnold_line_layout.addWidget(wdg)
                        arnold_layout_lines.append(arnold_line_layout)
                elif light_type == "aiMeshLight":
                    first_line_arnold = QtWidgets.QHBoxLayout()
                    first_line_arnold.addWidget(self.arnold_mesh_light_lbl)
                    arnold_layout_lines.append(first_line_arnold)
                    for lbl, wdg in self.mesh_widgets:
                        arnold_line_layout = QtWidgets.QHBoxLayout()
                        arnold_line_layout.addWidget(lbl)
                        arnold_line_layout.addWidget(wdg)
                        arnold_layout_lines.append(arnold_line_layout)
                elif light_type == "aiSkyDomeLight":
                    first_line_arnold = QtWidgets.QHBoxLayout()
                    first_line_arnold.addWidget(self.arnold_skydome_light_lbl)
                    arnold_layout_lines.append(first_line_arnold)
                    for lbl, wdg in self.skydome_widgets:
                        arnold_line_layout = QtWidgets.QHBoxLayout()
                        arnold_line_layout.addWidget(lbl)
                        arnold_line_layout.addWidget(wdg)

                        arnold_layout_lines.append(arnold_line_layout)
                elif light_type == "aiPhotometricLight":
                    first_line_arnold = QtWidgets.QHBoxLayout()
                    first_line_arnold.addWidget(self.arnold_photometric_light_lbl)
                    arnold_layout_lines.append(first_line_arnold)
                    for lbl, wdg in self.photometric_widgets:
                        arnold_line_layout = QtWidgets.QHBoxLayout()
                        arnold_line_layout.addWidget(lbl)
                        arnold_line_layout.addWidget(wdg)

                        arnold_layout_lines.append(arnold_line_layout)
                else:
                    # print("no match arnold type")
                    pass

                if arnold_layout_lines:
                    for arnold_line_layout in arnold_layout_lines:
                        arnold_main_vlayout.addLayout(arnold_line_layout)

        # first_line_layout.addStretch()
        # first_line_layout.addSpacing(1)

        main_layout.addWidget(self.generic_attribute_lbl)
        # self.n_lines += 1
        main_layout.addLayout(first_line_layout)
        # self.n_lines += 1

        self.line = QtWidgets.QFrame()
        self.line.setGeometry(QtCore.QRect(60, 110, 751, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # TODO add attributes add layout
        if light_type in self.MAYA_TYPES:
            print("create_layout() in maya types")
            main_layout.addWidget(self.line)
            main_layout.addSpacing(20)
            main_layout.addLayout(maya_main_vlayout)
        if light_type in self.ARNOLD_TYPES:
            main_layout.addWidget(self.line)
            main_layout.addSpacing(20)
            main_layout.addLayout(arnold_main_vlayout)

    def create_connections(self):
        self.light_type_btn.clicked.connect(self.select_light)
        self.visiblity_cb.toggled.connect(self.set_visibility)
        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb.editingFinished.connect(self.on_intensity_changed)
            self.color_btn.color_changed.connect(self.set_color)
            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb.toggled.connect(self.set_emit_diffuse)
                self.emit_specular_cb.toggled.connect(self.set_emit_specular)
            # TODO add attributes connections callback
            if light_type in self.MAYA_TYPES:
                if light_type == "directionalLight":
                    print(f"type is {light_type}")
                    for qlabel, qwidget in self.directional_widgets:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                if light_type == "ambientLight":
                    print(f"type is {light_type}")
                    for qlabel, qwidget in self.ambient_lights:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                if light_type == "pointLight":
                    print(f"type is {light_type}")
                    for qlabel, qwidget in self.point_lights:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                if light_type == "spotLight":
                    print(f"type is {light_type}")
                    for qlabel, qwidget in self.spot_lights:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                if light_type == "areaLight":
                    print(f"type is {light_type}")
                    for qlabel, qwidget in self.area_lights:
                        self.connect_widgets_dynamic(qlabel, qwidget)

            if light_type in self.ARNOLD_TYPES:
                if light_type == "aiAreaLight":
                    for qlabel, qwidget in self.area_arnold_widgets:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                elif light_type == "aiMeshLight":
                    for qlabel, qwidget in self.mesh_widgets:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                elif light_type == "aiSkyDomeLight":
                    for qlabel, qwidget in self.skydome_widgets:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                elif light_type == "aiPhotometricLight":
                    for qlabel, qwidget in self.photometric_widgets:
                        self.connect_widgets_dynamic(qlabel, qwidget)
                else:
                    pass
                    # print("no match arnold type in create_connections()")
                    # self.exposure_dsb.editingFinished.connect(self.on_exposure_changed)

    def connect_widgets_dynamic(self, qlabel, qwidget):
        print("connect_widgets_dynamic()")
        print(qlabel, qwidget)
        attr_name = qlabel.text()
        print(attr_name)
        classname = qwidget.metaObject().className()
        print(classname)
        if classname == "QDoubleSpinBox":
            value = qwidget.value()
            qwidget.editingFinished.connect(partial(self.on_QDoubleSpinBox_changed, qwidget, attr_name))
        if classname == "QCheckBox":
            state = qwidget.isChecked()
            qwidget.toggled.connect(partial(self.on_QCheckBox_changed, qwidget, attr_name))

    def update_values(self):
        self.transform_name_label.setText(self.get_transform_name())
        self.visiblity_cb.setChecked(self.is_visible())
        self.light_type_btn.setIcon(self.get_light_type_icon())

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb.setValue(self.get_intensity())
            # print(self.intensity_dsb)
            self.color_btn.set_color(self.get_color())
            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb.setChecked(self.emits_diffuse())
                self.emit_specular_cb.setChecked(self.emits_specular())
            # TODO add attributes update value
            if light_type in self.MAYA_TYPES:
                if light_type == "directionalLight":
                    for qlabel, qwidget in self.directional_widgets:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "ambientLight":
                    for qlabel, qwidget in self.ambient_lights:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "pointLight":
                    for qlabel, qwidget in self.point_lights:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "spotLight":
                    for qlabel, qwidget in self.spot_lights:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "areaLight":
                    for qlabel, qwidget in self.area_lights:
                        self.update_value_widget(qlabel, qwidget)

            if light_type in self.ARNOLD_TYPES:
                if light_type == "aiAreaLight":
                    for qlabel, qwidget in self.area_arnold_widgets:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "aiMeshLight":
                    for qlabel, qwidget in self.mesh_widgets:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "aiSkyDomeLight":
                    for qlabel, qwidget in self.skydome_widgets:
                        self.update_value_widget(qlabel, qwidget)
                if light_type == "aiPhotometricLight":
                    for qlabel, qwidget in self.photometric_widgets:
                        self.update_value_widget(qlabel, qwidget)

    def update_value_widget(self, qlabel, qwidget):
        print(qlabel, qwidget)
        attr_name = qlabel.text()
        print(attr_name)
        print(qlabel.text(), qwidget)
        classname = qwidget.metaObject().className()
        if classname == "QDoubleSpinBox":
            # qwidget.setValue(.66)
            qwidget.setValue(self.get_attribute_from_widget(attr_name=attr_name))
        if classname == "QCheckBox":
            qwidget.setChecked(self.get_attribute_from_widget(attr_name=attr_name))
            # qwidget.setChecked(False)

    def get_transform_name(self):
        return cmds.listRelatives(self.shape_name, parent=True)[0]

    def get_attribute_value(self, name, attribute):
        return cmds.getAttr("{0}.{1}".format(name, attribute))

    def set_attribute_value(self, name, attribute, *args):
        print("set_attribute_value enter")
        attr_name = "{0}.{1}".format(name, attribute)
        print(name, attribute, attr_name, args)

        cmds.setAttr(attr_name, *args)

    def is_visible(self):
        transform_name = self.get_transform_name()
        return self.get_attribute_value(transform_name, "visibility")

    def get_light_type(self):
        return cmds.objectType(self.shape_name)

    def get_light_type_icon(self):
        light_type = self.get_light_type()
        # print(light_type)
        icon = QtGui.QIcon()
        if light_type == "ambientLight":
            icon = QtGui.QIcon(":ambientLight.svg")
        elif light_type == "directionalLight":
            icon = QtGui.QIcon(":directionalLight.svg")
        elif light_type == "pointLight":
            icon = QtGui.QIcon(":pointLight.svg")
        elif light_type == "spotLight":
            icon = QtGui.QIcon(":spotLight.svg")
        elif light_type == "areaLight":
            icon = QtGui.QIcon(":areaLight.svg")
        # arnold lights
        # TODO le chemin ne marche pas avec le chemin relatif !?
        elif light_type == "aiAreaLight":
            area_icon_path = "C:/Program Files/Autodesk/Arnold/maya2022/icons/AreaLightShelf.png"
            # area_icon_path = "./icons/AreaLightShelf.png"

            icon = QtGui.QIcon(area_icon_path)
            # print("aiAreaLight")
        elif light_type == "aiMeshLight":
            aiMesh_icon_path = "C:/Program Files/Autodesk/Arnold/maya2022/icons/MeshLightShelf.png"
            icon = QtGui.QIcon(aiMesh_icon_path)
        elif light_type == "aiPhotometricLight":
            aiPhotometric_icon_path = "C:/Program Files/Autodesk/Arnold/maya2022/icons/PhotometricLightShelf.png"
            icon = QtGui.QIcon(aiPhotometric_icon_path)
        elif light_type == "aiSkyDomeLight":
            aiSkyDome_icon_path = "C:/Program Files/Autodesk/Arnold/maya2022/icons/SkyDomeLightShelf.png"
            icon = QtGui.QIcon(aiSkyDome_icon_path)

        else:
            icon = QtGui.QIcon(":Light.png")
        return icon

    def get_intensity(self):
        return self.get_attribute_value(self.shape_name, "intensity")

    def get_exposure(self):
        return self.get_attribute_value(self.shape_name, "exposure")

    def get_attribute_from_widget(self, attr_name):
        print("get_attribute_from_widget")
        print(self.shape_name, attr_name)
        return self.get_attribute_value(self.shape_name, attr_name)

    def get_color(self):
        temp_color = self.get_attribute_value(self.shape_name, "color")[0]
        # print(temp_color)
        color = QtGui.QColor(
            temp_color[0] * 255,
            temp_color[1] * 255,
            temp_color[2] * 255,
        )
        return color

    def emits_diffuse(self):
        return self.get_attribute_value(self.shape_name, "emitDiffuse")

    def emits_specular(self):
        return self.get_attribute_value(self.shape_name, "emitSpecular")

    def select_light(self):
        cmds.select(self.get_transform_name())

    def set_visibility(self, checked):
        self.set_attribute_value(self.get_transform_name(), "visibility", checked)

    def on_intensity_changed(self):
        self.set_attribute_value(self.shape_name, "intensity", self.intensity_dsb.value())

    def on_exposure_changed(self):
        # print("on_exposure_changed")
        self.set_attribute_value(self.shape_name, "exposure", self.exposure_dsb.value())

    def on_QDoubleSpinBox_changed(self, qdsb, attr_name):
        # print("on_QDoubleSpinBox_changed value: " + str(attr_name))
        # print(qdsb)
        value = qdsb.value()
        # print(value)
        self.set_attribute_value(self.shape_name, attr_name, value)

    def on_QCheckBox_changed(self, qcb, attr_name, state):
        # print("on_QCheckBox_changed value: " + str(attr_name) + " " + str(state))
        # print(qcb)
        self.set_attribute_value(self.shape_name, attr_name, state)

    def set_color(self, color):
        # print(color)
        self.set_attribute_value(
            self.shape_name,
            "color",
            color.redF(),
            color.greenF(),
            color.blueF(),
        )

    def set_emit_diffuse(self, checked):
        # print("set_emit_diffuse")
        self.set_attribute_value(self.shape_name, "emitDiffuse", checked)

    def set_emit_specular(self, checked):
        # print("set_emit_specular")
        self.set_attribute_value(self.shape_name, "emitSpecular", checked)

    def on_node_deleted(self):
        self.node_deleted.emit(self.shape_name)

    def on_name_changed(self):
        # UUID universal uniq identifier
        self.shape_name = cmds.ls(self.uuid)[0]
        self.update_values()

    def create_script_jobs(self):
        self.delete_script_jobs()
        # TODO ajouter pour chaque attribut?
        self.add_attribute_change_script_jobs(self.get_transform_name(), "visibility")
        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.add_attribute_change_script_jobs(self.shape_name, "color")
            self.add_attribute_change_script_jobs(self.shape_name, "intensity")
            if light_type in self.EMIT_TYPES:
                self.add_attribute_change_script_jobs(self.shape_name, "emitDiffuse")
                self.add_attribute_change_script_jobs(self.shape_name, "emitSpecular")
            # TODO add attributes scriptjob
            if light_type in self.MAYA_TYPES:
                if light_type == "directionalLight":
                    for attrName, _ in self.MAYA_ATTRIBUTES_DIRECTIONALLIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "ambientLight":
                    for attrName, _ in self.MAYA_ATTRIBUTES_AMBIENTLIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "pointLight":
                    for attrName, _ in self.MAYA_ATTRIBUTES_POINTLIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "spotLight":
                    for attrName, _ in self.MAYA_ATTRIBUTES_SPOTLIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "areaLight":
                    for attrName, _ in self.MAYA_ATTRIBUTES_AREALIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)

            if light_type in self.ARNOLD_TYPES:
                if light_type == "aiAreaLight":
                    for attrName, _ in self.ARNOLD_ATTRIBUTES_AREALIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "aiMeshLight":
                    for attrName, _ in self.ARNOLD_ATTRIBUTES_MESHLIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "aiSkyDomeLight":
                    for attrName, _ in self.ARNOLD_ATTRIBUTES_SKYDOMELIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)
                if light_type == "aiPhotometricLight":
                    for attrName, _ in self.ARNOLD_ATTRIBUTES_PHOTOMETRICLIGHT:
                        self.add_attribute_change_script_jobs(self.shape_name, attrName)

        scriptjob_number1 = cmds.scriptJob(nodeDeleted=(self.shape_name, partial(self.on_node_deleted)))
        self.script_jobs.append(scriptjob_number1)
        scriptjob_number2 = cmds.scriptJob(nodeNameChanged=(self.shape_name, partial(self.on_name_changed)))
        self.script_jobs.append(scriptjob_number2)

    def add_attribute_change_script_jobs(self, name, attribute):
        sjn = cmds.scriptJob(
            attributeChange=(
                "{0}.{1}".format(name, attribute),
                partial(self.update_values),
            )
        )
        self.script_jobs.append(sjn)

    def delete_script_jobs(self):
        # print("delete_script_jobs")
        for job_number in self.script_jobs:
            if cmds.scriptJob(exists=job_number):
                cmds.scriptJob(kill=job_number, force=True)
            cmds.evalDeferred(
                "if cmds.scriptJob(exists={0}):\n\tcmds.scriptJob(kill={0}, force=True)".format(job_number)
            )
        self.script_jobs = []


class LightPanel(QtWidgets.QDialog):

    WINDOW_TITLE = "Custom Light Editor"

    # Creating all the static variable used in function styleSheet
    def __init__(self, parent=maya_main_window()):
        super(LightPanel, self).__init__(parent)
        self.setStyleSheet(f"background-color : {MAIN_BACKGROUND_COLOR};")
        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.resize(700, 350)
        self.light_items = []
        self.script_jobs = []
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.refreshButton = QtWidgets.QPushButton("Refresh Lights Names")
        set_style_sheet_btn(self.refreshButton, BTN_BACKGROUND_COLOR, FONT_LABEL_DESC)
        self.title_lbl = QtWidgets.QLabel(
            "<span style='color:green'>GUILIC</span> Custom <span style='color:green'>Light</span> Editor"
        )
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setContentsMargins(0, 15, 0, 15)
        set_style_sheet_title_wdg(self.title_lbl, FONT_LABEL_DESC, FONT_SIZE_TITLE)

    def create_layout(self):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Light"))
        header_layout.addSpacing(50)
        header_layout.addWidget(QtWidgets.QLabel("Intensity"))
        header_layout.addSpacing(44)
        header_layout.addWidget(QtWidgets.QLabel("Color"))
        header_layout.addSpacing(24)
        header_layout.addWidget(QtWidgets.QLabel("Emit Diffuse"))
        header_layout.addSpacing(10)
        header_layout.addWidget(QtWidgets.QLabel("Emit Spec"))
        header_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refreshButton)

        light_list_wdg = QtWidgets.QWidget()

        # light_list_wdg.setStyleSheet(
        #     """
        #         border-width: 2px;
        #         border-radius: 10px;
        #         border-color: red;
        #     """
        # )
        # debug ui
        light_list_wdg.setContentsMargins(0, 0, 0, 0)
        self.light_layout = QtWidgets.QVBoxLayout(light_list_wdg)
        self.light_layout.setContentsMargins(2, 2, 2, 2)

        # self.light_layout.setSpacing(1)
        # self.light_layout.setAlignment(QtCore.Qt.AlignTop)
        # self.light_layout.addStretch()

        light_list_scroll_area = QtWidgets.QScrollArea()
        light_list_scroll_area.setWidgetResizable(True)
        light_list_scroll_area.setWidget(light_list_wdg)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        # main_layout.addLayout(header_layout)
        main_layout.addWidget(self.title_lbl)

        main_layout.addWidget(light_list_scroll_area)
        main_layout.addLayout(button_layout)

        # main_layout.addWidget(container)

    def create_connections(self):
        self.refreshButton.clicked.connect(self.refresh_lights)

    def get_lights_in_scene(self):
        return cmds.ls(type=cmds.listNodeTypes("light"))

    def refresh_lights(self):
        # print("refresh_lights")
        self.clear_lights()
        scene_lights = self.get_lights_in_scene()
        count_header = 0
        for light in scene_lights:
            # print(light)

            light_item = LightItem(light)
            # TODO change this value hard coding

            light_item.setContentsMargins(1, 1, 1, 1)

            light_item.node_deleted.connect(self.on_node_deleted)

            self.container_name = light_item.get_transform_name()
            container = Container(self.container_name)

            if count_header % 2:
                container.header.setStyleSheet(
                    f"""
                                QWidget{{
                                    background-color : {SECOND_BACKGROUND_COLOR}; 
                                }} 
                                """
                )
            else:
                container.header.setStyleSheet(
                    f"""
                                QWidget{{
                                    background-color : {SECOND_BACKGROUND_CLOSE_COLOR}; 
                                }}
                                """
                )

            self.light_layout.addWidget(container)

            content_layout = QtWidgets.QGridLayout(container.contentWidget)
            content_layout.addWidget(light_item)

            self.light_items.append(light_item)

            self.light_items.append(light_item)
            count_header += 1

    def clear_lights(self):
        for light in self.light_items:
            light.delete_script_jobs()

        self.light_items = []
        while self.light_layout.count() > 0:
            light_item = self.light_layout.takeAt(0)
            if light_item.widget():
                light_item.widget().deleteLater()

    def create_script_jobs(self):
        sjn = cmds.scriptJob(event=["DagObjectCreated", partial(self.on_dag_object_created)])
        self.script_jobs.append(sjn)
        sjn = cmds.scriptJob(event=["Undo", partial(self.on_undo)])
        self.script_jobs.append(sjn)
        # print(self.script_jobs)

    def delete_script_jobs(self):
        for script_job in self.script_jobs:
            cmds.scriptJob(kill=script_job)
        self.script_jobs = []

    def on_dag_object_created(self):
        if len(cmds.ls(type="light")) != len(self.light_items):
            # print("new light created...")
            self.refresh_lights()

    def on_undo(self):
        if len(cmds.ls(type="light")) != len(self.light_items):
            # print("undo light created...")
            self.refresh_lights()

    def on_node_deleted(self):
        self.refresh_lights()

    def showEvent(self, event):
        self.create_script_jobs()
        self.refresh_lights()

    def closeEvent(self, event):
        self.delete_script_jobs()
        self.clear_lights()


if __name__ == "__main__":

    try:
        light_panel_dialog.close()  # pylint: disable=E0601
        light_panel_dialog.deleteLater()
    except:
        pass

    light_panel_dialog = LightPanel()
    light_panel_dialog.show()
