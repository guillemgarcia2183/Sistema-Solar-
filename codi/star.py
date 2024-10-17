import math

import moderngl as mgl
import glm

import numpy as np

def read_shader_src(path: str) -> str:
    # TODO: Error Handling
    with open(path, 'r') as shader_file:
        shader_code = shader_file.read()

    return shader_code

class Star:
    def __init__(self, app, x, y, z):
        self.app = app
        self.ctx = app.ctx

        self.x = x
        self.y = y
        self.z = z

        self.vbo = self.get_vbo()
        self.shader = self.get_shader_program()
        self.vao = self.get_vao()

        self.m_model = self.get_model_matrix()
        self.on_init()

    def on_init(self):
        # Essential for viewing
        self.shader['m_proj'].write(self.app.camera.m_proj)
        self.shader['m_view'].write(self.app.camera.m_view)
        self.shader['m_model'].write(self.m_model)

    def get_model_matrix(self):
        # TODO: From X+ Y+ Z+ -> x, y, z
        # CB -> v from V to u from U -> vU=u
        rads = glm.radians(23.44)
        m_model = glm.translate(-self.app.objects[2].position)
        m_model *= glm.rotate(glm.mat4(), rads, glm.vec3(0, 0, 1))
        return m_model

    def get_vbo(self):
        data = self.get_data()
        vbo = self.ctx.buffer(data)
        return vbo

    def render(self):
        self.ctx.enable(mgl.PROGRAM_POINT_SIZE)
        self.ctx.point_size = 5
        self.vao.render(mgl.POINTS)

    def destroy(self):
        self.vbo.release()
        self.shader.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_data(self):
        
        data = np.array([self.x, self.y, self.z], dtype='f4')
        return data

    def get_shader_program(self):
        
        program = self.ctx.program(
            vertex_shader=read_shader_src(r"./codi/shaders/star.vert"),
            fragment_shader=read_shader_src(r"./codi/shaders/star.frag"),
        )
        return program
