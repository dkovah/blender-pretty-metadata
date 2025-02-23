# blender-pretty-metadata

A simple blender plugin to edit object metadata in a human-readable way. The metadata is added as blender custom properties to the objects and remains in the scene as long as it's exported to a compatible format, such as GLTF or FBX.

## Usage:
1) Install the plugin\
Open Blender and go to Edit -> Preferences -> Addons -> Install and select the plugin file.

2) Select the JSON configuration file\
After installing it a new option will be visible on the plugin preferences menu to select the JSON file with the project metadata structure.

3) Edit the objects metadata\
After selecting a suitable JSON file, a new menu called "Metadata" will be added to the properties of all the objects in the scene with fields that will vary depending on the JSON structure.

4) (Optional) Export the project to a metadata-compatible format, like GLTF.\
Be sure to check the option "Include -> Data -> Custom Properties" (wich is disabled by defalut) on the export settings if exporting to GLTF. Other formats should have similar options.

## JSON Structure:
The JSON configuration file should look something like this:

```json
{
  "items": [
    {
      "id": "some_type_id",
      "label": "Some Object Type",
      "description": "The description is optional and shows as a tooltip on the item type selection menu",
      "attributes": [
        {
          "id": "some_string_attribute",
          "label": "A string atribute for this type",
          "type": "string"
        },
        {
          "id": "some_float_attribute",
          "label": "A float atribute for this type",
          "type": "float"
        },
        {
          "id": "some_int_attribute",
          "label": "An integer atribute for this type",
          "type": "int"
        },
        {
          "id": "some_boolean_attribute",
          "label": "An boolean atribute for this type",
          "type": "boolean"
        },
        {
          "id": "some_enum_attribute",
          "label": "Types can also have an enum as attribute",
          "type": "enum",
          "options": [
            {
              "id": "some_enum_element_id",
              "label": "Some element",
              "description": "If a type has an enum as an attribute, its values can also have optional description"
            },
            {
              "id": "other_enum_element_id",
              "label": "Other element"
            }
          ]
        }
      ]
    },
    {
      "id": "door",
      "label": "Door",
      "attributes": [
        {
          "id": "weight",
          "label": "Weight",
          "type": "float"
        },
        {
          "id": "locked_by_default",
          "label": "Locked by default",
          "type": "boolean"
        }
      ]
    }
  ]
}
```

Currently, the plugin only support `string`,`int`, `float`,`boolean` and `enum` attribute types.
