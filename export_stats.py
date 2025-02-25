bl_info = {
    "name": "Object Statistics Exporter",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Tool",
    "description": "Gathers statistics for selected objects and exports to CSV or JSON",
    "category": "Object",
}

import bpy
import json
import csv

def get_object_stats(obj):
    stats = {}
    if obj.type == 'MESH':
        mesh = obj.data
        stats['vertices'] = len(mesh.vertices)
        stats['edges'] = len(mesh.edges)
        stats['faces'] = len(mesh.polygons)
        stats['uv_layers'] = len(mesh.uv_layers)
    else:
        stats['vertices'] = 0
        stats['edges'] = 0
        stats['faces'] = 0
        stats['uv_layers'] = 0
    return stats

class OBJECT_OT_export_stats_csv(bpy.types.Operator):
    bl_idname = "object.export_stats_csv"
    bl_label = "Export Stats to CSV"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        selected_objects = context.selected_objects
        fieldnames = ['Object Name', 'Vertices', 'Edges', 'Faces', 'UV Layers']
        try:
            with open(self.filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for obj in selected_objects:
                    stats = get_object_stats(obj)
                    writer.writerow({
                        'Object Name': obj.name,
                        'Vertices': stats.get('vertices', 0),
                        'Edges': stats.get('edges', 0),
                        'Faces': stats.get('faces', 0),
                        'UV Layers': stats.get('uv_layers', 0)
                    })
            self.report({'INFO'}, f"Exported stats to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export CSV: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class OBJECT_OT_export_stats_json(bpy.types.Operator):
    bl_idname = "object.export_stats_json"
    bl_label = "Export Stats to JSON"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        selected_objects = context.selected_objects
        export_data = {}
        for obj in selected_objects:
            export_data[obj.name] = get_object_stats(obj)
        try:
            with open(self.filepath, 'w') as jsonfile:
                json.dump(export_data, jsonfile, indent=4)
            self.report({'INFO'}, f"Exported stats to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export JSON: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class VIEW3D_PT_object_stats_exporter(bpy.types.Panel):
    bl_label = "Object Statistics Exporter"
    bl_idname = "VIEW3D_PT_object_stats_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Selected Object Statistics:")

        for obj in context.selected_objects:
            stats = get_object_stats(obj)
            box = layout.box()
            box.label(text=f"Name: {obj.name}")
            box.label(text=f"Vertices: {stats.get('vertices', 0)}")
            box.label(text=f"Edges: {stats.get('edges', 0)}")
            box.label(text=f"Faces: {stats.get('faces', 0)}")
            box.label(text=f"UV Layers: {stats.get('uv_layers', 0)}")

        layout.separator()
        layout.label(text="Export Options:")
        layout.operator("object.export_stats_csv", text="Export to CSV")
        layout.operator("object.export_stats_json", text="Export to JSON")

def register():
    bpy.utils.register_class(OBJECT_OT_export_stats_csv)
    bpy.utils.register_class(OBJECT_OT_export_stats_json)
    bpy.utils.register_class(VIEW3D_PT_object_stats_exporter)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_object_stats_exporter)
    bpy.utils.unregister_class(OBJECT_OT_export_stats_json)
    bpy.utils.unregister_class(OBJECT_OT_export_stats_csv)

if __name__ == "__main__":
    register()
