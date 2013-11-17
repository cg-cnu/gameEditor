import bpy

def main(self, context):
	myMass = bpy.context.object.rigid_body.mass
	bpy.context.object.MyMass = myMass
	bpy.ops.rigidbody.object_remove()

class MassAssign(bpy.types.Operator):
    """ calculates mass on the object """
    bl_idname = "rigidbody.mass_assign"
    bl_label = "Assign mass"
    bl_options = {'REGISTER', 'UNDO'}
	
    def execute(self, context):
        main(self, context)
        return {'FINISHED'}
