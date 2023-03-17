from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

import re

import os


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class AutoShaderDialog(QtWidgets.QDialog):

    # Creating all the generic variable to use
    FONT_LIST = QtGui.QFont("Turis Light")
    FONT_LABEL_DESC = QtGui.QFont("Retro Computer")
    MAIN_BACKGROUND_COLOR = "#192E5B"
    SECOND_BACKGROUND_COLOR = "#1D65A6"
    THIRD_BACKGROUND_COLOR = "#72A2C0"
    BTN_BACKGROUND_COLOR = "#00743F"
    FONT_COLOR_DESC = "#F2A104"
    FONT_COLOR_TITLE = "white"
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
            <li>If you want to import textures from a folder click on the radio button all at the bottom of the window </li>
            <br>
            <li>Fill the maps to correspond to your files names and respect the nomenclature, check the checkbox to tell which texture type you want</li>
            <br>
            <li>If you want to import each file specificly then select 'selected' and do this : </li>
            <br>
            <li>Click below base_color etc and choose your file</li>
            <br>
            <li>When you have your wanted textures clcick on the 'Apply textures' button</li>
        </ul>"""
    )

    def __init__(self, parent=maya_main_window()):
        print("init()")
        super(AutoShaderDialog, self).__init__(parent)

        self.extension_filters = [".png", ".exr", ".jpg", ".jpeg"]

        self.extension_str = " ".join(["*" + ext for ext in self.extension_filters])
        print(self.extension_str)

        self.default_text_path = "G:/ATI-M1/INTENSIFS_sem1/auto-shader/textures/dflt_text.png"
        self.texture_files_path = {
            "color": f"{self.default_text_path}",
            "metalness": f"{self.default_text_path}",
            "specular": f"{self.default_text_path}",
            "normal": f"{self.default_text_path}",
        }

        self.setWindowTitle("AUTO SHADER")
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.custom_set_style_sheet()

        # set default pink texture
        self.update_buttons_icons()

        self.updateRegexUI()

    def custom_set_style_sheet(self):
        print("function style for widget")
        self.setStyleSheet("background-color : #192E5B;")
        self.set_style_sheet_Desc_Label_wdg(
            self.description_te, self.FONT_COLOR_DESC, self.FONT_LABEL_DESC, self.FONT_SIZE_DESC
        )

        self.set_style_sheet_btn(self.apply_textures_btn, self.BTN_BACKGROUND_COLOR, self.FONT_LABEL_DESC)

        # Set all the label on the top
        self.set_style_sheet_Desc_Label_wdg(self.path_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL)
        self.set_style_sheet_Desc_Label_wdg(
            self.map_prefix_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.map_suffix_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.map_type_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.color_filter_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.metalness_filter_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.specular_filter_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.normal_filter_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )

        # Set all the line edit on the top
        self.set_style_sheet_line_edit(self.maps_path_le)
        self.set_style_sheet_line_edit(self.map_prefix_le)
        self.set_style_sheet_line_edit(self.map_suffix_le)
        self.set_style_sheet_line_edit(self.color_le)
        self.set_style_sheet_line_edit(self.metalness_le)
        self.set_style_sheet_line_edit(self.specular_le)
        self.set_style_sheet_line_edit(self.normal_le)

        # Set style of 4 bottom square
        self.set_style_sheet_Desc_Label_wdg(
            self.base_color_bottom_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.metalness_bottom_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.specular_bottom_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )
        self.set_style_sheet_Desc_Label_wdg(
            self.normal_bottom_lbl, self.FONT_COLOR_TITLE, self.FONT_LIST, self.FONT_SIZE_LABEL
        )

        self.set_style_sheet_checkbox(
            self.color_checkbox, self.normal_checkbox, self.specular_checkbox, self.metalness_checkbox
        )

        # self.set_style_sheet_btn(self.close_btn, self.BTN_BACKGROUND_COLOR,self.FONT_LABEL_DESC)

    def set_style_sheet_checkbox(*list_checkbox_widget):
        print("dans la fonction")
        for checkbox_wdg in list_checkbox_widget:
            checkbox_wdg.setStyleSheet(
                """
                                        QCheckBox::indicator{
                                            background-image: url(D:/ATI/M1/IntensifJanvier/img_ressources/green_checked_with_border.png);
                                        }
                                        """
            )

    def set_style_sheet_list_wdg(self, wdg_list, background_color, font_type):
        wdg_list.setFont(font_type)
        wdg_list.setStyleSheet(
            f"""background-color : {background_color};
                              border-radius : 5px;
                              """
        )

    def set_style_sheet_Desc_Label_wdg(self, wdg_list, font_color, font_type, font_size):
        wdg_list.setFont(font_type)
        wdg_list.setStyleSheet(
            f"""
                                color : {font_color};
                                font-size : {font_size}px;
                                """
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

    def set_style_sheet_line_edit(self, wdg_edit):
        wdg_edit.setStyleSheet(
            f"""
                               QLineEdit:focus{{
                                background-color : white;
                                color : black;
                               }} 
        """
        )

    def create_widgets(self):
        ##############
        # TOP WIDGETS
        ##############
        self.title_lbl = QtWidgets.QLabel(
            "<span style='color:green'>GUILIC</span> AutoShader <span style='color:green'>Tool</span>"
        )
        # top left widgets
        # labels
        # tl grid 00
        self.path_lbl = QtWidgets.QLabel("maps_path")
        # tl grid 01
        self.maps_path_le = QtWidgets.QLineEdit()
        # tl grid 02
        self.path_btn = QtWidgets.QPushButton("...")
        # tl grid 10
        self.map_prefix_lbl = QtWidgets.QLabel("map_prefix")
        # tl grid 11
        self.map_prefix_le = QtWidgets.QLineEdit("p_")
        # tl grid 20
        self.map_suffix_lbl = QtWidgets.QLabel("map_suffix")
        # tl grid 21
        self.map_suffix_le = QtWidgets.QLineEdit("_s")
        # tl grid 30
        self.map_type_lbl = QtWidgets.QLabel("map_type")
        # tl grid 31
        self.map_type_combobox = QtWidgets.QComboBox()
        # populate combobox
        self.map_type_combobox.addItems(self.extension_filters)
        self.map_type_combobox.setCurrentIndex(3)

        # top center widgets
        # tr grid 00
        self.color_checkbox = QtWidgets.QCheckBox()
        self.color_checkbox.setChecked(True)
        # tr grid 01
        self.color_filter_lbl = QtWidgets.QLabel("color_filter")
        # tr grid 02
        self.color_le = QtWidgets.QLineEdit("color")
        # tr grid 10
        self.metalness_checkbox = QtWidgets.QCheckBox()
        self.metalness_checkbox.setChecked(True)
        # tr grid 11
        self.metalness_filter_lbl = QtWidgets.QLabel("metalness_filter")
        # tr grid 12
        self.metalness_le = QtWidgets.QLineEdit("metal")
        # tr grid 20
        self.specular_checkbox = QtWidgets.QCheckBox()
        self.specular_checkbox.setChecked(True)
        # tr grid 21
        self.specular_filter_lbl = QtWidgets.QLabel("specular_filter")
        # tr grid 22
        self.specular_le = QtWidgets.QLineEdit("specular")
        # tr grid 30
        self.normal_checkbox = QtWidgets.QCheckBox()
        self.normal_checkbox.setChecked(True)
        # tr grid 31
        self.normal_filter_lbl = QtWidgets.QLabel("normal_filter")
        # tr grid 32
        self.normal_le = QtWidgets.QLineEdit("normal")

        # top right widgets regex
        self.color_regex_lbl = QtWidgets.QLabel("color regex")
        self.metalness_regex_lbl = QtWidgets.QLabel("metalness regex")
        self.specular_regex_lbl = QtWidgets.QLabel("specular regex")
        self.normal_regex_lbl = QtWidgets.QLabel("normal regex")

        self.color_regex_le = QtWidgets.QLineEdit()
        self.metalness_regex_le = QtWidgets.QLineEdit()
        self.specular_regex_le = QtWidgets.QLineEdit()
        self.normal_regex_le = QtWidgets.QLineEdit()

        # tool description wdg
        self.description_te = self.DESCRIPTION_TE

        #################
        # BOTTOM WIDGETS
        #################
        # labels
        self.base_color_bottom_lbl = QtWidgets.QLabel("base_color")
        self.metalness_bottom_lbl = QtWidgets.QLabel("metalness")
        self.specular_bottom_lbl = QtWidgets.QLabel("specular")
        self.normal_bottom_lbl = QtWidgets.QLabel("normal")

        # set alignment
        self.base_color_bottom_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.metalness_bottom_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.specular_bottom_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.normal_bottom_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Setting only the font and font size of the title_lbl
        self.title_lbl.setFont(self.FONT_LABEL_DESC)
        self.title_lbl.setStyleSheet(
            f"""
                                        font-size : {self.FONT_SIZE_TITLE}px;
                                        margin-bottom : 20px;
                                    """
        )

        # images
        """
        QPushButton *button = new QPushButton;
        button->setIcon(QIcon(":/icons/..."));
        button->setIconSize(QSize(65, 65));
        """

        self.base_color_img_btn = QtWidgets.QPushButton()
        # self.base_color_img_btn.setIcon(QtGui.QIcon("G:/ATI-M1/INTENSIFS_sem1/auto-shader/textures/E9_Lamp_Material_albedo.jpeg"))
        self.base_color_img_btn.setIconSize(QtCore.QSize(128, 128))

        self.metalness_img_btn = QtWidgets.QPushButton()
        # self.metalness_img_btn.setIcon(QtGui.QIcon("G:/ATI-M1/INTENSIFS_sem1/auto-shader/textures/E9_Lamp_Material_metallic.jpeg"))
        self.metalness_img_btn.setIconSize(QtCore.QSize(128, 128))

        self.specular_img_btn = QtWidgets.QPushButton()
        # self.specular_img_btn.setIcon(QtGui.QIcon("G:/ATI-M1/INTENSIFS_sem1/auto-shader/textures/E9_Lamp_Material_roughness.jpeg"))
        self.specular_img_btn.setIconSize(QtCore.QSize(128, 128))

        self.normal_img_btn = QtWidgets.QPushButton()
        # self.normal_img_btn.setIcon(QtGui.QIcon("G:/ATI-M1/INTENSIFS_sem1/auto-shader/textures/E9_Lamp_Material_normal.png"))
        self.normal_img_btn.setIconSize(QtCore.QSize(128, 128))

        self.apply_textures_btn = QtWidgets.QPushButton("Apply textures")

        # radio buttons
        self.selected_rbtn = QtWidgets.QRadioButton("selected")
        self.all_rbtn = QtWidgets.QRadioButton("all")

    def create_layout(self):
        main_vlayout = QtWidgets.QVBoxLayout(self)
        title_vlayout = QtWidgets.QVBoxLayout()

        grid_container_hlayout = QtWidgets.QHBoxLayout()

        bottom_vlayout = QtWidgets.QVBoxLayout()

        top_vlayout = QtWidgets.QVBoxLayout()
        top_vlayout.addWidget(self.title_lbl)

        top_left_g_layout = QtWidgets.QGridLayout()
        top_left_g_layout.addWidget(self.path_lbl, 0, 0)
        top_left_g_layout.addWidget(self.maps_path_le, 0, 1)
        top_left_g_layout.addWidget(self.path_btn, 0, 2)
        top_left_g_layout.addWidget(self.map_prefix_lbl, 1, 0)
        top_left_g_layout.addWidget(self.map_prefix_le, 1, 1)
        top_left_g_layout.addWidget(self.map_suffix_lbl, 2, 0)
        top_left_g_layout.addWidget(self.map_suffix_le, 2, 1)
        top_left_g_layout.addWidget(self.map_type_lbl, 3, 0)
        top_left_g_layout.addWidget(self.map_type_combobox, 3, 1)

        top_center_g_layout = QtWidgets.QGridLayout()
        top_center_g_layout.addWidget(self.color_checkbox, 0, 0)
        top_center_g_layout.addWidget(self.color_filter_lbl, 0, 1)
        top_center_g_layout.addWidget(self.color_le, 0, 2)
        top_center_g_layout.addWidget(self.metalness_checkbox, 1, 0)
        top_center_g_layout.addWidget(self.metalness_filter_lbl, 1, 1)
        top_center_g_layout.addWidget(self.metalness_le, 1, 2)
        top_center_g_layout.addWidget(self.specular_checkbox, 2, 0)
        top_center_g_layout.addWidget(self.specular_filter_lbl, 2, 1)
        top_center_g_layout.addWidget(self.specular_le, 2, 2)
        top_center_g_layout.addWidget(self.normal_checkbox, 3, 0)
        top_center_g_layout.addWidget(self.normal_filter_lbl, 3, 1)
        top_center_g_layout.addWidget(self.normal_le, 3, 2)

        top_right_g_layout = QtWidgets.QGridLayout()
        top_right_g_layout.addWidget(self.color_regex_lbl, 0, 0)
        top_right_g_layout.addWidget(self.color_regex_le, 0, 1)
        top_right_g_layout.addWidget(self.metalness_regex_lbl, 1, 0)
        top_right_g_layout.addWidget(self.metalness_regex_le, 1, 1)
        top_right_g_layout.addWidget(self.specular_regex_lbl, 2, 0)
        top_right_g_layout.addWidget(self.specular_regex_le, 2, 1)
        top_right_g_layout.addWidget(self.normal_regex_lbl, 3, 0)
        top_right_g_layout.addWidget(self.normal_regex_le, 3, 1)

        bottom_g_layout = QtWidgets.QGridLayout()

        bottom_g_layout.addWidget(self.base_color_bottom_lbl, 0, 0)
        bottom_g_layout.addWidget(self.metalness_bottom_lbl, 0, 1)
        bottom_g_layout.addWidget(self.specular_bottom_lbl, 0, 2)
        bottom_g_layout.addWidget(self.normal_bottom_lbl, 0, 3)

        bottom_g_layout.addWidget(self.base_color_img_btn, 1, 0)
        bottom_g_layout.addWidget(self.metalness_img_btn, 1, 1)
        bottom_g_layout.addWidget(self.specular_img_btn, 1, 2)
        bottom_g_layout.addWidget(self.normal_img_btn, 1, 3)

        bottom_rb_layout = QtWidgets.QHBoxLayout()
        bottom_rb_layout.addWidget(self.selected_rbtn)
        bottom_rb_layout.addWidget(self.all_rbtn)

        grid_container_hlayout.addLayout(top_left_g_layout)
        grid_container_hlayout.addLayout(top_center_g_layout)
        grid_container_hlayout.addLayout(top_right_g_layout)

        top_vlayout.addLayout(grid_container_hlayout)
        # top_vlayout.addWidget(self.import_from_folder_btn)
        top_vlayout.addWidget(self.description_te)

        bottom_vlayout.addLayout(bottom_g_layout)
        bottom_vlayout.addWidget(self.apply_textures_btn)

        main_vlayout.addLayout(title_vlayout)
        main_vlayout.addLayout(top_vlayout)
        main_vlayout.addLayout(bottom_vlayout)
        main_vlayout.addLayout(bottom_rb_layout)

    def create_connections(self):
        # btn path
        self.path_btn.clicked.connect(self.import_textures_is_clicked)

        # btn texture
        self.base_color_img_btn.clicked.connect(self.base_color_btn_clicked)
        self.metalness_img_btn.clicked.connect(self.metalness_btn_clicked)
        self.specular_img_btn.clicked.connect(self.specular_btn_clicked)
        self.normal_img_btn.clicked.connect(self.normal_btn_clicked)

        # btn apply texture
        self.apply_textures_btn.clicked.connect(self.import_btn_clicked)

        # on text changed for prefix, suffix, extension and filters
        self.map_prefix_le.textChanged.connect(self.updateRegexUI)
        self.map_suffix_le.textChanged.connect(self.updateRegexUI)
        self.color_le.textChanged.connect(self.updateRegexUI)
        self.metalness_le.textChanged.connect(self.updateRegexUI)
        self.specular_le.textChanged.connect(self.updateRegexUI)
        self.normal_le.textChanged.connect(self.updateRegexUI)
        # extension
        self.map_type_combobox.currentIndexChanged.connect(self.updateRegexUI)

    def updateRegexUI(self):
        # get values
        prefix = self.map_prefix_le.text()
        suffix = self.map_suffix_le.text()
        type = self.map_type_combobox.currentText()

        color_filter = self.color_le.text()
        metalness_filter = self.metalness_le.text()
        specular_filter = self.specular_le.text()
        normal_filter = self.normal_le.text()

        color_regex_str = f"{prefix}*{color_filter}*{suffix}*{type}"
        metalness_regex_str = f"{prefix}*{metalness_filter}*{suffix}*{type}"
        specular_regex_str = f"{prefix}*{specular_filter}*{suffix}*{type}"
        normal_regex_str = f"{prefix}*{normal_filter}*{suffix}*{type}"

        # write new values
        self.color_regex_le.setText(color_regex_str)
        self.metalness_regex_le.setText(metalness_regex_str)
        self.specular_regex_le.setText(specular_regex_str)
        self.normal_regex_le.setText(normal_regex_str)

    def import_btn_clicked(self):
        print("import_btn_clicked()")
        # TODO all or selected with radio buttons
        meshs_list = cmds.ls(sl=True)
        print(meshs_list)
        # meshList_lr = cmds.listRelatives(cmds.ls(g=True), p=True, pa=True)
        # print(meshList_lr)

        for mesh in meshs_list:
            material = mesh + "_MAT"
            print("============================================================")
            print("Creating material: " + material + "...")
            print("On mesh: " + mesh + "...")
            print("============================================================")
            cmds.shadingNode("aiStandardSurface", asShader=True, name=material)  # plus a shading node
            cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=material + "_SG")
            cmds.connectAttr(material + ".outColor", material + "_SG.surfaceShader", force=True)
            cmds.select(mesh)
            cmds.hyperShade(assign=material)

            for type, textureFile in self.texture_files_path.items():
                print(type, textureFile)
                if type == "color":
                    self.colorMap(textureFile, material)
                elif type == "metalness":
                    self.metalnessMap(textureFile, material)
                elif type == "specular":
                    self.specularMap(textureFile, material)
                elif type == "normal":
                    self.normalMap(textureFile, material)
                else:
                    print("error import_btn_clicked")

    def colorMap(self, textureFile, material):
        print("colorMap()")
        # if a file texture is already connected to this input, update it
        # otherwise, delete it
        input = "baseColor"
        colorSpace = "sRGB"

        # no connected file texture, so make a new one
        newFile = cmds.shadingNode("file", asTexture=1, icm=True)
        newPlacer = cmds.shadingNode("place2dTexture", asUtility=1, icm=True)

        # make common connections between place2dTexture and file texture
        connections = [
            "rotateUV",
            "offset",
            "noiseUV",
            "vertexCameraOne",
            "vertexUvThree",
            "vertexUvTwo",
            "vertexUvOne",
            "repeatUV",
            "wrapV",
            "wrapU",
            "stagger",
            "mirrorU",
            "mirrorV",
            "rotateFrame",
            "translateFrame",
            "coverage",
        ]
        cmds.connectAttr(newPlacer + ".outUV", newFile + ".uvCoord")
        cmds.connectAttr(newPlacer + ".outUvFilterSize", newFile + ".uvFilterSize")

        for connection in connections:
            cmds.connectAttr(newPlacer + "." + connection, newFile + "." + connection)

        # now connect the file texture output to the material input
        print("Connecting color map...")
        cmds.connectAttr(newFile + ".outColor", material + "." + input, f=1)
        print(">> " + newFile + ".outColor" + " connected to " + material + "." + input)
        cmds.setAttr(newFile + ".alphaIsLuminance", 0)
        print(">> " + newFile + ".alphaIsLuminance set to 0")

        cmds.setAttr(newFile + ".fileTextureName", textureFile, type="string")
        cmds.setAttr(newFile + ".cs", colorSpace, type="string")
        print(">> " + newFile + ".cs set to " + colorSpace)
        print(" ")

    def metalnessMap(self, textureFile, material):
        print("metalnessMap()")
        # if a file texture is already connected to this input, update it
        # otherwise, delete it
        input = "metalness"
        colorSpace = "Raw"

        # no connected file texture, so make a new one
        newFile = cmds.shadingNode("file", asTexture=1, icm=True)
        newPlacer = cmds.shadingNode("place2dTexture", asUtility=1, icm=True)
        # make common connections between place2dTexture and file texture
        connections = [
            "rotateUV",
            "offset",
            "noiseUV",
            "vertexCameraOne",
            "vertexUvThree",
            "vertexUvTwo",
            "vertexUvOne",
            "repeatUV",
            "wrapV",
            "wrapU",
            "stagger",
            "mirrorU",
            "mirrorV",
            "rotateFrame",
            "translateFrame",
            "coverage",
        ]
        cmds.connectAttr(newPlacer + ".outUV", newFile + ".uvCoord")
        cmds.connectAttr(newPlacer + ".outUvFilterSize", newFile + ".uvFilterSize")
        for i in connections:
            cmds.connectAttr(newPlacer + "." + i, newFile + "." + i)
        print("Connecting metalness map...")
        cmds.connectAttr(newFile + ".outAlpha", material + "." + input, f=1)
        print(">> " + newFile + ".outAlpha" + " connected to " + material + "." + input)
        cmds.setAttr(newFile + ".alphaIsLuminance", 1)
        print(">> " + newFile + ".alphaIsLuminance set to 1")

        cmds.setAttr(newFile + ".fileTextureName", textureFile, type="string")
        cmds.setAttr(newFile + ".cs", colorSpace, type="string")
        print(">> " + newFile + ".cs set to " + colorSpace)
        print(" ")

    def specularMap(self, textureFile, material):
        print("specularMap()")
        # if a file texture is already connected to this input, update it
        # otherwise, delete it
        input = "specularRoughness"
        # debug
        # colorSpace = 'Specular'
        colorSpace = "Raw"

        # no connected file texture, so make a new one
        newFile = cmds.shadingNode("file", asTexture=1, icm=True)
        newPlacer = cmds.shadingNode("place2dTexture", asUtility=1, icm=True)
        # make common connections between place2dTexture and file texture
        connections = [
            "rotateUV",
            "offset",
            "noiseUV",
            "vertexCameraOne",
            "vertexUvThree",
            "vertexUvTwo",
            "vertexUvOne",
            "repeatUV",
            "wrapV",
            "wrapU",
            "stagger",
            "mirrorU",
            "mirrorV",
            "rotateFrame",
            "translateFrame",
            "coverage",
        ]
        cmds.connectAttr(newPlacer + ".outUV", newFile + ".uvCoord")
        cmds.connectAttr(newPlacer + ".outUvFilterSize", newFile + ".uvFilterSize")
        for i in connections:
            cmds.connectAttr(newPlacer + "." + i, newFile + "." + i)
        print("Connecting specular map...")
        cmds.connectAttr(newFile + ".outAlpha", material + "." + input, f=1)
        print(">> " + newFile + ".outAlpha" + " connected to " + material + "." + input)
        cmds.setAttr(newFile + ".alphaIsLuminance", 1)
        print(">> " + newFile + ".alphaIsLuminance set to 1")

        cmds.setAttr(newFile + ".fileTextureName", textureFile, type="string")
        cmds.setAttr(newFile + ".cs", colorSpace, type="string")
        print(">> " + newFile + ".cs set to " + colorSpace)
        print(" ")

    def normalMap(self, textureFile, material):
        print("normalMap()")
        # if a file texture is already connected to this input, update it
        # otherwise, delete it
        input = "normalCamera"
        colorSpace = "Raw"

        # no connected file texture, so make a new one
        newFile = cmds.shadingNode("file", asTexture=1, icm=True)
        newPlacer = cmds.shadingNode("place2dTexture", asUtility=1, icm=True)
        # make common connections between place2dTexture and file texture
        connections = [
            "rotateUV",
            "offset",
            "noiseUV",
            "vertexCameraOne",
            "vertexUvThree",
            "vertexUvTwo",
            "vertexUvOne",
            "repeatUV",
            "wrapV",
            "wrapU",
            "stagger",
            "mirrorU",
            "mirrorV",
            "rotateFrame",
            "translateFrame",
            "coverage",
        ]
        cmds.connectAttr(newPlacer + ".outUV", newFile + ".uvCoord")
        cmds.connectAttr(newPlacer + ".outUvFilterSize", newFile + ".uvFilterSize")
        for i in connections:
            cmds.connectAttr(newPlacer + "." + i, newFile + "." + i)
        print("Connecting normal map...")
        bumpNode = cmds.shadingNode("bump2d", asUtility=1, icm=True)
        cmds.connectAttr(newFile + ".outAlpha", bumpNode + ".bumpValue", f=1)
        cmds.connectAttr(bumpNode + ".outNormal", material + "." + input, f=1)
        cmds.setAttr(bumpNode + ".bumpInterp", 1)
        print(">> " + newFile + " set to tangent space normals")
        cmds.setAttr(bumpNode + ".aiFlipG", 0)
        print(">> " + newFile + ".FlipRG set to 0")
        cmds.setAttr(bumpNode + ".aiFlipR", 0)
        cmds.setAttr(newFile + ".alphaIsLuminance", 0)
        print(">> " + newFile + ".alphaIsLuminance set to 0")

        cmds.setAttr(newFile + ".fileTextureName", textureFile, type="string")
        cmds.setAttr(newFile + ".cs", colorSpace, type="string")
        print(">> " + newFile + ".cs set to " + colorSpace)
        print(" ")

    def base_color_btn_clicked(self):
        print("base_color_btn_clicked()")
        qfd = QtWidgets.QFileDialog()

        texture_path = qfd.getOpenFileName(
            parent=self,
            caption="Open color texture",
            dir=".",
            filter=f"Image files ({self.extension_str})",
        )[0]
        self.texture_files_path["color"] = texture_path
        self.update_buttons_icons()

    def metalness_btn_clicked(self):
        print("metalness_btn_clicked()")
        qfd = QtWidgets.QFileDialog()

        texture_path = qfd.getOpenFileName(
            parent=self,
            caption="Open metalness texture",
            dir=".",
            filter=f"Image files ({self.extension_str})",
        )[0]
        self.texture_files_path["metalness"] = texture_path
        self.update_buttons_icons()

    def specular_btn_clicked(self):
        print("specular_btn_clicked()")
        qfd = QtWidgets.QFileDialog()

        texture_path = qfd.getOpenFileName(
            parent=self,
            caption="Open specular texture",
            dir=".",
            filter=f"Image files ({self.extension_str})",
        )[0]
        self.texture_files_path["specular"] = texture_path
        self.update_buttons_icons()

    def normal_btn_clicked(self):
        print("normal_btn_clicked()")
        qfd = QtWidgets.QFileDialog()

        texture_path = qfd.getOpenFileName(
            parent=self,
            caption="Open normal texture",
            dir=".",
            filter=f"Image files ({self.extension_str})",
        )[0]
        self.texture_files_path["normal"] = texture_path
        self.update_buttons_icons()

    def import_textures_is_clicked(self):
        print("import_textures_is_clicked()")
        qfd = QtWidgets.QFileDialog()
        # setup options qfiledialog
        qfd.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        qfd.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        qfd.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
        qfd.setNameFilterDetailsVisible(True)
        qfd.setNameFilters(self.extension_filters)

        self.maps_path = qfd.getExistingDirectory(self, "select directory")
        self.maps_path_le.setText(self.maps_path)

        self.get_values_from_UI()

        abs_filepaths = []
        abs_filepaths = self.get_abs_filepaths_in_folder(self.maps_path)
        print(abs_filepaths)
        self.associate_texture_paths(abs_filepaths)

        self.update_buttons_icons()

    def update_buttons_icons(self):
        print("update_buttons_icons()")
        for key, value in self.texture_files_path.items():
            print(key, value)
            if key == "color":
                self.base_color_img_btn.setIcon(QtGui.QIcon(f"{value}"))
                self.base_color_img_btn.setIconSize(QtCore.QSize(128, 128))
            if key == "metalness":
                self.metalness_img_btn.setIcon(QtGui.QIcon(f"{value}"))
                self.metalness_img_btn.setIconSize(QtCore.QSize(128, 128))
            if key == "specular":
                self.specular_img_btn.setIcon(QtGui.QIcon(f"{value}"))
                self.specular_img_btn.setIconSize(QtCore.QSize(128, 128))
            if key == "normal":
                self.normal_img_btn.setIcon(QtGui.QIcon(f"{value}"))
                self.normal_img_btn.setIconSize(QtCore.QSize(128, 128))

    def get_values_from_UI(self):
        print("get_values_from_UI()")
        self.map_prefix = self.map_prefix_le.text()
        self.map_suffix = self.map_suffix_le.text()
        self.map_type = self.map_type_combobox.currentText()

        self.selected_is_checked = self.selected_rbtn.isChecked()
        self.all_is_checked = self.all_rbtn.isChecked()

        self.color_filter = self.color_le.text() if self.color_checkbox.isChecked() else ""
        self.metalness_filter = self.metalness_le.text() if self.metalness_checkbox.isChecked() else ""
        self.specular_filter = self.specular_le.text() if self.specular_checkbox.isChecked() else ""
        self.normal_filter = self.normal_le.text() if self.normal_checkbox.isChecked() else ""

        print(self.map_prefix, self.map_suffix, self.map_type)
        print(self.selected_is_checked, self.all_is_checked)
        print(
            self.color_filter,
            self.metalness_filter,
            self.specular_filter,
            self.normal_filter,
        )

    def get_abs_filepaths_in_folder(self, folder_path):
        print("get_files_in_folder()")
        abs_filepaths = []
        for dirpath, _, filenames in os.walk(folder_path):
            for f in filenames:
                fpath = os.path.abspath(os.path.join(dirpath, f))
                abs_filepaths.append(fpath)

        print("abs_filepaths")
        return abs_filepaths

    def associate_texture_paths(self, texture_filepaths):
        print("associate_texture_paths()")
        # get values
        color_full_re = self.color_regex_le.text() + "$"
        metalness_full_re = self.metalness_regex_le.text() + "$"
        specular_full_re = self.specular_regex_le.text() + "$"
        normal_full_re = self.normal_regex_le.text() + "$"
        print(color_full_re, metalness_full_re, specular_full_re, normal_full_re)
        # regex
        color_re = re.compile(rf"{color_full_re}")
        metalness_re = re.compile(rf"{metalness_full_re}$")
        specular_re = re.compile(rf"{specular_full_re}$")
        normal_re = re.compile(rf"{normal_full_re}$")
        # color_re = re.compile(
        #     rf"{self.map_prefix}*{self.color_filter}*{self.map_suffix}*{self.map_type}$"
        # )
        # metalness_re = re.compile(
        #     rf"{self.map_prefix}*{self.metalness_filter}*{self.map_suffix}*{self.map_type}$"
        # )
        # specular_re = re.compile(
        #     rf"{self.map_prefix}*{self.specular_filter}*{self.map_suffix}*{self.map_type}$"
        # )
        # normal_re = re.compile(
        #     rf"{self.map_prefix}*{self.normal_filter}*{self.map_suffix}*{self.map_type}$"
        # )

        print(color_re)
        print(metalness_re)
        print(specular_re)
        print(normal_re)

        for file in texture_filepaths:
            print(f"-- FILE: {file} --")
            color_search = color_re.search(file)
            metalness_search = metalness_re.search(file)
            specular_search = specular_re.search(file)
            normal_search = normal_re.search(file)
            print(color_search)
            print(metalness_search)
            print(specular_search)
            print(normal_search)
            if color_search:
                self.texture_files_path["color"] = file
            if metalness_search:
                self.texture_files_path["metalness"] = file
            if specular_search:
                self.texture_files_path["specular"] = file
            if normal_search:
                self.texture_files_path["normal"] = file
        print(self.texture_files_path)


if __name__ == "__main__":

    try:
        autoshader_dialog.close()  # pylint: disable=E0601
        autoshader_dialog.deleteLater()
    except:
        pass

    autoshader_dialog = AutoShaderDialog()
    autoshader_dialog.show()
