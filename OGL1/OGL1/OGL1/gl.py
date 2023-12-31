import glm
from OpenGL.GL import * 
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):

	def __init__(self, screen):


		self.screen = screen
		_, _, self.width, self.height = screen.get_rect()

		self.clearColor = [0,0,0] 
		
		glEnable(GL_DEPTH_TEST)
		glViewport(0,0,self.width, self.height)

		self.scene = []

		self.elapsedTime = 0.0
		
		self.activeShader = None

		self.camPosition = glm.vec3(0,0,0)
		self.camRotation = glm.vec3(0,0,0)

		self.projectionMatirx = glm.perspective(glm.radians(60),			
												self.width / self.height,	
												0.1,						
												1000)						


	def getViewMatrix(self):
		identity = glm.mat4(1)

		translationMatrix = glm.translate(identity, self.camPosition)

		pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0))		
		yaw	  = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0))		
		roll  = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1))		

		rotationMatrix = pitch * yaw * roll

		camMatrix = translationMatrix * rotationMatrix

		return glm.inverse(camMatrix)


	def setShader(self, vertexShader, fragmentShader):
		if vertexShader is not None and fragmentShader is not None:
			self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
											   compileShader(fragmentShader, GL_FRAGMENT_SHADER))
		else:
			self.activeShader = None



	def render(self):

		glClearColor(*self.clearColor, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		if self.activeShader is not None:
			glUseProgram(self.activeShader)

			glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"viewMatrix"),
								1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))

			glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"projectionMatrix"),
								1, GL_FALSE, glm.value_ptr(self.projectionMatirx))

			glUniform1f(glGetUniformLocation(self.activeShader, "time"), self.elapsedTime)

		for obj in self.scene:
			if self.activeShader is not None:
				glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"modelMatrix"),
								1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))

			obj.render()