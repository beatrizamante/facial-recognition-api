def compare_encodings(new_encoding, encoded_faces, threshold=0.5):
    '''Função para comparar o encoding do usuário atual com uma lista de encodings
    puxada da base de dados. Recebe como parâmetro o novo encoding e retorna o label do
    usuário e true se houver match. Caso não, retorna o label vazio e um false boolean.'''
    for entry in encoded_faces:
        label = entry['label']
        mail = entry['mail']
        stored_encode = [np.array(encoding) for encoding in entry['encoding']]
        distances = face_recognition.face_distance(stored_encode, new_encoding)
        if len(distances) == 2:
            if distances[0] < threshold and distances[1] < threshold:
            return label, mail, True
    return "Desconhecido", None, False
