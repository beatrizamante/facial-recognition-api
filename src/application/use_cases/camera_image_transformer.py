'''Pacote responsável por encontrar o centro da câmera e do rosto em tela.'''
import cv2

class CameraImageTransformer:
    '''Classe responsável por retornar tais medidas.
    Parâmetros:
        camera_width: comprimento da câmera - começa em 0, será alterado em face_service,
        camera_height: altura da câmera - começa em 0, será alterado em face_service,
        center_x: centro do canvas na posição horizontal,
        center_y: centro do canvas na posição vertical,
        face_x: centro horizontal do rosto retornado em face_locations,
        face_y: centro vertical do rosto retornado em face_locations,
        tolerance: distância mínima entre o centro do rosto e o centro do canvas
    '''
    def __init__(self,  camera_width=0, camera_height=0, tolerance = 380):
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.center_X = self.camera_width / 2
        self.center_y = self.camera_height / 2
        self.face_x = None
        self.face_y = None
        self.tolerance = tolerance

    def update_dimensions(self, width, height):
        '''Função responsável por fazer alteração dos valores iniciar da câmera,
        tendo em vista que podem ser puxados de dispositivos diferentes.
        Parâmetros:
            width: comprimento recebido do canvas (em face_services),
            height: altura recebida do canvas (em face_services)
        Não tem retornos, apenas altera as dimensões do canvas.
        '''
        self.camera_width = width
        self.camera_height = height
        self.center_X = width / 2
        self.center_y = height / 2

    def convert_to_rgb(self, frame):
        '''Função para ajustar frames recebidas para tipo de imagem que
        o facial-recognition reconhece e retorna o formato correto. Recebe uma frame
        e retorna a frame convertida para rgb.'''
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        return rgb_frame
