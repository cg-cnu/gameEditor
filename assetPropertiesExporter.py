## have to export the BBValues 
import bpy, math, os
from bpy.props import StringProperty, BoolProperty, EnumProperty

def write_game_data(self, context):

	filepath = bpy.context.scene.render.filepath

	if os.path.exists(filepath) == False:
		self.report({'WARNING'}, " Select a valid path") 
	else:
		file = open(filepath+"\\gameData.txt", 'w', encoding='utf-8')
		
		init_selection = [ obj for obj in bpy.context.selected_objects if obj.type in ['MESH']]
		BB = [ obj for obj in init_selection if "_BB_" in obj.name ]
		selection = [obj.name for obj in init_selection if obj not in BB]
		selection.sort()
				
		for obj in selection:

			name = obj
			
			bpy.data.objects[name].select = True
			bpy.context.scene.objects.active = bpy.data.objects[name] 
			
			try:
				img = bpy.context.active_object.data.uv_textures[0].data.values()[0].image.name
			except IndexError:
				img = "none"
			location = bpy.context.object.location
			rotation = bpy.context.object.rotation_euler
			loc = [ str(round(i, 6)) for i in location ]
			rot = [ str(round(math.degrees(i), 6)) for i in rotation ]
			
			try:
				mass = str(round(bpy.context.scene.objects.active.rigid_body.mass, 6))
			except AttributeError:
				mass = "0"                    
			
			if bpy.context.scene.objects.active.StaticDynamic == 'One':
				state01 = 'Dynamic'
			else:
				state01 = 'Static'

			if bpy.context.scene.objects.active.HiddenVisible == 'One':
				state02 = 'Visible'
			else:
				state02 = 'Hidden'
			
			my_list = [ name, img, state02, state01, mass, loc[0] + "," + loc[1] + "," + loc[2], rot[0] + "," + rot[1]  + "," + rot[2] ]

			for each in my_list:            
				file.write( each )
				file.write(" ")
			file.write ("\n")    			
			
			# get the children
			children = bpy.data.objects[name].children
			if  len(children) != 0:
				matrix = bpy.context.object.matrix_world
				bpy.context.object.rotation_euler.zero()
				bpy.context.object.location = (0,0,0)
				for child in children:
					name = child.name
					bpy.context.scene.objects.active = bpy.data.objects[name]
					try:
						img = bpy.context.active_object.data.uv_textures[0].data.values()[0].image.name
					except IndexError:
						img = "none"
					location = bpy.context.object.location
					rotation = bpy.context.object.rotation_euler
					scale = bpy.context.object.scale
					loc = [ str(round(i, 6)) for i in  location]
					rot = [ str(round(math.degrees(i), 6)) for i in rotation ]
					sca = [ str(round(i, 6)) for i in scale ]

					my_list = [ name, loc[0] + "," + loc[1] + "," + loc[2], rot[0] + "," + rot[1]  + "," + rot[2], sca[0] + "," + sca[1]  + "," + sca[2] ]

					for each in my_list:            
						file.write( each )
						file.write(" ")
					file.write ("\n")
					
				bpy.context.object.matrix_world = matrix
				
			file.write ("\n")
			
		file.close()
		
	self.report({'INFO'}, " Exported " + str(len(selection)) + " assets")
	
	return {'FINISHED'}

class AssetPropertyExporter(bpy.types.Operator):
	""" exports the properties of the selected assets"""
	bl_idname = "export.asset_properties"  
	bl_label = "Asset Properties Exporter"
	
	def execute(self, context):
		return write_game_data(self, context)
