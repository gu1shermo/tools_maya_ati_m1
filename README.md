# 3 TOOLS FOR MAYA 2022
## TOOL1: Light Manager

The Maya Light Manager is a tool written in Maya that allows you to manage all the attributes of lights in your scene. With this tool, you can easily select lights, enable/disable lights, as well as control their properties, such as color, intensity, and radius.
The tool updates himself when adding / removing lights and all actions are synchronized with Maya UI.

Light Manager        |  
:-------------------------:   |
![](./screenshots/tool1.jpg) |

### Features Light Manager

The Maya Light Manager comes with a range of features that can help you streamline your lighting workflow, including:

- **Light selection:** Quickly select any light in your scene.
- **Attribute editing:** Change any attribute of a selected light, including color, intensity, cone angle, and decay rate.
- **Customization:** Add/remove any attribute you want to appear in the interface.

## TOOL2: Light Attribute Copier

The Maya Light Attribute Copier Tool is a Python script that allows users to copy attributes from one light to other lights chosen by the user. The tool is customizable, meaning that users can filter the attributes they want to appear by editing the code.

Light Attribute Copier       |  
:-------------------------:   |
![](./screenshots/tool2.jpg) |

### Usage Copy Light Attributes
<ol>
  <li>Select one light source</li>
  <li>Select the source light attributes you want to copy on the destination lights</li>
  <li>Select one or more lights for destination</li>
  <li>Click the copy button</li>
  <li>If you create a new light click on the update button to make it appear</li>
</ol>

## TOOL3: Auto Shader

The Maya Auto Shader tool is a Python script that allows users to easily attach texture maps to any object in the scene. The tool supports attaching base color, metalness, specular, and normal maps. Users can either specify a folder and a regex pattern to automatically find the textures, or they can choose the texture files individually.

Auto Shader      |  
:-------------------------:   |
![](./screenshots/tool3.jpg) |

### Usage Auto Shader
<ol>
  <li>Choose a folder path that contains your texture maps.</li>
  <li>You can specify a regex pattern to filter your files(prefix, suffix, and keyword for the concerned map).</li>
  <li>If files are missing (pink square), you can choose the filepath by clicking on the square.</li>
  <li>Click the Apply Textures button</li>
</ol>

## Installation

To install each of the tools, follow these steps:

1. Download the latest version from the [releases](https://github.com/yourusername/maya-light-manager/releases) page.
2. Extract the ZIP file to a folder on your computer.
3. In Maya, open the Script Editor (Window > General Editors > Script Editor).
4. In the Script Editor, select "Python" as the language and open the downloaded script file.
5. Press "Ctrl+Enter" to execute the script.

## Usage

1. To use the Maya Light Manager, simply open the tool. From there, you can edit any attribute of all the lights in the scene (including Arnold lights).
2. To use the Maya Copy Light Attributes, TODO
3. To use the Maya Auto Shader, TODO

## License
The Maya Light Manager is released under the [MIT License](LICENSE), which means you can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to certain conditions. See the full license for details.
