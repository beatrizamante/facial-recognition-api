'''Pacote responsável por encontrar o centro da câmera e do rosto em tela.'''

class CameraModel:
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
        
    def find_center_face(self, face_locations):
        '''Função responsável por encontrar o centro do rosto de uma imagem através de face_locations.
        Parâmetros: 
            face_locations: localização do rosto na imagem puxada por face_recognition.
        Função não faz retornos, apenas altera o valor face_x e face_y da classe.
        '''
        for face_location in face_locations:
            top, right, bottom, left = face_location
            self.face_x = (right + left) / 2
            self.face_y = (top + bottom) / 2
        
    def check_if_centered(self):
        '''Função responsável por comparar a distância entre o centro do rosto da imagem e o centro do canvas
        da camera.
            Compara os valores em horizontal X e vertical Y em abs. Se os valores estiverem dentro da tolerância,
            reconhece o rosto como True - centralizado. Senão, retorna False.
        '''
        print(self.face_x is not None)
        print(self.face_y is not None)
        if self.face_x is not None and self.face_y is not None:
            if abs(self.face_x - self.center_X) < self.tolerance and abs(self.face_y - self.center_y) < self.tolerance:
                return True
        return False
    
