bl_info = {
	"name": "Game Editor",
	"description": " game Editor ",
	"author": "sreenivas alapati",
	"version": (1, 0),
	"blender": (2, 65, 0),
	"category": "Game Engine"
}

##################### importing modules ################

if "bpy" in locals():
	import imp
	imp.reload(objMultiExporter)
	imp.reload(assetPropertiesExporter)
	imp.reload(massCalculator)
else:
	from . import assetPropertiesExporter
	from . import objMultiExporter
	from . import massCalculator


#########################################################

import bpy, imp, math, mathutils, time, datetime
from bpy.props import *
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator

######## defining object properties ##################

bpy.types.Object.MyMass = FloatProperty(
		name = "Mass", 
		description = "Edit mass",
		default = 0,
		min = -100000000,
		max = 100000000)

bpy.types.Object.HiddenVisible = EnumProperty(
	items = [('One', 'Visible', 'One'), 
			 ('Two', 'Hidden', 'Two')],                 
	name = "visible/Hidden")
	
bpy.types.Object.StaticDynamic = EnumProperty(
	items = [('One', 'Dynamic', 'One'), 
			 ('Two', 'Static', 'Two')],                 
	name = "Static/Dynamic")

########### UI Panel ##########################
class GameEditor(bpy.types.Panel):
	"""Creates a gameEditor panel in the scene context of the properties editor"""
	bl_label = "Asset Properties Editor"
	bl_idname = "GAME_EDITOR_layout"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "object"
	
	def draw(self, context):                
		selection = [ obj for obj in bpy.context.selected_objects if obj.type in ['MESH']]       
		rd = bpy.context.scene.render
		
		layout = self.layout
		layout.prop(rd, "filepath", text="")
		layout.operator("export.multi_obj")
		layout.operator("export.asset_properties")

		row = layout.row(align=True)        
		row.label(text="Asset")
		row.label(text="Visible/Hidden")
		row.label(text="Static/Dynamic")
		row.label(text="Mass")
		
				
		for object in selection:
			RigidBodyObject = object.rigid_body
			name = object.name
			
			row = layout.row()            
			row.label(text= name)
			row.prop(object, "HiddenVisible", text = "")
			row.prop(object, "StaticDynamic", text = "")            
			
			try:
				mass = object.rigid_body.mass
				if mass == 1:
					row.operator("RIGIDBODY_OT_mass_calculate")
				if mass > 1:
					row.operator("rigidbody.mass_assign")
			except AttributeError:
				if object.MyMass == 0:
					row.operator("RIGIDBODY_OT_object_add")
				elif object.MyMass > 1:
					row.prop(object, "MyMass", text = "")
					
def menu_func_export(self, context):
	self.layout.operator(objMultiExporter.bl_idname, text= "Obj multi Exporter")
	self.layout.operator(assetPropertyExporter.bl_idname, text="Asset Properties Exporter")	
		
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_func_export)
 
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_func_export)
	
if __name__ == "__main__":
	register()
