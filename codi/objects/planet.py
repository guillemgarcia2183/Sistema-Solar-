import glm
import math
from objects.object import Object

class Planet(Object):
    __slots__=["size",
               "position",
               "velocity",
               "inclination",
               "eccentricity"]
    
    """Classe filla d'Objecte. Crea els Planetes.
    """
    def __init__(self, app, shader, texture, info, size, position, velocity, inclination, eccentricity):
        """Inicialització de la classe Planet. Tindrà els atributs de Object i els següents

        Args:
            size (glm.vec3): Tamany del planeta
            position (glm.vec3): Posició del planeta
            velocity (float): Velocitat del planeta
            inclination (float): Inclinació de rotació
            eccentricity (float): Excentritat de l'el·lipse
        """
        # Característiques de l'esfera
        self.size = size
        self.position = position
        self.velocity = velocity
        self.inclination = inclination
        self.eccentricity = eccentricity
        super().__init__(app, shader, texture, info)
        
    def get_model_matrix(self):
        """Obtenció de la model matrix
        Returns:
            glm.vec4: Matriu model 
        """
        m_model = glm.rotate(glm.mat4(), glm.radians(0), glm.vec3(0, 1, 0))
        m_model = glm.scale(m_model, self.size)  
        m_model = glm.translate(m_model, self.position)   
        return m_model
            
    def get_data(self):
        return self.create_sphere(False)
    
    def render(self):
        """Renderització del VAO i rotació dels planetes
        """
        self.texture.use()
        self.rotate_sun()
        self.rotate_self()
        self.vao.render()    

    def rotate_self(self):
        """Rotació del planeta sobre sí mateix.
        """        
        # Inclinación en el eje de rotación (por ejemplo, ligeramente inclinada)
        inclination_radians = math.radians(self.inclination)
        inclined_axis = glm.vec3(math.sin(inclination_radians), math.cos(inclination_radians), 0)

        # Normalizar el eje para que el vector tenga longitud 1
        inclined_axis = glm.normalize(inclined_axis)

        self.m_model = glm.rotate(self.m_model, self.app.time*self.velocity*20, inclined_axis)
        self.shader['m_model'].write(self.m_model)
        
    def rotate_sun(self):
        """Rotació del planeta sobre el sol.
        """
        # Crear una matriz de transformación inicial (identidad)
        m_model = glm.mat4()

        # Semieje mayor y menor basados en la distancia inicial del planeta al Sol
        a = glm.length(glm.vec2(self.position.x, self.position.z))  # La magnitud en XZ como semieje mayor
        b = a * (1 - self.eccentricity ** 2) ** 0.5 # Semieje menor (ajústalo según el grado de excentricidad que desees)

        # Calcular el ángulo en función del tiempo
        theta = self.app.time * self.velocity   # Ajusta la velocidad de la órbita

        # Posición del planeta en la órbita elíptica (plano XZ)
        x = a * glm.cos(theta)
        z = b * glm.sin(theta)
        y = self.position.y  # Mantener la altura constante o ajustarla si deseas órbitas inclinadas


        # Trasladar el planeta a la nueva posición calculada (órbita elíptica respecto al Sol en (0, 0, 0))
        new_position = glm.vec3(x, y, z)

        m_model = glm.translate(m_model, new_position)
        m_model = glm.scale(m_model, self.size)
        
        # Actualizar la matriz de modelo
        self.m_model = m_model    
