import bpy
import json
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
 
bl_info = {
    'name': 'Pretty Metadata',
    'category': 'All',
    'author': 'Yoandy Paz',
    'version': (1, 0, 0),
    'blender': (2, 80, 0),
    'location': '',
    'description': 'Add structured metadata to objects'
}

def update_handler(scene):
    addon_preferences = bpy.context.preferences.addons[__name__].preferences
    filepath = addon_preferences.filepath
    if(filepath == ""):
        return
    f = open(filepath)
    data = json.load(f)
    f.close()
    item_types = data["items"]
    parsed_types = [('NA', 'N/A', 'Not used in game')]
    for i in item_types:

        desc = ""
        if "description" in i:
            desc = i["description"]
        parsed_types.append((i["id"], i["label"], desc))

        for j in i["attributes"]:
            match j["type"]:
                case "string":
                    setattr(bpy.types.Object, j["id"], bpy.props.StringProperty(name=j["label"], default=""))
                case "boolean":
                    setattr(bpy.types.Object, i["id"]+"_"+j["id"], bpy.props.BoolProperty(name=j["label"], default=False))
                case "int":
                    setattr(bpy.types.Object, i["id"]+"_"+j["id"], bpy.props.IntProperty(name=j["label"], default=0))
                case "float":
                    setattr(bpy.types.Object, i["id"]+"_"+j["id"], bpy.props.FloatProperty(name=j["label"]))
                case "enum":
                    attr_values = j["options"]
                    enum_values = []
                    for k in attr_values:
                        kdesc = ""
                        if "description" in k:
                            kdesc = k["description"]
                        enum_values.append((k["id"], k["label"], kdesc))
                    setattr(bpy.types.Object, i["id"]+"_"+j["id"], bpy.props.EnumProperty(name=j["label"],items= enum_values,default=attr_values[0]["id"]))     
    
    bpy.types.Object.itemTag = bpy.props.EnumProperty(
        name="Object Type",
        items=parsed_types,
        default='NA'
    )


class PrettifyPanel(bpy.types.Panel):
    bl_label = "Metadata"
    bl_idname = "OBJECT_PT_pretty_metadata"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        preferences = context.preferences.addons[__name__].preferences
        filepath = preferences.filepath
        
        f = open(filepath)
        data = json.load(f)
        f.close()
    
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.prop(obj, "itemTag")

        if(obj.itemTag == "NA"): return

        selected_data = data["items"][0]
        for item in data["items"]:
            if item["id"] == obj.itemTag:
                selected_data = item
        
        for att in selected_data["attributes"]:
            row = layout.row()
            row.prop(obj, selected_data["id"] +"_" + att["id"])


class MetadataPrettifyPreferences(AddonPreferences):
    bl_idname = __name__
 
    filepath: StringProperty(
        name="JSON File Path",
        subtype='FILE_PATH',
    )
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select JSON configuration file")
        layout.prop(self, "filepath")
 
 
def register():
    bpy.utils.register_class(MetadataPrettifyPreferences)
    bpy.utils.register_class(PrettifyPanel)
    bpy.app.handlers.depsgraph_update_post.append(update_handler)
    update_handler(0)
 
 
def unregister():
    bpy.utils.unregister_class(MetadataPrettifyPreferences)
    bpy.utils.unregister_class(PrettifyPanel)
 
 
if __name__ == '__main__':
    register()